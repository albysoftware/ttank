import json
import pyzipper

from typing import (
    Any
)
from datetime import (
    datetime
)

class LibraryInterface:
    def __init__(
        self,
        zip_path: str,
        password: str
    ) -> None:
        self.zip_path: str = zip_path
        self.password: bytes = password.encode()

    @classmethod
    def init_library(cls, zip_path: str, password: str) -> LibraryInterface:
        empty_index = {
            "creation_date": datetime.now().isoformat()
        }
        index_content = json.dumps(empty_index, indent = 4)

        with pyzipper.AESZipFile(
            zip_path,
            "w",
            **LibraryInterface._get_write_kwargs()
        ) as zip_file:
            zip_file.setpassword(password.encode())

            zip_file.writestr("./system/index.json", index_content.encode())
            zip_file.writestr("./system/cache/", b"")
        
        return LibraryInterface(zip_path, password)

    @classmethod
    def _get_write_kwargs(cls) -> dict[str, Any]:
        return {
            "compression": pyzipper.ZIP_LZMA,
            "encryption": pyzipper.WZ_AES
        }

    def read_file(self, file_path: str) -> str:
        with pyzipper.AESZipFile(self.zip_path, "r") as zip_file:
            zip_file.setpassword(self.password)
            with zip_file.open(file_path) as file:
                return file.read().decode()
    
    def write_file(self, file_path: str, content: str) -> None:
        with pyzipper.AESZipFile(
            self.zip_path,
            "w",
            **self._get_write_kwargs()
        ) as zip_file:
            zip_file.setpassword(self.password)
            zip_file.writestr(file_path, content.encode())
    
    def get_index(self) -> Any:
        return self.read_file("./system/index.json")
