from datetime import datetime

import streamlit as st

from buttons import add_button, load_button, remove_button, reorder_button, save_button
from dialogs import load_config_window, reorder_window, save_config_window
from utils import (
    add_folder,
    caption_path_selectbox,
    remove_folder,
    set_default_display_names,
    set_default_values,
    unique_display_names,
)


def main():
    st.set_page_config(layout="wide")
    set_default_values()

    with st.sidebar:
        if "config_path" not in st.session_state:
            timestamp = datetime.now().strftime("%y%m%d.%H%M%S")
            st.session_state["timestamp"] = timestamp
            st.session_state["config_path"] = f"{timestamp}.yaml"
        need_load = load_button(styleable_key="styleable_load_button", key="load_button", use_container_width=True)
        need_save = save_button(styleable_key="styleable_save_button", key="save_button", use_container_width=True)
        if need_load:
            load_config_window()
        st.divider()
        need_compare = st.button("Compare", key="compare_button", type="primary", use_container_width=True)

    with st.container(border=True):
        col1, col2, col3 = st.columns([1.5, 1.5, 8])
        with col1:
            num_samples_per_page = st.number_input(
                "Number of Samples Per Page", key="input_num_samples_per_page", min_value=1, max_value=50
            )
        with col2:
            random_seed = st.number_input("Random Seed", key="input_random_seed", min_value=-1)
        with col3:
            caption_path = caption_path_selectbox()

    num_folders = st.session_state["num_folders"]

    for i in range(num_folders + 1):
        col1, col2, col3, col4 = st.columns([2, 10, 6, 2], vertical_alignment="bottom")
        with col1:
            button = add_button(
                styleable_key=f"styleable_add_button_{i}", key=f"add_button_{i}", use_container_width=True
            )
            if button:
                add_folder(i)
        with col4:
            button = remove_button(
                styleable_key=f"styleable_remove_button_{i}",
                key=f"remove_button_{i}",
                disabled=i == num_folders,
                use_container_width=True,
            )
            if button and num_folders > 1:
                remove_folder(i)
        with col2:
            st.text_input(f"Folder Path", key=f"input_folder_path_{i}", disabled=i == num_folders)
            st.session_state[f"folder_path_{i}"] = st.session_state[f"input_folder_path_{i}"]
        with col3:
            folder_id = i + 1
            st.text_input(
                f"Display Name",
                key=f"input_display_name_{i}",
                placeholder=f"Folder {folder_id}",
                disabled=i == num_folders,
            )
            st.session_state[f"display_name_{i}"] = st.session_state[f"input_display_name_{i}"]

    st.session_state["num_folders"] = num_folders
    st.session_state["num_samples_per_page"] = num_samples_per_page
    st.session_state["random_seed"] = random_seed
    st.session_state["caption_path"] = caption_path
    for i in range(num_folders):
        st.session_state[f"folder_path_{i}"] = st.session_state[f"input_folder_path_{i}"]
        st.session_state[f"display_name_{i}"] = st.session_state[f"input_display_name_{i}"]

    original_display_names = [st.session_state.get(f"input_display_name_{i}", "") for i in range(num_folders)]
    original_folder_paths = [st.session_state.get(f"input_folder_path_{i}", "") for i in range(num_folders)]
    display_names = set_default_display_names(original_display_names)

    button = reorder_button(
        styleable_key="reorder_button",
        key="reorder_button",
        disabled=not unique_display_names(display_names),
        use_container_width=True,
    )
    if button:
        reorder_window(original_display_names, display_names, original_folder_paths)

    if need_save:
        save_config_window()

    if need_compare:
        st.switch_page("pages/compare.py")


if __name__ == "__main__":
    main()
