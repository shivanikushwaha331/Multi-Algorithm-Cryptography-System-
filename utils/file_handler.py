def read_file(file):
    return file.read().decode()

def save_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)