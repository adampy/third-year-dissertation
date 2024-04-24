from matplotlib import pyplot as plt
from dataset_scraper import load_results
import pandas as pd

EXPERIMENT = "lp_b150_e150_s7200_r30_sa100_sp1800"
#SERVICES = ["auth", "db", "image", "persistence", "recommender", "registry", "webui"]
SERVICES = ["auth", "image", "persistence", "recommender", "webui"]
SERVICE_CPU_LIMITS = {
    "auth": 500,
    "db": 800,
    "image": 500,
    "persistence": 500,
    "recommender": 200,
    "webui": 900,
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

def get_results_by_service(experiment) -> dict[str, list['PodData']]:
    data = load_results(experiment)
    data_by_service = {service: [] for service in SERVICES}
    for pod in data:
        if any(service in pod.name for service in SERVICES) == False: continue # Exluce other services
        data_by_service[pod.name.split("-")[1]].append(pod)
    return data_by_service

if __name__ == "__main__":
    # Plot each service, we need to first group them
    data_by_service = get_results_by_service(EXPERIMENT)
        
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

        # Calculate the  evaluation metrics (under and over provisioning accuracy and timeshare)
        combined_df["Total"] = total_cpu_usage["Value"]
        combined_df["Overprov"] = combined_df["Total"] - combined_df["Value"]
        #ax.plot(combined_df["Timestamp"].values, combined_df["Overprov"].values, label="Overprovisioning")
        ax.legend()

        accuracy_O = combined_df["Value"].sum() / len(combined_df)
        accuracy_U = -combined_df[combined_df["Value"] < 0]["Value"].sum() / len(combined_df)
        timeshare_O = len(combined_df[combined_df["Value"] > 0]) / len(combined_df)
        timeshare_U = len(combined_df[combined_df["Value"] < 0]) / len(combined_df)

        # combined total cpu usage into combined_df
        print(f"{EXPERIMENT}/{service} | Accuracy_U: {accuracy_U} | Accuracy_O: {accuracy_O} | Timeshare_U: {timeshare_U} | Timeshare_O: {timeshare_O}")

    # Finally show all plots
    plt.show()