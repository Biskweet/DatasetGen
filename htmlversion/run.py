import sys
import shutil
import os
from src.gen import Generator

if __name__ == "__main__":
    # Creating necessary folders
    for directory in ("./jsons/", "./htmls/", "./images/"):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    if len(sys.argv) < 2 or sys.argv[1] not in ("generate-dataset", "generate-json", "single", "multiple", "clearall"):
        raise SystemExit("Please select a valid command.")

    # Random generation
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        # Complete A to Z dataset 
        if sys.argv[1] == "generate-dataset":
            Generator.generate_dataset(int(sys.argv[2]))

        # JSON only
        if sys.argv[1] == "generate-json":
            Generator.generate_json(int(sys.argv[2]))

    else:
        # HTML to JPG generation
        if sys.argv[1] == "single":
            app = Generator(sys.argv)
            app.generate_image()

        elif sys.argv[1] == "multiple":
            app = Generator(sys.argv)
            app.generate_multiple_images()

        elif sys.argv[1] == "clearall":
            try:
                shutil.rmtree("./jsons/")
                shutil.rmtree("./htmls/")
                shutil.rmtree("./images/")
            except Exception: ...

        else:
            print("Please provide arguments.")
