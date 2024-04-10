from datetime import datetime
from os import listdir
from pod_data import PodData
from matplotlib import pyplot as plt
from dataset_scraper import save_results, load_results, plot_results
import pandas as pd

EXPERIMENT = "lp_b100_e100_s7200_r3_sa70_sp3600"
SERVICES = ["auth", "db", "image", "persistence", "recommender", "registry", "webui"]
SERVICE_CPU_LIMITS = {
    "auth": 800,
    "db": 800,
    "image": 1000,
    "persistence": 800,
    "recommender": 600,
    "webui": 1000,
    "registry": 800,
}

def sum_into_combined_df(dfs):
    combined = {} # Timestamp to value
    for df in dfs:
        for i, row in df.iterrows():
            if row["Timestamp"] not in combined:
                combined[row["Timestamp"]] = row["Value"]
            else:
                combined[row["Timestamp"]] += row["Value"]
    
    combined_df = pd.DataFrame({"Timestamp": list(combined.keys()), "Value": list(combined.values())})
    combined_df.sort_values(by="Timestamp", inplace=True)
    return combined_df

def plot_total_cpu_usage(dfs, service_usage):
    combined = {} # Timestamp to value
    for df in dfs:
        for i, row in df.iterrows():
            if row["Timestamp"] not in combined:
                combined[row["Timestamp"]] = service_usage / 1000
            else:
                combined[row["Timestamp"]] += service_usage / 1000
    
    combined_df = pd.DataFrame({"Timestamp": list(combined.keys()), "Value": list(combined.values())})
    combined_df.sort_values(by="Timestamp", inplace=True)
    return combined_df

if __name__ == "__main__":
    # Plot each service, we need to first group them
    data = load_results(EXPERIMENT)
    data_by_service = {service: [] for service in SERVICES}
    for pod in data:
        if "limbo" in pod.name: continue
        data_by_service[pod.name.split("-")[1]].append(pod)
        
    # Now plot all services in subplots
    for service, pods in data_by_service.items():
        # Combine dataframes
        fig, ax = plt.subplots()
        pod_dfs = [pod.as_df() for pod in pods]
        combined_df = sum_into_combined_df(pod_dfs)
        total_cpu_usage = plot_total_cpu_usage(pod_dfs, SERVICE_CPU_LIMITS[service])
        
        # Plot each pod
        for pod_df in pod_dfs:
            ax.plot(pod_df["Timestamp"].values, pod_df["Value"].values)
            
        # Plot combined and total cpu usage
        ax.plot(combined_df["Timestamp"].values, combined_df["Value"].values, label="Combined")
        ax.plot(total_cpu_usage["Timestamp"].values, total_cpu_usage["Value"].values, label="Total CPU Usage")
        ax.set_title(service)
        ax.legend()

    # Finally show all plots
    plt.show()