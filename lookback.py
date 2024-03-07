# Store lookback file in the following format
# {
#     "stored_pods": ["teastore-webui-654cffc85f-p5x86"],
#     "teastore-webui-654cffc85f-p5x86": {
#         "lookback": {
#             "window": 10,
#             "data": [0.1, 0.1, 0.1, 0.1 ,0.1, 0.1, 0.1, 0.1, 0.1, 0.1] // 0th element is earliest
#         }
#     }
# }

import json

class LookbackDataNotFoundError(Exception):
    pass

def make_file_if_not_exists():
    try:
        with open("lookback.json", "r") as f:
            pass
    except FileNotFoundError:
        with open("lookback.json", "w") as f:
            f.write(json.dumps({"stored_pods": []}))

def get_all():
    make_file_if_not_exists()
    with open("lookback.json", "r") as f:
        return json.loads(f.read())
    
def get_pod(pod_name):
    data = get_all()
    if pod_name not in data["stored_pods"]:
        raise LookbackDataNotFoundError(f"Lookback data for pod {pod_name} not found")
    return data[pod_name]

def append_window(pod_name, new_data, window):
    data = get_all()

    # If pod not found in data, we add a 0 window
    if pod_name not in data["stored_pods"]:
        data = zero(pod_name, window) # Zero out the rest of the window

    #Now we need to append after popping the first element
    data[pod_name]["lookback"]["data"].pop(0)
    data[pod_name]["lookback"]["data"].append(new_data)

    with open("lookback.json", "w") as f:
        f.write(json.dumps(data))

def zero(pod_name, window): # RETURNS DATA BACK
    data = get_all()
    if pod_name in data["stored_pods"]:
        raise ValueError(f"Pod {pod_name} already exists in lookback data")
    
    data["stored_pods"].append(pod_name)
    data[pod_name] = {
        "lookback": {
            "window": window,
            "data": [0 for _ in range(window)]
        }
    }
    with open("lookback.json", "w") as f:
        f.write(json.dumps(data))

    return data

def remove(pod_name):
    data = get_all()
    if pod_name not in data["stored_pods"]:
        raise LookbackDataNotFoundError(f"Lookback data for pod {pod_name} not found")
    
    data["stored_pods"].remove(pod_name)
    del data[pod_name]
    with open("lookback.json", "w") as f:
        f.write(json.dumps(data))