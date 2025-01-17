import copy
import os
import random

import streamlit as st
import yaml

from variables import ALLOWED_EXTENSIONS, CAPTION_PATH_OPTIONS


def caption_path_selectbox() -> str | None:
    options = copy.deepcopy(CAPTION_PATH_OPTIONS)
    caption_dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captions")
    caption_paths = []
    for root, dirs, files in os.walk(caption_dirpath):
        for file in files:
            if file.endswith((".yaml", ".yml", ".YAML", ".YML")):
                caption_paths.append(os.path.relpath(os.path.join(root, file), caption_dirpath))
    caption_paths = sorted(caption_paths)
    options.extend(caption_paths)
    default_caption_path = st.session_state.get("caption_path", None)
    if default_caption_path is not None:
        if default_caption_path in options:
            options.remove(default_caption_path)
        options.insert(0, st.session_state["caption_path"])
    caption_path = st.selectbox("Path to a Caption File", options=options, key="input_caption_path")
    if caption_path == "none":
        caption_path = None
    return caption_path


def match_file(dirpath: str, name: str) -> str:
    for ext in ALLOWED_EXTENSIONS:
        if os.path.exists(os.path.join(dirpath, name + "." + ext)):
            return name + "." + ext
        elif os.path.exists(os.path.join(dirpath, name + "." + ext.upper())):
            return name + "." + ext.upper()
    return name


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_names(dirpaths: list[str], seed: int) -> list[str]:
    all_files = []
    for dirpath in dirpaths:
        print(os.getcwd(), dirpath)

        dirpath = dirpath.strip()
        if dirpath == "" or not os.path.isdir(dirpath):
            file_names = []
        else:
            file_names = [f.rsplit(".", 1)[0] for f in os.listdir(dirpath) if allowed_file(f)]
        all_files.append(file_names)
    name_sets = [set(names) for names in all_files]
    file_names = sorted(list(set.intersection(*name_sets)))

    if seed >= 0:
        random.Random(seed).shuffle(file_names)
    return file_names


def get_caption(captions: dict[str, str], file_name: str) -> str | None:
    if captions is not None:
        return captions.get(file_name, None)
    else:
        return None


def set_default_values():
    if "num_folders" not in st.session_state:
        st.session_state["num_folders"] = 2
    if "random_seed" not in st.session_state:
        st.session_state["input_random_seed"] = 0
    if "page_id" not in st.session_state:
        st.session_state["page_id"] = 0
    if "num_samples_per_page" not in st.session_state:
        st.session_state["input_num_samples_per_page"] = 10
    if "caption_path" not in st.session_state:
        st.session_state["caption_path"] = None


def set_default_display_names(display_names: list[str]) -> list[str]:
    new_display_names = []
    for i, name in enumerate(display_names):
        name = name.strip()
        if name == "":
            new_display_names.append(f"Folder {i + 1}")
        else:
            new_display_names.append(name)
    return new_display_names


def unique_display_names(display_names: list[str]) -> bool:
    return len(set(display_names)) == len(display_names)


def add_folder(
    position: int, folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    st.session_state.num_folders = st.session_state["num_folders"] + 1
    for j in range(st.session_state.num_folders, position, -1):
        st.session_state[folder_path_format.format(j)] = st.session_state.get(folder_path_format.format(j - 1), "")
        st.session_state[display_name_format.format(j)] = st.session_state.get(display_name_format.format(j - 1), "")
    st.session_state[folder_path_format.format(position)] = ""
    st.session_state[display_name_format.format(position)] = ""
    st.rerun()


def remove_folder(
    position: int, folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    for j in range(position, st.session_state.num_folders - 1):
        st.session_state[folder_path_format.format(j)] = st.session_state.get(folder_path_format.format(j + 1), "")
        st.session_state[display_name_format.format(j)] = st.session_state.get(display_name_format.format(j + 1), "")
    st.session_state.num_folders = st.session_state.num_folders - 1
    st.rerun()


def get_current_config(
    folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
) -> dict:
    config = {}
    config["num_folders"] = st.session_state.get("num_folders", 2)
    config["random_seed"] = st.session_state.get("random_seed", 0)
    config["num_samples_per_page"] = st.session_state.get("num_samples_per_page", 5)
    config["caption_path"] = st.session_state.get("caption_path", None)

    config["folder_paths"] = []
    config["display_names"] = []
    for i in range(config["num_folders"]):
        folder_path = st.session_state.get(folder_path_format.format(i), "")
        display_name = st.session_state.get(display_name_format.format(i), "")
        config["folder_paths"].append(folder_path)
        config["display_names"].append(display_name)
    return config


def restore_from_config(
    path: str, folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    if not os.path.exists(path) or not path.endswith(".yaml"):
        return
    config = yaml.load(open(path, "r"), Loader=yaml.FullLoader)
    st.session_state["num_folders"] = config["num_folders"]
    st.session_state["random_seed"] = config["random_seed"]
    st.session_state["num_samples_per_page"] = config["num_samples_per_page"]
    st.session_state["caption_path"] = config["caption_path"]
    for i in range(config["num_folders"]):
        st.session_state[folder_path_format.format(i)] = config["folder_paths"][i]
        st.session_state[display_name_format.format(i)] = config["display_names"][i]


def save_config(
    save_name: str, folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    if not save_name.endswith((".yaml", ".yml", ".YAML", ".YML")):
        save_name += ".yaml"
    config = get_current_config(folder_path_format, display_name_format)

    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")
    path = os.path.join(root, save_name)

    save_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(save_dir, exist_ok=True)

    with open(path, "w") as f:
        yaml.dump(config, f)


def load_config(
    load_name: str, folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")
    restore_from_config(
        os.path.join(root, load_name), folder_path_format=folder_path_format, display_name_format=display_name_format
    )
    st.rerun()
