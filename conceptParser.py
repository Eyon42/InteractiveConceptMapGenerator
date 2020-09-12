import networkx as nx


def parse_concepts(filename):
    """Takes a markdown file with with a certain structure
    and parses it to separate the concept and the relations
    between the concepts.

    Structure:

    # [Title]

    ## [Concept]

    [Some text]
    [Even Latex math]

    ### [Any subtitle]

    ### Utiliza:

    - [Related concept 1]
    - [Related concept 2]

    ## [Concept]
    ...

    The functions returns an array of dicts and a string with the Title.
    Each dictionary correspond to a concept and has keys for:
    
    id      -> The position of the dict in the array. This is useful to build the network.
    name    -> The title of the concept. What appears as [Concept] in the structure.
    uses    -> Array of the indexes of the concepts in the "Utiliza:" section.
    content -> All of the plain text beetween the Concept title and the "Utiliza:" section.
    """
    # Open the markdown file
    with open(filename, "r") as file:
        text = file.read()

    # Create list of concepts and save title
    Concepts = []
    index = 0
    sections = text.split("\n## ")
    Title = sections[0].strip("# ").strip("\n")
    for con in sections[1:]:
        concept = {}
        lines = [i for i in con.split("\n") if i != ""]
        concept["id"] = index
        concept["name"] = lines[0]

        try:
            end_index = lines.index("### Utiliza:")
            concept["uses"] = [line.strip("- ") for line in lines[end_index+1:]]
        except:
            concept["uses"] = []
            end_index = len(lines)

        concept["content"] = "\n".join(lines[1:end_index])
        concept["content"] = "##"+concept["name"]+ "\n" + concept["content"]
        
        Concepts.append(concept)
        index += 1

    # Update relative indexes
    for con in Concepts:
        uses_index = []
        for i in Concepts:
            if i["name"] in con["uses"]:
                uses_index.append(i["id"])
        con["uses"] = uses_index

    return Concepts, Title


def build_concept_network(filename):
    """
    Uses NetworkX to build a network of concepts with the data
    parsed from the file passed as argument.
    
    The network only saves conections, it does not keep the direction
    of the conections.

    Returns a tuple with:
    - NetworkX graph object
    - Number of nodes
    - The dictionary with the concept data
    - The title for the network
    """

    concept_data, Title = parse_concepts(filename)

    N = len(concept_data)

    G = nx.Graph()
    G.add_nodes_from(list(range(0, N)))

    # Build edges
    for concept in concept_data:
        for use in concept["uses"]:
            G.add_edge(concept["id"], use)
    
    return (G, N, concept_data, Title)