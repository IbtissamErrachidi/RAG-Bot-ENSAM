import shutil
import os

def clear_output_folder(folder_path='infos_txt'):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)

