import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join("data", "history.json")


def save_history(action, algorithm):
    entry = {
        "action": action,
        "algorithm": algorithm,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []
    except:
        data = []

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
    except:
        pass

    return []
