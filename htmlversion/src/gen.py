import json
import os


class Generator:

    def __init__(self, args):
        if len(args) not in (2, 3):
            print("Too many or no input file provided. Please provide one JSON date file for the generation (and optionnally one destination file).")
            exit()

        try:
            with open(args[1], "r") as file:
                content = file.read()
                self.data = json.loads(content)
        except Exception:
            print(f"File {args[1]} was not found or is corrupted. Please check your input file.")
            exit()

        self.dest = args[2] if len(args) == 3 else "./image.jpg"  # Setting curstom/default img file destination


    @staticmethod
    def generate_html(data):

        document = f"<!DOCTYPE html><head></head><body>"

        for i, element in enumerate(data):
            elem_type = element.get("type")
            content = element.get("content")
            name = element.get("name")
            value = element.get("value")

            # Coordinates and size are required arguments. If they do not exist the program will crash.
            coord = element["coordinates"]["x"], element["coordinates"]["y"]
            height, width = element["coordinates"]["height"], element["coordinates"]["width"]


            # We start filling the document from there
            document += f"<div style='position:absolute;left:{coord[0]}px;top:{coord[1]}px'><input id='{chr(65 + i)}' style='"

            if elem_type.lower() == "image":
                document += f"transform:scale({width},{height});transform-origin:top left' src='./cross.svg'"
            else:
                document += f"width:{width}px;height:{height}px' "

            document += f"type='{elem_type}' name='{name}'"

            # If 'value' exists: add field
            document += f" value='{value}'" if value else ""

            # If 'content' exists: add field
            document += f" content='{content}'" if content else ""

            # Set content as label for buttons lists (checkbox, radio)
            if elem_type.lower() in ("radio", "checkbox"):
                document += f"><label for='{chr(65 + i)}' style='font-family:sans-serif'>{content}</label"

            document += "></div>"

        document += "</body></html>"

        return document


    def generate_image(self, dest=None):
        html = Generator.generate_html(self.data)
        with open("tempfile.html", "w") as file: file.write(html)
        os.system(f"wkhtmltoimage tempfile.html {self.dest if dest is None else dest} --allow ./cross.svg -f jpg")
