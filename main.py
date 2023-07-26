import os
import pathlib

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

    print("Working on:", root_path, "\n\n")

    files = { "root": [] }
    all_files = []

    path_list = list(pathlib.Path(root_path).iterdir())
    with alive_bar(total=len(path_list), title="Collecting files", theme="classic") as progess_bar:
        for file in path_list:
            print(str( file.name ))
            if file.is_dir():
                sub_files = list_directory(f"{root_path}/{file.name}")
                files[file.name] = sub_files
                all_files += sub_files
                progess_bar()
            else:
                files["root"].append({ "path": str(file.absolute()), "name": file.name })
                all_files.append({ "path": str(file.absolute()), "name": file.name })
                progess_bar()

    total = 0
    for directory in files:
        total += len(files[directory])
    print(f"found {total} files in {len(files)} dirs")
    print(f"Total {len(all_files)}")


if __name__ == "__main__":
    fire.Fire(main)

