from datetime import datetime
import pandas as pd
from pod_data import PodData

URL = "http://172.187.146.126:31767"
START_TIME = datetime(2024, 3, 4, 15, 0, 0)
END_TIME = datetime(2024, 3, 4, 18, 15, 0)
QUERY = 'sum(rate(container_cpu_usage_seconds_total{pod!=""}[5m]))by(pod)'

if __name__ == "__main__":
    # Open from file
    webui = PodData.from_csv("webui-05032024.csv")
    
    # Or get from Prometheus
    #data = PodData.from_query_range(URL, QUERY, START_TIME, END_TIME, 15)
    #webui = [pod for pod in data if 'webui' in pod.name][0]
    
    # Plot data
    start_date = datetime(2024, 3, 4, 16, 15, 0)
    end_date = datetime(2024, 3, 4, 18, 0, 0)
    #webui.plot(start_date=start_date, end_date=end_date)
    print(webui.as_df(start_date=start_date, end_date=end_date))
    # Save to file
    #webui.save_to_csv(f"{webui.name}.csv")