from bs4 import BeautifulSoup
import json


def parse_bookmarks(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        root_element = soup.find("dl")

        if root_element:
            bookmarks_json = parse_folder(root_element.find_all("dt"))
            return True, bookmarks_json

    except Exception as e:
        return False, f"Error parsing HTML: {str(e)}"


def parse_folder(folder_elements):
    folder_data = {
        "name": get_text(folder_elements[0].find("h3")) if folder_elements else "",
        "description": (
            f"{get_text(folder_elements[0].find('h3'))} folder"
            if folder_elements
            else "Root folder"
        ),
        "type": "folder",
        "contain": [],
    }

    for folder_element in folder_elements:
        subfolder = folder_element.find("dl")
        if subfolder:
            folder_data["contain"].append(parse_folder(subfolder.find_all("dt")))
        else:
            folder_data["contain"].append(parse_bookmark(folder_element))

    return folder_data


def parse_bookmark(bookmark_element):
    bookmark_data = {
        "name": get_text(bookmark_element.find("a")),
        "human_name": get_text(bookmark_element.find("a")),
        "description": f"{get_text(bookmark_element.find('a'))} Web Site",
        "type": "url",
        "url": bookmark_element.find("a").get("href"),
    }
    return bookmark_data


def get_text(element):
    return element.get_text() if element else ""


def do(filename):
    success, result = parse_bookmarks(filename)
    if success:
        return True, json.dumps(result, indent=2)
    else:
        raise Exception(result)


if __name__ == "__main__":
    raise Exception("This file is a module and not meant to be executed directly")
