from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

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


    def __str__(self) -> str:
        return self.name


nop = ConfigOp('nop', lambda c: c)


def set_op(attr: str, value: Any) -> ConfigOp:
    return ConfigOp(
        '{} = {}'.format(attr, value),
        lambda c: c.set(attr, value)
    )


def set_ops(values) -> ConfigOp:
    if len(values) == 0:
        return nop
    op = set_op(values[0][0], values[0][1])
    for v in values[1:]:
        op = op + set_op(v[0], v[1])
    return op
