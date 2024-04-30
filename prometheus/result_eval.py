from matplotlib import pyplot as plt
from dataset_scraper import load_results
import pandas as pd

EXPERIMENT = "ppah1e100_lp_b150_e400_s7200_r5_sa15_sp300"
SERVICES = ["auth", "image", "persistence", "recommender", "webui"]
SERVICE_CPU_LIMITS = {
    "auth": 500,
    "image": 500,
    "persistence": 500,
    "recommender": 200,
    "webui": 900,
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

def calculate_effective_cost(combined_df, vm_cost_per_hour, vcpu_per_node, interval):
    vcpu_cost_per_hour = vm_cost_per_hour / vcpu_per_node
    vcpu_cost_per_interval = interval * vcpu_cost_per_hour / 3600
    effective_cost = combined_df["Total"].sum() * vcpu_cost_per_interval
    return effective_cost

if __name__ == "__main__":
    # Plot each service, we need to first group them
    data_by_service = get_results_by_service(EXPERIMENT)
        
    # Now plot all services in subplots
    overall_avg_pod_lifetime = 0
    overall_number_of_pods = 0
    for service, pods in data_by_service.items():
        # Combine dataframes
        fig, ax = plt.subplots()
        pod_dfs = [pod.as_df() for pod in pods]
        combined_df = sum_into_combined_df(pod_dfs)
        total_cpu_usage = plot_total_cpu_usage(pod_dfs, SERVICE_CPU_LIMITS[service])
        
        # Plot each pod
        # for pod_df in pod_dfs:
        #     ax.plot(pod_df["Timestamp"].values, pod_df["Value"].values)
            
        # Plot combined and total cpu usage
        experiment_start_time = combined_df["Timestamp"].values[0]
        adjusted_combined_timestamps = (combined_df["Timestamp"].values - experiment_start_time) / (1000 * 1000 * 1000)
        adjusted_total_cpu_timestamps = (total_cpu_usage["Timestamp"].values - experiment_start_time) / (1000 * 1000 * 1000)
        
        ax.plot(adjusted_combined_timestamps, combined_df["Value"].values, label="Total vCPU usage")
        ax.plot(adjusted_total_cpu_timestamps, total_cpu_usage["Value"].values, label="Allocated vCPU capacity")
        ax.set_title(f"Usage vs Allocated ({service})")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("vCPU (cores)")

        # Calculate the  evaluation metrics (under and over provisioning accuracy and timeshare)
        combined_df["Total"] = total_cpu_usage["Value"]
        combined_df["Overprov"] = combined_df["Total"] - combined_df["Value"]
        #ax.plot(combined_df["Timestamp"].values, combined_df["Overprov"].values, label="Overprovisioning")
        ax.legend(loc="upper right")

        accuracy_O = combined_df["Value"].sum() / len(combined_df)
        accuracy_U = -combined_df[combined_df["Value"] < 0]["Value"].sum() / len(combined_df)
        timeshare_O = len(combined_df[combined_df["Value"] > 0]) / len(combined_df)
        timeshare_U = len(combined_df[combined_df["Value"] < 0]) / len(combined_df)

        # Calculate effective cost (in pence)
        effective_cost = calculate_effective_cost(combined_df, 0.0652 * 100, 2, 15)

        # Calculate the max number of pods and average pod lifetime
        max_pods = total_cpu_usage["Value"].max() / (SERVICE_CPU_LIMITS[service] / 1000) # Convert from millicores
        max_pods = round(max_pods)
        avg_pod_lifetime = 0
        for pod in pod_dfs:
            # Add to local service avg
            pod_lifetime = (pod["Timestamp"].max() - pod["Timestamp"].min()).total_seconds()
            avg_pod_lifetime += pod_lifetime
            
            # And add to global avg
            overall_avg_pod_lifetime += pod_lifetime
            overall_number_of_pods += 1
            
        avg_pod_lifetime /= len(pod_dfs)
        avg_pod_lifetime = round(avg_pod_lifetime / 60, 2)

        #print(f"{EXPERIMENT}/{service} | Accuracy_U: {accuracy_U} | Accuracy_O: {accuracy_O} | Timeshare_U: {timeshare_U} | Timeshare_O: {timeshare_O} | | Effective cost: {round(effective_total_cpu, 2)}p")
        print(f"{EXPERIMENT}/{service} | Accuracy_O: {accuracy_O} | Effective cost: {round(effective_cost, 2)}p | Max no. of pods: {max_pods} | Avg pod lifetime: {avg_pod_lifetime}mins")

    print(f"Average pod lifetime: {round((overall_avg_pod_lifetime / overall_number_of_pods) / 60, 2)}mins")

    # Finally show all plots
    plt.show()