import json
import os
import random
import threading
import time

import cv2 as cv
import numpy as np

from PIL import Image

# Custom import
from . import utils

# Creating white canvas
img = np.full((3, 3, 3), 255)

class Generator:
    input_types = [     # index
        "button",       # 0
        "checkbox",     # 1
        "image",        # 2
        "label",        # 3
        "link",         # 4
        "paragraph",    # 5
        "radio",        # 6
        "select",       # 7
        "textarea",     # 7
        "textbox"       # 8
    ]


    def __init__(self, args):
        if len(args) not in (3, 4) and args[1] != "multiple":
            print("Too many or no input file provided. Please provide one JSON \
                  data file for the generation (and optionally one destination file).")
            raise SystemExit("Aborting.")


        # Single file generation
        if (args[1] == "single"):
            try:
                with open(args[2], "r") as file:
                    content = file.read()
                    self.data = json.loads(content)
            except Exception as e:
                print("File", args[2], "was not found, has wrong data format or \
                       is corrupted. Please check your input file.", e)
                raise SystemExit("Aborting.")

        # Multiple file generation
        elif (args[1] == "multiple"):
            self.data = []
            try:
                for file in args[2:]:
                    with open(file, "r") as f:
                        content = f.read()
                        self.data.append(json.loads(content))
            except Exception:
                print("File was not found, has wrong data format or is \
                       corrupted. Please check your input files.")
                raise SystemExit("Aborting.")

        # Setting img file destination with custom/default
        # Trimming the destination file name to remove the extension
        self.dest = args[3].split('.')[0] if (len(args) == 4 and args[1] == "single") else "./image"


    @staticmethod
    def get_random_image(etype):
        category = Generator.input_types.index(etype)
        file = random.choice(os.listdir(f"src/elements/{category}/"))

        try:
            img = cv.imread(f"src/elements/{category}/{file}") # type: ignore
        except Exception:
            print(f"Could not open image file elements/{category}/{file}")
            raise SystemExit("Aborting")

        return img


    @staticmethod
    def generate_json(amount, lower_elem_bound=1, upper_elem_bound=10, xmax=500, ymax=500, dimmin=10, dimmax=200):
        for i in range(amount):
            elements = {"data": []}
            nbelem = random.randint(lower_elem_bound, upper_elem_bound)

            for _ in range(nbelem):
                # Generating valid, non-overlapping dimensions for each element
                elem_type = random.choice(Generator.input_types)

                # Generating base random data
                width, height, posx, posy = utils.generate_random(elem_type, dimmin, dimmax, xmax, ymax)

                while utils.has_collision(posx, posy, width, height, elements["data"]):
                    width, height, posx, posy = utils.generate_random(elem_type, dimmin, dimmax, xmax, ymax)

                # if elem_type == "paragraph":
                #     content = utils.generate_text_content()
                # elif elem_type == "button":
                #     content = utils.generate_text_content(length=random.randint(1, 3))
                # else:
                #     content = "content"


                elements["data"].append({
                    "type": elem_type,
                    "value": "value",
                    "name": "name",
                    # "content": content,
                    "coord": {"x": posx, "y": posy, "w": width, "h": height}
                })

            with open(f"./jsons/{str(i).zfill(len(str(amount)))}.json", "w") as file:
                json.dump(elements, file)

            print(f"Generated {i+1}/{amount} JSON files.", end="\r")

        print()


    @staticmethod
    def generate_image(data):
        data = data.get("data")

        if data is None:
            print("Incorrect input")
            raise SystemExit("Aborting.")

        # Creating white canvas
        canvas_h, canvas_w = utils.get_max_coord(data)
        canvas = np.full((canvas_w, canvas_h, 3), 255)

        # Filling canvas with each element
        for element in data:
            etype = element.get("type")
            # content = data.get("content")

            # coord and size are checked in `get_max_coord`
            coord = element["coord"]["x"], element["coord"]["y"]
            width = element["coord"]["w"]
            height = element["coord"]["h"]

            elem = Generator.get_random_image(etype)

            if etype is None:
                print("Data is corrupt.")
                raise SystemExit("Aborting.")


            elem = cv.resize(elem, (width, height), interpolation=cv.INTER_AREA)  # type: ignore

            # Overwriting canvas at given location with element
            canvas[coord[1]:coord[1] + elem.shape[0], coord[0]:coord[0] + elem.shape[1]] = elem

        return canvas


    @staticmethod
    def generate_dataset(size):
        Generator.generate_json(size)

        args = [None,"multiple"]
        args += list(map(lambda filename: "./jsons/" + filename, sorted(os.listdir("./jsons/"))))

        app = Generator(args)
        app.generate_multiple_images()
        app.generate_labels()

        print("\n\nDone.")


    def generate_multiple_images(self):
        # Creating N threads to generate data faster
        threads = []
        
        # cpu_count = psutil.cpu_count(logical=False)
        no_of_threads = 10
        reserved = 0
        processed_count = [0]
        for sublist in np.array_split(self.data, no_of_threads):
            threads.append(threading.Thread(target=self.image_generation_thread, args=(sublist, reserved, processed_count)))
            reserved += len(sublist)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        print()


    def image_generation_thread(self, sublist, reserved, processed_count):
        for i, page in enumerate(sublist):
            img = Generator.generate_image(page)
            filename = str(reserved + i).zfill(len(str(len(self.data))))
            cv.imwrite(f"./images/{filename}.jpg", img)  # type: ignore

            processed_count[0] += 1
            print(f"\rGenerated {processed_count[0]}/{len(self.data)} images.", end=" ")


    def generate_labels(self):
        for i, page in enumerate(self.data):
            page_data = page["data"]
            filename = str(i).zfill(len(str(len(self.data))))

            with open(f"./labels/{filename}.txt", "w") as file:
                img = Image.open(f"./images/{filename}.jpg")

                for elem in page_data:
                    category_id = Generator.input_types.index(elem["type"])
                    width = elem["coord"]["w"] / img.width
                    height = elem["coord"]["h"] / img.height
                    center_x = (elem["coord"]["x"] + (elem["coord"]["w"] / 2)) / img.width
                    center_y = (elem["coord"]["y"] + (elem["coord"]["h"] / 2)) / img.height

                    center_x = min(1, center_x)
                    center_y = min(1, center_y)

                    file.write(f"{category_id} {center_x} {center_y} {width} {height}\n")

            print(f"\rGenerated {i+1}/{len(self.data)} labels.", end=" ")




