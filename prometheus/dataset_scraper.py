from datetime import datetime
from os import listdir
from pod_data import PodData
from matplotlib import pyplot as plt

URL = "http://20.26.238.197:30900/"
START_TIME = datetime(2024, 3, 21, 21, 58, 0)
END_TIME = datetime(2024, 3, 21, 22, 58, 0)
QUERY = 'sum(rate(container_cpu_usage_seconds_total{pod=~"teastore.*|limbo.*"}[5m])) by (pod)' #'sum(rate(container_cpu_usage_seconds_total{pod!=""}[5m]))by(pod)'
EXPERIMENT = "lp_c100_s900_r4"

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
        plt.legend()
    plt.show()

if __name__ == "__main__":
    results = load_results()
    plot_results(results)
    