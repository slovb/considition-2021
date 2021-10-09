from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from .config import Config

@dataclass(frozen=True)
class ConfigOp:
    name: str
    action: Callable[[Config], Config]
    
    def __add__(self, other) -> ConfigOp:
        return ConfigOp(
            '{}, {}'.format(self.name, other.name),
            lambda c: self.action(other.action(c))
        )


nop = ConfigOp('nop', lambda c: c)


def set_op(attr: str, value) -> ConfigOp:
    return ConfigOp(
        'set {} = {}'.format(attr, value),
        lambda c: c.set(attr, value)
    )
