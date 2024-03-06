# It's a module to convert json to bookmarked html file

if __name__ == "__main__":
    raise Exception("This file is module and not meant to be executed directly")

import json
from time import time as utime


def load_json(file):
    try:
        f = open(file, "r")
        return json.load(f)
    except FileExistsError:
        raise Exception("File not found")
    except Exception as e:
        raise e


def parse_folder(data):
    unixtime = int(utime())
    chunk = ""
    if not "name" in data:
        raise Exception("Folder must have a name")
    chunk += "<DT>\n"
    chunk += (
        f'<H3 ADD_DATE="{unixtime}" LAST_MODIFIED="{unixtime}">{data["name"]}</H3>\n'
    )
    if "contain" in data:
        chunk += "<DL>\n"
        chunk += "<p>\n"
        for item in data["contain"]:
            if item["type"] == "folder":
                chunk += parse_folder(item)
            elif item["type"] == "url":
                chunk += parse_url(item)
            else:
                raise Exception("Unknown type")
        chunk += "</p>\n"
        chunk += "</DL>\n"
    chunk += "</DT>\n"
    return chunk


def parse_url(data):
    unixtime = int(utime())
    chunk = ""
    if not "name" in data:
        raise Exception("URL must have a name")
    if not "url" in data:
        raise Exception("URL must have a URL")
    chunk += "<DT>\n"
    chunk += "<p>\n"
    chunk += (
        f'<A HREF="{data["url"]}" ADD_DATE="{unixtime}" ICON="">{data["name"]}</A>\n'
    )
    chunk += "</p>\n"
    chunk += "</DT>\n"
    return chunk


def do(filename):
    unixtime = int(utime())
    data = load_json(filename)
    if not "type" in data or data["type"] != "folder":
        raise Exception("Root must be a folder")
    if not "name" in data:
        raise Exception("Root must have a name")

    # Boilerplate
    output_content = ""
    output_content += "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
    output_content += "<!-- This is an automatically generated file.\n"
    output_content += "It will be read and overwritten.\n"
    output_content += "DO NOT EDIT! -->\n"
    output_content += (
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
    )
    output_content += "<TITLE>Bookmarks</TITLE>\n"
    output_content += "<H1>Bookmarks</H1>\n"

    # Root boilerplate
    output_content += "<DL>\n"
    output_content += "<p>\n"
    output_content += "<DT>\n"
    output_content += f'<H3 ADD_DATE="{unixtime}" LAST_MODIFIED="{unixtime}" PERSONAL_TOOLBAR_FOLDER="true">{data["name"]}</H3>\n'

    if "contain" in data:
        output_content += "<DL>\n"
        output_content += "<p>\n"
        for item in data["contain"]:
            if item["type"] == "folder":
                output_content += parse_folder(item)
            elif item["type"] == "url":
                output_content += parse_url(item)
            else:
                raise Exception("Unknown type")
        output_content += "</p>\n"
        output_content += "</DL>\n"

    # End of root boilerplate
    output_content += "</DT>\n"
    output_content += "</p>\n"
    output_content += "</DL>\n"

    return True, output_content
