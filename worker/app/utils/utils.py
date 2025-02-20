import os
from typing import Tuple


def separate_path_and_name(file_path: str) -> Tuple[str, str]:
    path = os.path.dirname(file_path)
    name = os.path.basename(file_path).split('.')[0]
    return path, name
