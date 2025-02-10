from dataclasses import dataclass, field
from typing import List, Optional

from .constants import reference_order_benchmark, reference_order_software

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
    
    @classmethod
    def from_relation(cls, id: str, label: str, description: str) -> 'Relatant':

        return cls(
            id = id,
            label = label,
            description = description,
        )

@dataclass
class Benchmark:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    reference: Optional[List] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Benchmark':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            reference = {reference_order_benchmark[key][0]: [reference_order_benchmark[key][1], value] for part in data.get('reference', {}).get('value', '').split(' | ') if (key := part.split(':')[0]) in reference_order_benchmark and (value := part.split(':')[1])} | ({reference_order_benchmark['url'][0]: [reference_order_benchmark['url'][1], url]} if (url := next((part for part in data.get('reference', {}).get('value', '').split(' | ') if part.startswith('https://')), None)) else {}),
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
        
@dataclass
class Software:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    reference: Optional[List] = field(default_factory=list)
    tests: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Software':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            reference = {reference_order_software[key][0]: [reference_order_software[key][1], value] for part in data.get('reference', {}).get('value', '').split(' | ') if (key := part.split(':')[0]) in reference_order_software and (value := part.split(':')[1])} | ({reference_order_software['url'][0]: [reference_order_software['url'][1], url]} if (url := next((part for part in data.get('reference', {}).get('value', '').split(' | ') if part.startswith('https://')), None)) else {}),
            tests =  [Relatant.from_query(benchmark) for benchmark in data.get('tests', {}).get('value', '').split(" / ") if benchmark] if 'tests' in data else [], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class Problem:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    instantiates: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Problem':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            specializes = [Relatant.from_query(specializes) for specializes in data.get('specializes', {}).get('value', '').split(" / ") if specializes] if 'specializes' in data else [], 
            specializedBy = [Relatant.from_query(specializedBy) for specializedBy in data.get('specializedBy', {}).get('value', '').split(" / ") if specializedBy] if 'specializedBy' in data else [], 
            instantiates =  [Relatant.from_query(benchmark) for benchmark in data.get('instantiates', {}).get('value', '').split(" / ") if benchmark] if 'instantiates' in data else [], 
        )
    
@dataclass
class Algorithm:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    componentOf: Optional[List[Relatant]] = field(default_factory=list)
    hasComponent: Optional[List[Relatant]] = field(default_factory=list)
    subclassOf: Optional[List[Relatant]] = field(default_factory=list)
    hasSubclass: Optional[List[Relatant]] = field(default_factory=list)
    relatedTo: Optional[List[Relatant]] = field(default_factory=list)
    solves: Optional[List[Relatant]] = field(default_factory=list)
    implementedBy: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Algorithm':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            componentOf = [Relatant.from_query(componentOf) for componentOf in data.get('componentOf', {}).get('value', '').split(" / ") if componentOf] if 'componentOf' in data else [], 
            hasComponent = [Relatant.from_query(hasComponent) for hasComponent in data.get('hasComponent', {}).get('value', '').split(" / ") if hasComponent] if 'hasComponent' in data else [], 
            subclassOf = [Relatant.from_query(subclassOf) for subclassOf in data.get('subclassOf', {}).get('value', '').split(" / ") if subclassOf] if 'subclassOf' in data else [], 
            hasSubclass = [Relatant.from_query(hasSubclass) for hasSubclass in data.get('hasSubclass', {}).get('value', '').split(" / ") if hasSubclass] if 'hasSubclass' in data else [], 
            relatedTo = [Relatant.from_query(relatedTo) for relatedTo in data.get('relatedTo', {}).get('value', '').split(" / ") if relatedTo] if 'relatedTo' in data else [], 
            solves =  [Relatant.from_query(problem) for problem in data.get('solves', {}).get('value', '').split(" / ") if problem] if 'solves' in data else [], 
            implementedBy =  [Relatant.from_query(software) for software in data.get('implementedBy', {}).get('value', '').split(" / ") if software] if 'implementedBy' in data else [], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )