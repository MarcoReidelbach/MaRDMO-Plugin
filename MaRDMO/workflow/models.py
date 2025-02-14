from dataclasses import dataclass, field
from typing import List, Optional

from ..id import *
from ..utils import get_data

from .constants import reference_order_software

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
    
    @classmethod
    def from_msc(cls, id: str, label: str, description: str) -> 'Relatant':

        return cls(
            id = f"msc:{id}",
            label = label,
            description = description,
        )
    
@dataclass
class MRelatant:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    
    @classmethod
    def from_query(cls, raw: str) -> 'MRelatant':

        id_mathalgodb = ''
        id_general, label, description, link = raw.split(" | ")

        if link and link.startswith('https://mardi4nfdi.de/mathalgodb/0.1/algorithm#'):
            _, id_mathalgodb = link.split('#')

        return cls(
            id = f"mathalgodb:{id_mathalgodb}" if id_mathalgodb else id_general,
            label = label,
            description = description,
        )
    
@dataclass
class ProcessStep:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    inputDataSet: Optional[List[Relatant]] = field(default_factory=list)
    outputDataSet: Optional[List[Relatant]] = field(default_factory=list)
    uses: Optional[List[Relatant]] = field(default_factory=list)
    platformSoftware: Optional[List[Relatant]] = field(default_factory=list)
    platformInstrument: Optional[List[Relatant]] = field(default_factory=list)
    fieldOfWork: Optional[List[Relatant]] = field(default_factory=list)
    mscID: Optional[List[Relatant]] = field(default_factory=list)

    
    @classmethod
    def from_query(cls, raw_data: List) -> 'ProcessStep':

        data = raw_data[0]
        
        # Load MSC Classification
        msc = get_data('data/msc2020.json')

        return cls(
            id = None,
            label = None,
            description = None,
            inputDataSet = [Relatant.from_query(input) for input in data.get('inputDataSet', {}).get('value', '').split(" / ") if input] if 'inputDataSet' in data else [],
            outputDataSet = [Relatant.from_query(output) for output in data.get('outputDataSet', {}).get('value', '').split(" / ") if output] if 'outputDataSet' in data else [],
            uses = [MRelatant.from_query(algorithm) for algorithm in data.get('uses', {}).get('value', '').split(" / ") if algorithm] if 'uses' in data else [], 
            platformSoftware = [Relatant.from_query(software) for software in data.get('platformSoftware', {}).get('value', '').split(" / ") if software] if 'platformSoftware' in data else [],
            platformInstrument = [Relatant.from_query(instrument) for instrument in data.get('platformInstrument', {}).get('value', '').split(" / ") if instrument] if 'platformInstrument' in data else [], 
            fieldOfWork = [Relatant.from_query(field) for field in data.get('fieldOfWork', {}).get('value', '').split(" / ") if field] if 'fieldOfWork' in data else [],
            mscID = [Relatant.from_msc(mscID, next((key for key, value in msc.items() if value['id'] == mscID), None), next((value['quote'] for key, value in msc.items() if value['id'] == mscID), None)) for mscID in data.get('mscID', {}).get('value', '').split(" / ") if mscID] if 'mscID' in data else [],
        )

@dataclass
class Method:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    implementedBySoftware: Optional[List[Relatant]] = field(default_factory=list)
    implementedByInstrument: Optional[List[Relatant]] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: List) -> 'ProcessStep':

        data = raw_data[0]
        
        return cls(
            id = None,
            label = None,
            description = None,
            implementedBySoftware = [Relatant.from_query(software) for software in data.get('implementedBySoftware', {}).get('value', '').split(" / ") if field] if 'implementedBySoftware' in data else [],
            implementedByInstrument = [Relatant.from_query(software) for software in data.get('implementedByInstrument', {}).get('value', '').split(" / ") if field] if 'implementedByInstrument' in data else [] 
        )
    
@dataclass
class Software:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    sourceCodeRepository: Optional[str]
    userManualURL: Optional[str]
    reference: Optional[List] = field(default_factory=list)
    programmedIn: Optional[List[Relatant]] = field(default_factory=list)
    dependsOnSoftware: Optional[List[Relatant]] = field(default_factory=list)
    
    @classmethod
    def from_query(cls, raw_data: dict) -> 'Software':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            sourceCodeRepository = data.get('sourceCodeRepository', {}).get('value', '') ,
            userManualURL = data.get('userManualURL', {}).get('value', ''),
            reference = {reference_order_software[key][0]: [reference_order_software[key][1], value] for part in data.get('reference', {}).get('value', '').split(' | ') if (key := part.split(':')[0]) in reference_order_software and (value := part.split(':')[1])} | ({reference_order_software['url'][0]: [reference_order_software['url'][1], url]} if (url := next((part for part in data.get('reference', {}).get('value', '').split(' | ') if part.startswith('https://')), None)) else {}),
            programmedIn =  [Relatant.from_query(language) for language in data.get('programmedIn', {}).get('value', '').split(" / ") if language] if 'programmedIn' in data else [], 
            dependsOnSoftware = [Relatant.from_query(software) for software in data.get('dependsOnSoftware', {}).get('value', '').split(" / ") if software] if 'dependsOnSoftware' in data else []
        )
    
@dataclass
class Hardware:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    nodes: Optional[str]
    cores: Optional[str]
    CPU: Optional[List[Relatant]] = field(default_factory=list)
    
    @classmethod
    def from_query(cls, raw_data: dict) -> 'Hardware':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None, 
            nodes = data.get('nodes', {}).get('value', ''),
            cores = data.get('cores', {}).get('value', ''),
            CPU = [Relatant.from_query(cpu) for cpu in data.get('CPU', {}).get('value', '').split(" / ") if cpu] if 'CPU' in data else []
        )



