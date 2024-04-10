from datetime import datetime
from os import listdir
from pod_data import PodData
from matplotlib import pyplot as plt

URL = "http://20.26.238.197:30900/"
START_TIME = datetime(2024, 3, 22, 16, 52, 0)
END_TIME = datetime(2024, 3, 22, 21, 25, 0)
QUERY = 'sum(rate(container_cpu_usage_seconds_total{pod=~"teastore.*|limbo.*"}[5m])) by (pod)' #'sum(rate(container_cpu_usage_seconds_total{pod!=""}[5m]))by(pod)'
EXPERIMENT = "lp_b100_e100_s7200_r3_sa70_sp3600"

def save_results():
    # Query data from Prometheus
    data = PodData.from_query_range(URL, QUERY, START_TIME, END_TIME, 15)
    
    # Now save all to csv
    for pod in data:
        pod.save_to_csv(f"results/{EXPERIMENT}/{pod.name}.csv")
        
def load_results():
    # Find all pods in directory
    pods = listdir(f"results/{EXPERIMENT}")
    
    # Then load them into data
    data = []
    for pod in pods:
        data.append(PodData.from_csv(f"results/{EXPERIMENT}/{pod}"))
    return data

def plot_results(data):
    # Combine all data into one plot
    for pod in data:
        df = pod.as_df()
        plt.plot(df["Timestamp"].values, df["Value"].values, label=pod.name)
        #plt.legend()
    plt.show()

if __name__ == "__main__":
    #save_results()
    #results = load_results()
    #plot_results(results)
    
    
    # plot all webui from experiment
    data = load_results()
    for pod in data:
        if "limbo" in pod.name:
            df = pod.as_df()
            plt.plot(df["Timestamp"].values, df["Value"].values, label=pod.name)
    plt.legend()
    plt.show()