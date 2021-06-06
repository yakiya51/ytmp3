import os
from tkinter import messagebox

def full_path(relative_path):
    base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def get_default_path():
    with open(full_path('dependencies/default_path.txt'), 'r') as path_file:
        path = path_file.readline()
        path_file.close()
    return path

def set_default_path(new_path):
    with open(full_path('dependencies/default_path.txt'), 'w') as path_file:
        path_file.write(new_path)
        path_file.close()
