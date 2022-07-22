import random


WORDS = [
    "dolorem",    "natus",         "consequatur", "modi",
    "ea",         "aut",           "nesciunt",    "dolore",
    "eum",        "dicta",         "veniam",      "iure",
    "totam",      "nisi",          "laudantium",  "nulla",
    "ipsum",      "corporis",      "omnis",       "ratione",
    "dolores",    "perspiciatis",  "ipsa",        "velit",
    "quae",       "reprehenderit", "et",          "aperiam",
    "commodi",    "sequi",         "quasi",       "sed",
    "magni",      "consequuntur",  "sunt",        "fugit",
    "ut",         "illum",         "accusantium", "ad",
    "architecto", "error",         "pariatur",    "in",
    "nostrum",    "doloremque",    "aliquid",     "laboriosam",
    "magnam",     "est",           "tempora",     "consectetur",
    "vitae",      "incidunt",      "quam",        "aliquam",
    "ex",         "aspernatur",    "voluptatem",  "voluptate",
    "porro",      "beatae",        "explicabo",   "exercitationem",
    "eius",       "quia",          "eos",         "suscipit",
    "nemo",       "qui",           "quis",        "quaerat",
    "fugiat",     "minima",        "inventore",   "amet",
    "labore",     "illo",          "unde",        "esse",
    "eaque",      "molestiae",     "quisquam",    "vel",
    "ullam",      "non",           "ab",          "numquam",
    "dolor",      "odit",          "voluptas",    "enim",
    "veritatis",  "iste",          "adipisci",    "autem",
    "quo",        "ipsam",         "sit",         "rem",
    "nihil",      "neque"
]


FONTS = [
    "Letters for learners",     # Handwriting
    "Libre Baskerville",        # Serif
    "Kalam",                    # Handwriting
    "Kausham",                  # Serif
    "Roboto",                   # Sans serif
    ""                          # Default serif font
]


def has_collision(objx, objy, objw, objh, elem_list):
    for elem in elem_list:
        width, height = elem["coordinates"]["width"], elem["coordinates"]["height"]
        xpos, ypos = elem["coordinates"]["x"], elem["coordinates"]["y"]

        if (objx < (xpos + width) and objy < (ypos + height) and (objx + objw) > xpos and (objy + objh) > ypos):
            return True

    return False


def generate_random(elem_type, dimmin, dimmax, xmax, ymax):
    """Narrowing results to desired shapes"""
    width = random.randint(dimmin, dimmax)
    height = random.randint(dimmin, dimmax)
    posx = random.randint(0, xmax)
    posy = random.randint(0, ymax)

    if elem_type in ("select", "textbox"):
        while not ((1 / 8) <= (height / width) <= (1/4)):
            width = random.randint(150, 300)
            height = random.randint(20, 75)

    elif elem_type in ("checkbox", "radio"):
        width, height = 20, 20

    elif elem_type == "label":
        width, height = 60, 24

    elif elem_type == "link":
        width, height = 52, 25

    elif elem_type == "header":
        width, height = 125, 60

    elif elem_type == "paragraph":
        while (width / height) < 0.6 or (height / width) < 0.2:
            width = random.randint(40, dimmax)
            height = random.randint(20, dimmax)

    else:
        while (width / height) < 0.3 or (height / width) < 0.15:
            width = random.randint(40, dimmax)
            height = random.randint(20, dimmax)

    return width, height, posx, posy


def generate_text_content(length=35):
    return " ".join([random.choice(WORDS) for _ in range(length)]).capitalize()

