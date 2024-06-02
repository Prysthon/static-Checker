# utils.py

def read_file(file_path):
    with open(f'{file_path}.241', 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
