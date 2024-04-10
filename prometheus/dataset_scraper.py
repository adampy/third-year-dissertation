from datetime import datetime
from os import listdir
from pod_data import PodData
from matplotlib import pyplot as plt

URL = "http://20.26.238.197:30900/"
START_TIME = datetime(2024, 4, 10, 21, 53, 0)
END_TIME = datetime(2024, 4, 10, 23, 24, 0)
QUERY = 'sum(rate(container_cpu_usage_seconds_total{pod=~"teastore.*|limbo.*"}[5m])) by (pod)' #'sum(rate(container_cpu_usage_seconds_total{pod!=""}[5m]))by(pod)'
EXPERIMENT = "lp_b200_e200_s7200_r3_sa70_sp3600"

def save_results(url, query, start_time, end_time, experiment_name):
    # Query data from Prometheus
    data = PodData.from_query_range(url, query, start_time, end_time, 15)
    
    # Now save all to csv
    for pod in data:
        pod.save_to_csv(f"results/{experiment_name}/{pod.name}.csv")
        
def load_results(experiment_name):
    # Find all pods in directory
    pods = listdir(f"results/{experiment_name}")
    
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
    save_results(URL, QUERY, START_TIME, END_TIME, EXPERIMENT)
    results = load_results(EXPERIMENT)
    plot_results(results)
    
    
    # plot all webui from experiment
    # data = load_results(EXPERIMENT)
    # for pod in data:
    #     if "webui" in pod.name:
    #         df = pod.as_df()
    #         plt.plot(df["Timestamp"].values, df["Value"].values, label=pod.name)
    # plt.legend()
    # plt.show()