# HTML JSON description of a webpage to an image

The project aims to generate image representations from JSON descriptions of a webpages's input elements.

## Input template:
```json
data: [
    {
        "name": "name",
        "type": "type",  // See the `Input types` section
        "coordinates": { "x": "x-pos", "y": "y-pos", "w": "width", "h": "height" },
        "content": "content"
    },
    {
        "etc": "..."
    }
]
```
Note: no element can overlap any other.

## Output:
Image (any common format).

## Input types
See a list of allowed input types in [Mozilla's docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input).

## Method
We will generate HTML files from the JSON data and then render the webpage to an image.
This readme is subject to change.
