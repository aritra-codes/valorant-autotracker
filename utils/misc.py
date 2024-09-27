from typing import Any

from customtkinter import CTkImage
from PIL import Image

from utils.path import get_resource_path

def get_key_from_value(dictionary: dict, value: Any) -> Any:
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

def get_pillow_image(relative_path: str) -> Image.Image:
    return Image.open(get_resource_path(relative_path))

def get_ctk_image(light_path: str, dark_path: str) -> CTkImage:
    return CTkImage(get_pillow_image(light_path), get_pillow_image(dark_path))