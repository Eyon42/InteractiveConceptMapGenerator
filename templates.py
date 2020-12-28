from jinja2 import Template

# Set up html template
template = Template('''

<!DOCTYPE html>
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
                height: auto;
            }
            #main
            {         
                position:fixed;
                top:0px;
                bottom:0px;
                left:0px;
                right:0px;
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
        <div id="main">
            <div class="embed-wrapper">
                {{ div }}
            </div>
        </div>
    </body>
</html>

''')