import datetime
import requests
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Union

URL = "http://172.187.146.126:31767"
START_TIME = datetime.datetime(2024, 3, 4, 15, 0, 0)
END_TIME = datetime.datetime(2024, 3, 4, 18, 15, 0)
QUERY = 'sum(rate(container_cpu_usage_seconds_total{pod!=""}[5m]))by(pod)'

@dataclass
class PodData:
    name: str
    data: list[list[Union[int, float]]] # List of [timestamp, value]

    def plot(self):
        timestamps = [datetime.datetime.fromtimestamp(x[0]) for x in self.data]
        values = [float(x[1]) for x in self.data]
        
        plt.plot(timestamps, values)
        plt.title(f"CPU Usage for {self.name}")
        plt.xlabel("Time")
        plt.ylabel("CPU Usage")
        plt.show()

def get_data(query: str) -> list[PodData]:
    # Send reqeust to Prometheus
    response = requests.get(URL + "/api/v1/query_range", params={
        "query": QUERY,
        "start": START_TIME.timestamp(),
        "end": END_TIME.timestamp(),
        "step": 15
    })
    data = response.json()
    
    # First check for error
    if data['status'] != 'success':
        raise ValueError(data['error'])
    
    # Now parse into PodData
    pods = data['data']['result']
    pod_data = []
    for pod in pods:
        name = pod['metric']['pod']
        values = pod['values']
        pod_data.append(PodData(name, values))
    
    return pod_data

if __name__ == "__main__":
    data = get_data(QUERY)
    webui = [pod for pod in data if 'webui' in pod.name][0]
    webui.plot()