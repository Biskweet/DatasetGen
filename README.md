# JSON description of an HTML webpage and image generation

The project aims to generate image representations from JSON descriptions of a webpages's input elements.

## Requirements
* The [WKHTMLtoPDF](https://wkhtmltopdf.org/) Linux package
* Any compatible Linux distribution
* A recent Python installation


## Input template:
```json
"data": [
    {
        "name": "name",
        "type": "type",
        "coordinates": { "x": "x-pos", "y": "y-pos", "w": "width", "h": "height" },
        "content": "content"
    },
    {
        "etc": "..."
    }
]
```
Note: no element can overlap any other.
Note 2 : See the [Input types](#input-types) section

## Output:
Image (any common format).

## Input types
See a list of allowed input types in [Mozilla's docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input).

## Method
We will generate HTML files from the JSON data and then render the webpage to an image.
This readme is subject to change.

