import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do projeto

def build_path(*args):
    return os.path.join(BASE_DIR, 'data', *args)
