import enum
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from PIL import Image, ImageDraw

classnames = ['button', 'checkbox', 'header', 'image', 'label', 'link',
              'paragraph', 'radio', 'select', 'textarea', 'textbox']
classes = {i:name for i, name in enumerate(classnames)}


def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size
    plotted_image = ImageDraw.Draw(image)
    transformed_annotations = np.copy(annotations)
    transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
    transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
    transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
    transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
    transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
    transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0,y0), (x1,y1)), outline="green")
        plotted_image.text((x0, y0 - 10), classes[(int(obj_cls))], fill="green")
    plt.imshow(np.array(image))
    plt.show()


filename = random.choice(os.listdir("images/"))
image = Image.open("images/" + filename)
label = "labels/" + filename.replace("jpg", "txt")

with open(label, "r") as file:
    description = file.read().split("\n")[:-1]
    description = [x.split(" ") for x in description]
    description = [[float(y) for y in x ] for x in description]

print("Image number:", filename)

plot_bounding_box(image, description)
