from dataclasses import dataclass, field
from typing import List, Optional

from ..adders import add_reference_order
from ..models import Relatant

@dataclass
class Benchmark:
    '''Data Class For Benchmark Item'''
    reference: Optional[List] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Benchmark':

        data = raw_data[0]
        order = add_reference_order('benchmark')

        return cls(
            reference = {order[key][0]: [order[key][1], value] for part in data.get('reference', {}).get('value', '').split(' | ') if (key := part.split(':')[0]) in order and (value := part.split(':')[1])} | ({order['url'][0]: [order['url'][1], url]} if (url := next((part for part in data.get('reference', {}).get('value', '').split(' | ') if part.startswith('https://')), None)) else {}),
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
        
@dataclass
class Software:
    reference: Optional[List] = field(default_factory=list)
    tests: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Software':

        data = raw_data[0]
        order = add_reference_order('software')

        return cls(
            reference = {order[key][0]: [order[key][1], value] for part in data.get('reference', {}).get('value', '').split(' | ') if (key := part.split(':')[0]) in order and (value := part.split(':')[1])} | ({order['url'][0]: [order['url'][1], url]} if (url := next((part for part in data.get('reference', {}).get('value', '').split(' | ') if part.startswith('https://')), None)) else {}),
            tests =  [Relatant.from_query(benchmark) for benchmark in data.get('tests', {}).get('value', '').split(" / ") if benchmark] if 'tests' in data else [], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class Problem:
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    instantiates: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Problem':

        data = raw_data[0]

        return cls(
            specializes = [Relatant.from_query(specializes) for specializes in data.get('specializes', {}).get('value', '').split(" / ") if specializes] if 'specializes' in data else [], 
            specializedBy = [Relatant.from_query(specializedBy) for specializedBy in data.get('specializedBy', {}).get('value', '').split(" / ") if specializedBy] if 'specializedBy' in data else [], 
            instantiates =  [Relatant.from_query(benchmark) for benchmark in data.get('instantiates', {}).get('value', '').split(" / ") if benchmark] if 'instantiates' in data else [], 
        )
    
@dataclass
class Algorithm:
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
            componentOf = [Relatant.from_query(componentOf) for componentOf in data.get('componentOf', {}).get('value', '').split(" / ") if componentOf] if 'componentOf' in data else [], 
            hasComponent = [Relatant.from_query(hasComponent) for hasComponent in data.get('hasComponent', {}).get('value', '').split(" / ") if hasComponent] if 'hasComponent' in data else [], 
            subclassOf = [Relatant.from_query(subclassOf) for subclassOf in data.get('subclassOf', {}).get('value', '').split(" / ") if subclassOf] if 'subclassOf' in data else [], 
            hasSubclass = [Relatant.from_query(hasSubclass) for hasSubclass in data.get('hasSubclass', {}).get('value', '').split(" / ") if hasSubclass] if 'hasSubclass' in data else [], 
            relatedTo = [Relatant.from_query(relatedTo) for relatedTo in data.get('relatedTo', {}).get('value', '').split(" / ") if relatedTo] if 'relatedTo' in data else [], 
            solves =  [Relatant.from_query(problem) for problem in data.get('solves', {}).get('value', '').split(" / ") if problem] if 'solves' in data else [], 
            implementedBy =  [Relatant.from_query(software) for software in data.get('implementedBy', {}).get('value', '').split(" / ") if software] if 'implementedBy' in data else [], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )