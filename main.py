import os
import pathlib
from difflib import SequenceMatcher as SM

import fire
from alive_progress import alive_bar

def list_directory(dir_path: str):
    files = []

    for obj in pathlib.Path(dir_path).iterdir():
        if obj.is_dir():
            sub_files = list_directory(f"{dir_path}/{obj.name}")
            files += sub_files
        else:
            files.append({ "path": str(obj.absolute()), "name": obj.name })

    return files

def main(root_path:str):
    if not os.path.exists(root_path):
        raise Exception(f"Directory {root_path} not exists")

    print("Working on:", root_path, "\n")

    files = { "root": [] }

    path_list = list(pathlib.Path(root_path).iterdir())
    with alive_bar(total=len(path_list), title="Collecting files", theme="classic") as progess_bar:
        for file in path_list:
            if file.is_dir():
                sub_files = list_directory(f"{root_path}/{file.name}")
                files[file.name] = sub_files
                progess_bar()
            else:
                files["root"].append({ "path": str(file.absolute()), "name": file.name })
                progess_bar()

    all_files = []
    for directory in files:
        all_files += files[directory]
    print(f" - found {len(all_files)} files in {len(files)} dirs")

    collection = []
    coincidences = {}

    for file in all_files[:10]:
        current_key = file["path"]
        current = file ["name"]
        coincidences[current_key] = []

        with alive_bar(total=len(all_files)-1, title=current_key.split("/")[-1], theme="classic") as progress_bar:
            for folder in files:
                for _file in [item for item in files[folder] if item["path"] != current_key]:
                    if SM(None, current, _file["name"]).ratio() > 0.7 and _file["path"] not in collection:
                        coincidences[current_key].append(_file["path"])
                        collection.append(_file["path"])
                    progress_bar()

            if len(coincidences[current_key]) == 0:
                del coincidences[current_key]

    print("RESULT:")
    for coincidence in coincidences:
        print("  -", coincidence)
        for path in coincidences[coincidence]:
            print("   ->", path)

if __name__ == "__main__":
    fire.Fire(main)

