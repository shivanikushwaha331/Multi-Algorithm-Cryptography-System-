import json

def load_metadata():
    with open("data/algorithm_metadata.json", "r") as f:
        return json.load(f)


def analyze_algorithm(algo):
    data = load_metadata()
    return data.get(algo, "No data available")