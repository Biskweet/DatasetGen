import sys
import shutil
import os
from src.gen import Generator


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("dataset", "clean"):
        raise SystemExit("Please select a valid command.")

    # Generating dataset of size N = `sys.argv[2]`
    if len(sys.argv) > 2 and sys.argv[1] == "dataset" and sys.argv[2].isdigit():
        os.system("python run.py clean")  # Cleaning

        # Creating necessary directories
        for directory in ("./jsons/", "./images/", "./labels/"):
            if not os.path.isdir(directory):
                os.mkdir(directory)

        size = int(sys.argv[2])
        Generator.generate_dataset(size)


    elif sys.argv[1] == "clean":
        for folder in ("./jsons/", "./images/", "./labels/", "./src/__pycache__/"):
            try:
                shutil.rmtree(folder)
            except Exception: ...  # Ignoring `rm` errors (i.e. non-existing directory)
