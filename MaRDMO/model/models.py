from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Relatant:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    
    @classmethod
    def from_query(cls, raw: str) -> 'Relatant':

        id, label, description = raw.split(" | ")

        return cls(
            id = id,
            label = label,
            description = description,
        )

@dataclass
class ResearchField:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    generalizedByField: Optional[List[Relatant]] = field(default_factory=list)
    generalizesField: Optional[List[Relatant]] = field(default_factory=list)
    similarToField: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'ResearchField':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            generalizedByField = [Relatant.from_query(field) for field in data.get('generalizedByField', {}).get('value', '').split(" / ") if field] if 'generalizedByField' in data else [],
            generalizesField = [Relatant.from_query(field) for field in data.get('generalizesField', {}).get('value', '').split(" / ") if field] if 'generalizesField' in data else [],
            similarToField = [Relatant.from_query(field) for field in data.get('similarToField', {}).get('value', '').split(" / ") if field] if 'similarToField' in data else [],            
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )