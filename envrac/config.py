from dataclasses import dataclass


@dataclass
class Config:
    discovery_mode: bool = False
    print_values: bool = False

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
