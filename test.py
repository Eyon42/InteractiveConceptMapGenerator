import argparse

parser = argparse.ArgumentParser(description='A python script that takes a markdown file with a specific structure, parses it, and uses bokeh to generate an interactive graph.')
parser.add_argument('-o', '--output', help="Select output file.")
parser.add_argument('-i', '--input', help="Select input file.")

parser.add_argument

args = parser.parse_args()
if args.input:
    print('test')