import os

import streamlit as st
import yaml

from buttons import add_button, load_button, remove_button, reorder_button, save_button
from dialogs import load_config_window, reorder_window, save_config_window
from utils import (
    add_folder,
    caption_path_selectbox,
    get_caption,
    get_file_names,
    match_file,
    remove_folder,
    set_default_display_names,
    set_default_values,
    unique_display_names,
)
from variables import IMAGE_EXTENSIONS, MEDIA_COLUMN_WIDTH


def main():
    set_default_values()

    num_folders = st.session_state["num_folders"]
    dirpaths = [st.session_state[f"folder_path_{i}"].strip() for i in range(st.session_state.num_folders)]
    original_display_names = [st.session_state[f"display_name_{i}"].strip() for i in range(num_folders)]
    display_names = set_default_display_names(original_display_names)
    seed = st.session_state["random_seed"]
    file_names = get_file_names(dirpaths, seed)

    num_samples_per_page = st.session_state["num_samples_per_page"]
    max_page_id = max((len(file_names) + num_samples_per_page - 1) // num_samples_per_page, 1)

    if st.session_state["page_id"] >= max_page_id:
        st.session_state["page_id"] = max_page_id - 1
    page_id = st.session_state["page_id"]

    with st.sidebar:
        st.number_input(
            "Number of Samples Per Page",
            key="num_samples_per_page",
            min_value=1,
            max_value=50,
        )
        st.number_input("Random Seed", key="random_seed", min_value=-1)

        caption_path_selectbox()
        caption_path = st.session_state.get("input_caption_path", None)

        if caption_path == "none":
            caption_path = None
        elif isinstance(caption_path, str):
            caption_dirpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "captions")
            caption_path = os.path.join(caption_dirpath, caption_path)

        if caption_path is not None and os.path.exists(caption_path):
            captions = yaml.load(open(caption_path, "r"), Loader=yaml.FullLoader)
        else:
            captions = None

        button = reorder_button(
            styleable_key="reorder_button",
            key="reorder_button",
            disabled=not unique_display_names(display_names),
            use_container_width=True,
        )
        if button:
            reorder_window(original_display_names, display_names, dirpaths, "folder_path_{}", "display_name_{}")

        st.divider()

        if load_button(styleable_key="styleable_load_button", key="load_button", use_container_width=True):
            load_config_window(folder_path_format="folder_path_{}", display_name_format="display_name_{}")
        if save_button(styleable_key="styleable_save_button", key="save_button", use_container_width=True):
            save_config_window(folder_path_format="folder_path_{}", display_name_format="display_name_{}")

        st.divider()

        return_index = st.button("Return to Index", type="primary", use_container_width=True)
        if return_index:
            st.session_state["input_random_seed"] = st.session_state["random_seed"]
            st.session_state["input_num_samples_per_page"] = st.session_state["num_samples_per_page"]
            for i in range(st.session_state["num_folders"]):
                st.session_state[f"input_folder_path_{i}"] = st.session_state[f"folder_path_{i}"]
                st.session_state[f"input_display_name_{i}"] = st.session_state[f"display_name_{i}"]

            st.switch_page("main.py")

    cols = st.columns([MEDIA_COLUMN_WIDTH] * num_folders + [1])

    for i in range(num_folders + 1):
        with cols[i]:
            if i < num_folders:
                col1, col2 = st.columns(2)
                with col1:
                    need_add_folder = add_button(
                        styleable_key=f"styleable_add_button_{i}", key=f"add_button_{i}", use_container_width=True
                    )
                with col2:
                    need_remove_folder = remove_button(
                        styleable_key=f"styleable_remove_button_{i}",
                        key=f"remove_button_{i}",
                        use_container_width=True,
                    )
            else:
                need_add_folder = add_button(
                    styleable_key=f"styleable_add_button_{i}", key=f"add_button_{i}", use_container_width=True
                )
            if need_add_folder:
                add_folder(i, folder_path_format="folder_path_{}", display_name_format="display_name_{}")
            if need_remove_folder and num_folders > 1:
                remove_folder(i, folder_path_format="folder_path_{}", display_name_format="display_name_{}")
            if i < num_folders:
                st.text_input(f"Folder Path", key=f"folder_path_{i}")
            else:
                st.text_input(f"Folder Path", key=f"folder_path_{i}", value="", disabled=True)
            kwargs = {}
            if i == num_folders:
                kwargs["value"] = ""
            st.text_input(f"Display Name", key=f"display_name_{i}", disabled=i == num_folders, **kwargs)

    for i in range(page_id * num_samples_per_page, min((page_id + 1) * num_samples_per_page, len(file_names))):
        file_name = file_names[i]
        with st.container(border=True):
            cols = st.columns([MEDIA_COLUMN_WIDTH] * num_folders + [1], vertical_alignment="bottom")
            for j in range(num_folders):
                col = cols[j]
                with col:
                    dirpath = dirpaths[j].strip()
                    display_name = display_names[j]
                    if display_name == "":
                        display_name = dirpath
                    with st.container():
                        if dirpath != "" and os.path.isdir(dirpath):
                            matched_file = match_file(dirpath, file_name)
                            if matched_file.endswith(IMAGE_EXTENSIONS):
                                st.image(
                                    os.path.join(dirpath, matched_file), caption=display_name, use_container_width=True
                                )
                            else:
                                st.video(
                                    os.path.join(dirpath, match_file(dirpath, file_name)), loop=True, autoplay=True
                                )
                    caption = get_caption(captions, file_name)
            if caption is None:
                st.markdown(f"**{file_name}**")
            else:
                st.markdown(f"**{file_name}**: {caption}")

    # Page Number
    start_item = page_id * num_samples_per_page + 1
    end_item = min((page_id + 1) * num_samples_per_page, len(file_names))
    st.write(f"Page {page_id + 1} of {max_page_id} ({start_item}-{end_item} items, in total {len(file_names)})")
    col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 4], vertical_alignment="bottom")
    with col2:
        button = st.button("Previous", key="previous_button", disabled=page_id == 0, use_container_width=True)
        if button:
            st.session_state["page_id"] = st.session_state["page_id"] - 1
            st.rerun()
    with col3:
        input_page_id = st.number_input("Page Number", min_value=1, max_value=max_page_id, value=page_id + 1)
        if input_page_id != st.session_state["page_id"] + 1:
            st.session_state["page_id"] = input_page_id - 1
            st.rerun()
    with col4:
        button = st.button("Next", key="next_button", disabled=page_id == max_page_id - 1, use_container_width=True)
        if button:
            st.session_state["page_id"] = st.session_state["page_id"] + 1
            st.rerun()


if __name__ == "__main__":
    main()
