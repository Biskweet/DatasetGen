import json
import random


posx = random.randint(0, 1920)
posy = random.randint(0, 1080)
sizex = random.randint(0, 60)
sizey = random.randint(0, 60)


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

        # If 'value' exists add field
        document += f" value='{value}'" if value else ""

        # If 'content' exists add field
        document += f" content='{content}'" if content else ""

        if elem_type.lower() in ("radio", "checkbox"):
            document += f"><label for='{chr(65 + i)}' style='font-family:sans-serif'>{content}</label"

        document += "></div>"

    document += "</body></html>"

    return document


html = generate_html(
    [
        {
            "content": "LETSOGGGG",
            "value": "Weee",
            "name": "bouton",
            "type": "button",
            "coordinates": {"x": 500, "y": 100, "width": 200, "height": 100}
        },
        # {
        #     ""
        # }
    ]
)

with open("res.html", "w") as f: f.write(html)
print("Done")
