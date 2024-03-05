from datetime import datetime
from dataclasses import dataclass
import matplotlib.pyplot as plt
import csv
import pandas as pd
import requests


@dataclass
class PodData:
    name: str
    data: list[list[int | float]] # List of [timestamp, value]

    def plot(self, start_date: datetime | None = None, end_date: datetime | None = None):
        if start_date is None:
            start_date = datetime.fromtimestamp(self.data[0][0])
        if end_date is None:
            end_date = datetime.fromtimestamp(self.data[-1][0])

        timestamps = [datetime.fromtimestamp(x[0]) for x in self.data if x[0] >= start_date.timestamp() and x[0] <= end_date.timestamp()]
        values = [float(x[1]) for x in self.data if x[0] >= start_date.timestamp() and x[0] <= end_date.timestamp()]
        
        plt.plot(timestamps, values)
        plt.title(f"CPU Usage for {self.name}")
        plt.xlabel("Time")
        plt.ylabel("CPU Usage")
        plt.show()

    def as_df(self, start_date: datetime | None = None, end_date: datetime | None = None) -> pd.DataFrame:
        if start_date is None:
            start_date = datetime.fromtimestamp(self.data[0][0])
        if end_date is None:
            end_date = datetime.fromtimestamp(self.data[-1][0])

        timestamps = [datetime.fromtimestamp(x[0]) for x in self.data if x[0] >= start_date.timestamp() and x[0] <= end_date.timestamp()]
        values = [float(x[1]) for x in self.data if x[0] >= start_date.timestamp() and x[0] <= end_date.timestamp()]
        
        return pd.DataFrame({"Timestamp": timestamps, "Value": values})
        
    def save_to_csv(self, filename: str):
        with open(filename, "w", newline="\n") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Value"])
            writer.writerows(self.data)
                
    @classmethod
    def from_csv(cls, filename: str):
        with open(filename, "r") as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            data = [[int(row[0]), float(row[1])] for row in reader if row]
            return cls(filename, data)
        
    @classmethod
    def from_query_range(cls, base_url: str, query: str, start: datetime, end: datetime, step: int) -> list['PodData']:
        # Send reqeust to Prometheus
        response = requests.get(base_url + "/api/v1/query_range", params={
            "query": query,
            "start": start.timestamp(),
            "end": end.timestamp(),
            "step": step
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