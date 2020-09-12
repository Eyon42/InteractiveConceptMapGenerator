import networkx as nx
import numpy as np
import markdown as md

from bokeh.plotting import figure, from_networkx
from bokeh.models import (Circle, HoverTool, TapTool, Div, Label, LabelSet, CustomJS,
                          MultiLine, NodesAndLinkedEdges, ColumnDataSource)
from bokeh.layouts import row, column
from bokeh.palettes import PuBu9 as color_palette
from bokeh.embed import components
from bokeh.resources import CDN

from conceptParser import build_concept_network
from jinja2 import Template


# Import data

G, N, concept_data, Title = build_concept_network("Conceptos.md")
titles = [concept["name"] for concept in concept_data]
html_content = [md.markdown(concept["content"]) for concept in concept_data]

# Get conection info about the nodes
node_conections = [list(nx.neighbors(G, n)) for n in range(N)]
node_conectivity = [len(con) for con in node_conections]


# Graph plotting code

plot_size = 800 #px
plot = figure(toolbar_location=None, x_range=(-1,1), y_range=(-1,1), height=plot_size, width=plot_size)
plot.xgrid.visible = False
plot.ygrid.visible = False
plot.axis.visible = False
plot.outline_line_alpha = 0
plot.toolbar.active_drag = None

# Create the graph object from the NetworkX nodes
graph_rel_size = 0.8
graph = from_networkx(G, nx.circular_layout, scale=graph_rel_size, center=(0,0))

# Size of the node depends on amount of conections:
node_sizes = [(plot_size*graph_rel_size*np.pi/N)*(1.5 + np.log(node))/4 for node in node_conectivity]

# Add data to the nodes
graph.node_renderer.data_source.add(titles, 'title')
graph.node_renderer.data_source.add(node_conectivity, 'node_conectivity')
graph.node_renderer.data_source.add(node_sizes, 'node_size')
graph.node_renderer.data_source.add([", ".join([concept_data[n]["name"] for n in node]) for node in node_conections], 'node_conections')

# Set up tooltips and enable selection.
graph.selection_policy = NodesAndLinkedEdges()
node_hover_name = HoverTool(tooltips=[("Concepto", "@title"), ("Conectividad", "@node_conectivity"), ("Conecciones", "@node_conections")])
plot.add_tools(node_hover_name, TapTool())

# Configure the nodes's apparence
graph.node_renderer.glyph = Circle(size="node_size", fill_color=color_palette[1])
graph.node_renderer.selection_glyph = Circle(size="node_size", fill_color=color_palette[4])
graph.node_renderer.hover_glyph = Circle(size="node_size", fill_color=color_palette[3])

# Configure the edge's apparence
graph.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=2)
graph.edge_renderer.selection_glyph = MultiLine(line_color=color_palette[4], line_width=3)

# Node labels:
# Organize the lable data and keep it separated from the graph data
labels_pos = np.transpose(list(graph.layout_provider.graph_layout.values()))
label_angles = np.arctan(labels_pos[1]/labels_pos[0]) # Used to calculate position offset
labeldata = ColumnDataSource(data=dict(x_pos=labels_pos[0], y_pos=labels_pos[1],
                             # This makes that labels are only showed for the nodes with most conections:
                             text=[titles[i] if node_conectivity[i] > 4 else "" for i in range(N)],
                             x_off=25 * np.cos(label_angles), y_off=50 * np.sin(label_angles)))

labels = LabelSet(x="x_pos", y="y_pos", text='text', level='glyph',
              x_offset="x_off", y_offset="y_off", source=labeldata, render_mode='canvas')

# Add all graph elements to plot
plot.add_layout(labels)
plot.renderers.append(graph)

## Create side panel with content

default_text=md.markdown(f"""
## Mapa de {Title}

Este es un mapa que conecta todos los conceptos de {Title} en un gráfico interactivo

Cada círculo representa un concepto, y las lineas representan las conexiones entre conceptos.
Al pasar el mouse por sobre los circulos podrás ver información sobre el concepto y sus conecciones. Al hacer click en los circulos, este panel mostrará información detallada sobre el concepto.
    """)

div_content = Div(text=default_text, width=int(plot_size/2), height=plot_size, css_classes=["scroll"])

# This script handels the text changes and Katex redrawing
displayDetails = CustomJS(args=dict(src=graph.node_renderer.data_source, target=div_content, label_texts=html_content), code="""
            const index = src.selected.indices[0]
            target.text = label_texts[index];
            renderMathInElement(document.body, {
                delimiters:[
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false}
                ]
            });
        """
)

taptool = plot.select(type=TapTool)
taptool.callback = displayDetails

# Export everything as an html file

# get bokeh parts
sep_line = Div(style=dict(zip(["border", "height"], ["1px solid black", "100%"])))
script_bokeh, div_bokeh = components(row(plot, sep_line, div_content))
resources_bokeh = CDN.render()


# Set up html template
template = Template(
    '''<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>
                    {{ title }}
                </title>
                {{ resources }}
                {{ script }}
                <style>
                    .embed-wrapper {
                        display: flex;
                        justify-content: space-evenly;
                    }
                    div.scroll {
                        overflow-y: auto;
                    }
                </style>


                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">

                <!-- The loading of KaTeX is deferred to speed up page rendering -->
                <script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js" integrity="sha384-g7c+Jr9ZivxKLnZTDUhnkOnsh30B4H0rpLUpJ4jAIKs4fnJI+sEnkvrMWph2EDg4" crossorigin="anonymous"></script>
            
                <!-- To automatically render math in text elements, include the auto-render extension: -->
                <script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js" integrity="sha384-mll67QQFJfxn0IYznZYonOWZ644AWYC+Pt2cHqMaRhXVrursRwvLnLaebdGIlYNa" crossorigin="anonymous"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        renderMathInElement(document.body, {
                            delimiters:[
                                {left: "$$", right: "$$", display: true},
                                {left: "$", right: "$", display: false}
                            ]
                        });
                    });
                </script>
            </head>
            <body>            
                <div class="embed-wrapper">
                    {{ div }}
                </div>
            </body>
        </html>
        ''')


# render everything together
html = template.render(title=Title,
                        resources=resources_bokeh,
                        script=script_bokeh,
                        div=div_bokeh)

# save to file
out_file_path = "am_map.html"
with open(out_file_path, mode='w') as f:
    f.write(html)


"""
TO-DO:
- Make it prettier, and adaptable to different screen sizes
- Put it online

Sources:
https://katex.org/
https://python-markdown.github.io/
https://docs.bokeh.org/en/latest/index.html
https://networkx.github.io/documentation/stable/index.html
"""