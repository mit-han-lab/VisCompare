import streamlit as st
from streamlit_extras.stylable_container import stylable_container


def remove_button(*args, **kwargs):
    with stylable_container(
        key=kwargs.pop("styleable_key"),
        css_styles=f"button {{background-color: IndianRed; color: white; border-radius: 20px; "
        f"opacity: {0.5 if kwargs.get('disabled', False) else 1}}}",
    ):
        return st.button(*args, label="Remove", **kwargs)


def browse_button(*args, **kwargs):
    kwargs["disabled"] = True
    with stylable_container(
        key=kwargs.pop("styleable_key"),
        css_styles=f"button {{background-color: #FAEBD7; color: black; border-radius: 20px; "
        f"opacity: {0.5 if kwargs.get('disabled', False) else 1}}}",
    ):
        return st.button(*args, label="Browse", **kwargs)


def reorder_button(*args, **kwargs):
    with stylable_container(
        key=kwargs.pop("styleable_key"),
        css_styles=f"button {{background-color: LightBlue; color: black; "
        f"opacity: {0.5 if kwargs.get('disabled', False) else 1}}}",
    ):
        return st.button(*args, label="Reorder", **kwargs)


def add_button(*args, **kwargs):
    with stylable_container(
        key=kwargs.pop("styleable_key"),
        css_styles=f"button {{background-color: #3CB371; color: white; border-radius: 20px; "
        f"opacity: {0.5 if kwargs.get('disabled', False) else 1};}}",
    ):
        return st.button(*args, label="Add", **kwargs)


def save_button(*args, **kwargs):
    with stylable_container(
        key=kwargs.pop("styleable_key"),
        css_styles=f"button {{background-color: #77dd77; color: black; border-radius: 20px; "
        f"opacity: {0.5 if kwargs.get('disabled', False) else 1};}}",
    ):
        return st.button(*args, label="Save", **kwargs)


def load_button(*args, **kwargs):
    with stylable_container(
        key=kwargs.pop("styleable_key"),
        css_styles=f"button {{background-color: #aec6cf; color: black; border-radius: 20px; "
        f"opacity: {0.5 if kwargs.get('disabled', False) else 1};}}",
    ):
        return st.button(*args, label="Load", **kwargs)
