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
            reference = [reference for reference in data.get('reference', {}).get('value').split(' | ')], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
        
@dataclass
class Software:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    reference: Optional[List] = field(default_factory=list)
    benchmarks: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Software':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            reference = [reference for reference in data.get('reference', {}).get('value').split(' | ')],
            benchmarks =  [Relatant.from_query(benchmark) for benchmark in data.get('benchmark', {}).get('value', '').split(" / ") if benchmark] if 'benchmark' in data else [], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class AlgorithmicProblem:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    benchmarks: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'AlgorithmicProblem':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            specializes = [Relatant.from_query(specializes) for specializes in data.get('specializes', {}).get('value', '').split(" / ") if specializes] if 'specializes' in data else [], 
            specializedBy = [Relatant.from_query(specializedBy) for specializedBy in data.get('specializedBy', {}).get('value', '').split(" / ") if specializedBy] if 'specializedBy' in data else [], 
            benchmarks =  [Relatant.from_query(benchmark) for benchmark in data.get('benchmark', {}).get('value', '').split(" / ") if benchmark] if 'benchmark' in data else [], 
        )
    
@dataclass
class Algorithm:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    properties : Optional[List] = field(default_factory=list)
    componentOf: Optional[List[Relatant]] = field(default_factory=list)
    hasComponent: Optional[List[Relatant]] = field(default_factory=list)
    subclassOf: Optional[List[Relatant]] = field(default_factory=list)
    hasSubclass: Optional[List[Relatant]] = field(default_factory=list)
    relatedTo: Optional[List[Relatant]] = field(default_factory=list)
    problems: Optional[List[Relatant]] = field(default_factory=list)
    softwares: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'AlgorithmicProblem':

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
            problems =  [Relatant.from_query(problem) for problem in data.get('problem', {}).get('value', '').split(" / ") if problem] if 'problem' in data else [], 
            softwares =  [Relatant.from_query(software) for software in data.get('software', {}).get('value', '').split(" / ") if software] if 'software' in data else [], 
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )