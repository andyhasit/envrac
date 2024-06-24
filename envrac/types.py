from enum import Enum


class ValueType(Enum):
    bool = "bool"
    date = "date"
    datetime = "datetime"
    int = "int"
    float = "float"
    str = "str"
    time = "time"

    def __str__(self):
        return str(self.value)
