import os, json

from dataclasses import dataclass
from typing import List, Optional

from ..id import *

@dataclass
class ModelProperties:
    Time: Optional[str]
    Space: Optional[str]
    
    @classmethod
    def from_query(cls, raw_data: List) -> 'ModelProperties':

        data = raw_data[0]

        return cls(
            Time = data.get('time', {}).get('value'),
            Space = data.get('space', {}).get('value'),
        )
    
@dataclass
class Variables:
    ID: Optional[str]
    Name: Optional[str]
    Unit: Optional[str]
    Symbol: Optional[str]
    Task: Optional[str]
    Type: Optional[str]
    
    @classmethod
    def from_query(cls, data: List) -> 'Variables':

        return cls(
            ID = f"mathmoddb:{data.get('ID', {}).get('value')}",
            Name = data.get('Name', {}).get('value'),
            Unit = data.get('Unit', {}).get('value'),
            Symbol = f"$${data.get('Symbol', {}).get('value')}$$",
            Task = data.get('label', {}).get('value'),
            Type = data.get('Type', {}).get('value')
        )
    
@dataclass
class Parameters:
    Name: Optional[str]
    Unit: Optional[str]
    Symbol: Optional[str]
    Task: Optional[str]
    
    @classmethod
    def from_query(cls, data: List) -> 'Parameters':

        return cls(
            Name = data.get('Name', {}).get('value'),
            Unit = data.get('Unit', {}).get('value'),
            Symbol = f"$${data.get('Symbol', {}).get('value')}$$",
            Task = data.get('label', {}).get('value')
        )