import os
from datetime import datetime

import streamlit as st
from streamlit_file_browser import st_file_browser
from streamlit_sortables import sort_items

from utils import load_config, save_config


@st.dialog("File Browser", width="large")
def file_browser_window(key: str, state_name: str, path: str = ".", file_type: str | None = None):
    if path.strip() == "":
        path = "./"
    if file_type is None:
        show_choose_folder = True
        show_choose_file = True
    elif file_type == "folder":
        show_choose_folder = True
        show_choose_file = False
    elif file_type == "yaml":
        show_choose_folder = False
        show_choose_file = True
    else:
        raise ValueError("file_type must be either 'folder' or 'yaml'")
    event = st_file_browser(
        path,
        ignore_file_select_event=True,
        show_choose_file=show_choose_file,
        show_choose_folder=show_choose_folder,
        key=key,
        sort=True,
    )
    if event is not None and event["type"].startswith("CHOOSE_"):
        target = event["target"]
        if isinstance(target, dict):
            st.session_state[state_name] = target["path"]
        else:
            st.session_state[state_name] = target[0]["path"]
        st.rerun()


@st.dialog("Reorder", width="small")
def reorder_window(
    original_display_names: list[str],
    display_names: list[str],
    original_folder_paths: list[str],
    folder_path_name_format: str = "input_folder_path_{}",
    display_name_name_format: str = "input_display_name_{}",
):
    sorted_display_names = sort_items(display_names, key="index_page_reorder", direction="vertical")
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        finished_button = st.button("Finished", key="reorder_finish")
        if finished_button:
            for i, name in enumerate(sorted_display_names):
                if name != display_names[i]:
                    original_index = display_names.index(name)
                    st.session_state[folder_path_name_format.format(i)] = original_folder_paths[original_index]
                    st.session_state[display_name_name_format.format(i)] = original_display_names[original_index]
            st.rerun()


@st.dialog("Save Config", width="small")
def save_config_window(
    folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    timestamp = datetime.now().strftime("%y%m%d.%H%M%S")
    save_name = st.text_input(
        "Save Path",
        key="save_path",
        placeholder=f"Path to Save the Current Configurations (Default: {timestamp}.yaml)",
        value=st.session_state.get("input_save_path", ""),
        on_change=lambda: st.session_state.update(input_save_path=st.session_state.save_path),
    )
    save_name = save_name.strip()
    if save_name == "":
        save_name = st.session_state.get("save_path", "")
    if save_name.strip() == "":
        save_name = f"{timestamp}.yaml"
    if st.button("Finish", key="save_finish"):
        save_config(save_name=save_name, folder_path_format=folder_path_format, display_name_format=display_name_format)
        st.rerun()


@st.dialog("Load Config", width="small")
def load_config_window(
    folder_path_format: str = "input_folder_path_{}", display_name_format: str = "input_display_name_{}"
):
    options = []
    config_dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")
    for root, dirs, files in os.walk(config_dirpath):
        for file in files:
            if file.endswith((".yaml", ".yml", ".YAML", ".YML")):
                options.append(os.path.relpath(os.path.join(root, file), root))
    options = sorted(options)
    config_path = st.selectbox("Path to a Configuration File", options=options, key="load_config_path")
    if st.button("Finish", key="load_finish"):
        load_config(
            load_name=config_path, folder_path_format=folder_path_format, display_name_format=display_name_format
        )
