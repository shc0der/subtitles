from enum import Enum


class InfoStatus(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"
