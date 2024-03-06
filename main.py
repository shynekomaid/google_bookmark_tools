import sys
import os
import argparse
import json


def args_parser():
    parser = argparse.ArgumentParser(description="Converts JSON to HTML and vice versa")
    parser.add_argument(
        "--mode",
        type=str,
        help="Mode: j2b for JSON to HTML, b2j for HTML to JSON",
        required=True,
        choices=["j2b", "b2j"],
    )
    parser.add_argument(
        "--input_file", type=str, help="Input file", default="input.json"
    )
    parser.add_argument(
        "--output_file", type=str, help="Output file", default="output.html"
    )
    # more modes will be added in future
    return parser.parse_args()


try:
    if __name__ == "__main__":
        argum = args_parser()
        if argum.mode == "j2b":
            import modules.j2b as j2b

            status, bookmarkFile = j2b.do(argum.input_file)
            if status:
                try:
                    f = open(argum.output_file, "w")
                    f.write(bookmarkFile)
                    f.close()
                except Exception as e:
                    raise e
            else:
                raise Exception("Bookmark file not created")

            pass
        elif argum.mode == "b2j":
            import modules.b2j as b2j

            status, jsonFile = b2j.do(argum.input_file)
            if status:
                try:
                    f = open(argum.output_file, "w")
                    f.write(jsonFile)
                    f.close()
                except Exception as e:
                    raise e
            else:
                raise Exception("JSON file not created")
    else:
        raise Exception("This file is not meant to be imported")

except Exception as e:
    print(e)
    sys.exit(1)
