'''Module containing general Models for MaRDMO'''

from dataclasses import dataclass
from typing import Optional

@dataclass
class Relatant:
    '''Data Class For Relatant Items'''
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]

    @classmethod
    def from_query(cls, raw: str) -> 'Relatant':
        '''Generate Item From Query'''
        identifier, label, description = raw.split(" | ")
        return cls(
            id = identifier,
            label = label,
            description = description,
        )

    @classmethod
    def from_triple(cls, identifier: str, label: str, description: str) -> 'Relatant':
        '''Generate Item From Triple'''
        return cls(
            id = identifier,
            label = label,
            description = description,
        )

    @classmethod
    def from_msc(cls, identifier: str, label: str, description: str) -> 'Relatant':
        '''Generate Item from MSC'''
        return cls(
            id = f"msc:{identifier}",
            label = label,
            description = description,
        )

@dataclass
class RelatantWithClass:
    '''Data Class For Relatant Items With Class'''
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    item_class: Optional[str]

    @classmethod
    def from_query(cls, raw: str) -> 'RelatantWithClass':
        '''Generate Item From Query'''
        raw_split = raw.split(" | ")
        if len(raw_split) == 3:
            item_class = None
        else:
            item_class = raw_split[3]
        return cls(
            id = raw_split[0],
            label = raw_split[1],
            description = raw_split[2],
            item_class = item_class
        )
