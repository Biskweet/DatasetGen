import json
import os
import random
import threading

import cv2 as cv
import numpy as np

from PIL import Image

# Custom import
from . import utils


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
        "textarea",     # 8
        "textbox"       # 9
    ]


    def __init__(self, jsons):
        self.data = [j[1] for j in jsons]


    @staticmethod
    def get_random_image(etype):
        category = Generator.input_types.index(etype)
        file = random.choice(os.listdir(f"src/elements/{category}/"))

        try:
            img = cv.imread(f"src/elements/{category}/{file}")  # type: ignore

        except Exception:
            print(f"Could not open image file: elements/{category}/{file}")
            raise SystemExit("Aborting")

        return img


    @staticmethod
    def generate_dataset(size):
        """
        Goes through 3 main steps:
            (1) Generates random data in JSON format and writes down in files
            (2) Reads the JSON files and generates its corresponding images under same names
            (3) Reads back the images and calculates the label for each one of them
        """
        json_list = Generator.generate_json(size)

        app = Generator(json_list)

        app.generate_multiple_images()
        app.generate_labels()

        app.organize_dataset()

        print("\nEnd.\n")


    @staticmethod
    def generate_json(amount, lower_elem_bound=1, upper_elem_bound=10, xmax=500, ymax=500, dimmin=10, dimmax=200):
        jsons = []

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

                elements["data"].append({
                    "type": elem_type,
                    "value": "value",
                    "name": "name",
                    # "content": content,
                    "coord": {"x": posx, "y": posy, "w": width, "h": height}
                })

            file = str(i).zfill(len(str(amount))) + ".json"

            with open(f"./jsons/{file}", "w") as file:
                json.dump(elements, file)

            jsons.append(("./jsons/{file}", elements))

            print(f"\rGenerating {i+1}/{amount} JSON files.", end=" ")

        print("Done.")

        return jsons


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

            # Overwriting canvas at given subpixel (=sublist) with element
            canvas[coord[1]:coord[1] + elem.shape[0], coord[0]:coord[0] + elem.shape[1]] = elem

        return canvas


    def generate_multiple_images(self):
        """
        Create N threads with N sublists of the dataset, each running
        `Generator.generate_image`. `processed_count` is used as a hack for
        sharing a common variable between them.
        """

        # Creating 10 threads to generate data faster
        no_of_threads = 10
        threads = [ ]

        assigned = 0
        processed_count = 0

        def image_generation_thread(starting_point, amount):
            nonlocal processed_count

            for i in range(starting_point, starting_point + amount):
                img = Generator.generate_image(self.data[i])
                filename = str(i).zfill(len(str(len(self.data))))

                cv.imwrite(f"./images/{filename}.jpg", img)  # type: ignore

                processed_count += 1
                print(f"\rGenerating {processed_count}/{len(self.data)} images.", end=" ")


        for i in range(no_of_threads):
            chunk_size = len(self.data) // no_of_threads + (i >= (no_of_threads - len(self.data) % no_of_threads))

            # print("chunk =", assigned, "+", chunk_size)

            threads.append(
                threading.Thread(target=image_generation_thread, args=(assigned, chunk_size))
            )

            assigned += chunk_size


        # for sublist in np.array_split(self.data, no_of_threads):
        #     threads.append(threading.Thread(target=self.image_generation_thread, args=(sublist, assigned, processed_count)))
        #     assigned += len(sublist)

        # Starting all threads
        for thread in threads:
            thread.start()

        # Waiting for all threads
        for thread in threads:
            thread.join()

        print("Done.")


    def generate_labels(self):
        for i, page in enumerate(self.data):
            page_data = page["data"]
            filename = str(i).zfill(len(str(len(self.data))))

            img = Image.open(f"./images/{filename}.jpg")

            for elem in page_data:
                category_id = Generator.input_types.index(elem["type"])
                width = elem["coord"]["w"] / img.width
                height = elem["coord"]["h"] / img.height
                center_x = (elem["coord"]["x"] + (elem["coord"]["w"] / 2)) / img.width
                center_y = (elem["coord"]["y"] + (elem["coord"]["h"] / 2)) / img.height

                center_x = min(1, center_x)
                center_y = min(1, center_y)

                with open(f"./labels/{filename}.txt", "w") as file:
                    file.write(f"{category_id} {center_x} {center_y} {width} {height}\n")

            print(f"\rGenerating {i+1}/{len(self.data)} labels.", end=" ")

        print("Done.")


    def organize_dataset(self):
        extensions = ("json", "jpg", "txt")

        for i, folder in enumerate(("jsons", "images", "labels")):
            os.mkdir(folder + "/train")
            os.mkdir(folder + "/val")
            os.mkdir(folder + "/test")

            for j in range(len(self.data)):
                filename = str(j).zfill(len(str(len(self.data))))

                if j / len(self.data) < utils.TRAIN_RATIO:
                    subfolder = "train"
                elif j / len(self.data) < utils.TRAIN_RATIO + utils.VAL_RATIO:
                    subfolder = "val"
                else:
                    subfolder = "test"

                os.rename(f"{folder}/{filename}.{extensions[i]}",
                          f"{folder}/{subfolder}/{filename}.{extensions[i]}")

                print(f"\rOrganizing file {j + 1 + i * len(self.data)}/{3 * len(self.data)}.", end=" ")

        print("Done.")
