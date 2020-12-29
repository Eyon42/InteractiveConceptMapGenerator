# Interactive Concept Map Generator
A python script that takes a markdown file with a specific structure, parses it, and uses bokeh to generate an interactive graph.

## Examples:
- [Análisis Matemático(Spanish)](https://eyon42.github.io/InteractiveConceptMapGenerator/output/map.html)

## Structure for the markdown file:

```
# [Title]
## [Concept]
[Some text]
[Latex math is supported]
[Images have limited support]
### [Any subtitle]
### Utiliza:
- [Related concept 1]
- [Related concept 2]
## [Concept]
```

## Usage 

```
python3 build.py [-h] [-o OUTPUT] [-i INPUT]
```

If no optional arguments are given, the file "examples/AnálisisMatemático1.md" will be used as source and the output will be "output/map.html".

## Requirements:

- Python (min.: 3.6)
- [Bokeh](https://bokeh.org/)
- [NetworkX](https://networkx.org/)
- [Numpy](https://numpy.org/)
- [Markdown](https://python-markdown.github.io/)
- [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)

## Using images:

Images are not managed by this script. The path to the images is kept the same as in the markdown file.
