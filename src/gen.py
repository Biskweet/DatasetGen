import json


class Generator:
    def __init__(self, args):
        if len(args) not in (2, 3):
            print("Too many or no input file provided. Please provide one JSON date file for the generation (and optionnally one destination file).")
            exit()

        try:
            with open(args[1], "r") as file:
                content = file.read()
                self.data = json.loads(content)
        except:
            print(f"File {args[1]} was not found or is corrupted. Please check your input file.")
            exit()

        self.dest = args[2] if len(args) == 3 else "./image.png"


    @staticmethod
    def generate_html(data):
        document = "<!DOCTYPE html><head></head><body>"

        for element in data:
            document += f'<input name="{element["name"]}" ' \
                        f'type="{element["type"]}" '        \
                        f'style="position:absolute;left:{element["coordinates"]["x"]};top:{element["coordinates"]["y"]}"'

            if element.get("value"):
                document += f' value="{element["value"]}"'

            if element.get(""):
                ...


    def generate_image(self):
        html = Generator.generate_html(self.data)
