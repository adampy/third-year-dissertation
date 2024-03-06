# Adapted from: https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/

from prometheus.pod_data import PodData
from datetime import datetime
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

import azure_blob

LOOK_BACK = 1
SEED = 7
EPOCHS = 10
BATCH_SIZE = 1
TEST_SET_SIZE = 0.33

VERBOSITY = 0 #2

# fix random seed for reproducibility
tf.random.set_seed(SEED)


def create_dataset(dataset, look_back=1):
    # convert an array of values into a dataset matrix
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

def plot_predictions(dataset, train_predict, test_predict):
    # shift train predictions for plotting
    train_predict_plot = np.full_like(dataset, np.nan)
    train_predict_plot[LOOK_BACK:len(train_predict)+LOOK_BACK, :] = train_predict
    # shift test predictions for plotting
    test_predict_plot = np.full_like(dataset, np.nan)
    test_predict_plot[len(train_predict)+(LOOK_BACK*2)+1:len(dataset)-1, :] = test_predict
    # plot baseline and predictions
    plt.plot(scaler.inverse_transform(dataset))
    plt.plot(train_predict_plot)
    plt.plot(test_predict_plot)
    plt.show()

if __name__ == "__main__":
    start_date = datetime(2024, 3, 4, 16, 15, 0)
    end_date = datetime(2024, 3, 4, 17, 45, 0)
    
    webui_df = PodData.from_csv("prometheus/webui-05032024.csv").as_df(start_date=start_date, end_date=end_date)
    # plt.plot(webui_df["Timestamp"].values, webui_df["Value"].values)
    # plt.show()
    
    # --------------------------------
   
    # Now turn 1d float array into 2D np array
    dataset = webui_df["Value"]
    dataset = dataset.astype('float32')
    dataset = dataset.values.reshape(-1, 1)
    
    # Normalise dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    
    # Split dataset
    train, test = train_test_split(dataset, test_size=TEST_SET_SIZE, shuffle=False, random_state=SEED)
    print(len(train), len(test))
    
    # Shape into required sizes (to include look_back)
    trainX, trainY = create_dataset(train, LOOK_BACK)
    testX, testY = create_dataset(test, LOOK_BACK)
    
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    # Create and fit LSTM model
    model = Sequential()
    model.add(LSTM(50, input_shape=(1, LOOK_BACK), activation='relu'))
    model.add(Dense(50))
    model.add(Dense(1))
    
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=VERBOSITY)
    
    #azure_blob.load_blob_file("webui_lstm_model.keras")
    #model = load_model("webui_lstm_model.keras")
    
    # Inference
    train_predict = model.predict(trainX)
    test_predict = model.predict(testX)
    
    # Invert predictions
    train_predict = scaler.inverse_transform(train_predict)
    trainY = scaler.inverse_transform([trainY])
    test_predict = scaler.inverse_transform(test_predict)
    testY = scaler.inverse_transform([testY])
    
    # Calculate RMSE to evaluate model
    train_score = np.sqrt(mean_squared_error(trainY[0], train_predict[:,0]))
    print(f'Train Score: {round(train_score, 3)} RMSE')
    test_score = np.sqrt(mean_squared_error(testY[0], test_predict[:,0]))
    print(f'Test Score: {round(test_score, 3)} RMSE')
         
    #plot_predictions(dataset, train_predict, test_predict)
    
    model.save("webui_lstm_model.keras")
    azure_blob.upload_blob_file("webui_lstm_model.keras")