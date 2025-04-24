import os

from . import VALID_PICTURE_EXTENSIONS


class FileValidator:

    def __init__(self,filename:str):
        self.filename = filename


    def check_is_valid_image(self) -> bool:
        return os.path.splitext(self.filename)[1] in VALID_PICTURE_EXTENSIONS
