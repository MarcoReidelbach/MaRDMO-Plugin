import re
from dataclasses import dataclass, field
from typing import List, Optional

from .constants import order_to_publish

from ..adders import add_reference_order
from ..getters import get_data, get_options
from ..models import Relatant

@dataclass
class ModelProperties:
    Time: Optional[str]
    Space: Optional[str]
    
    @classmethod
    def from_query(cls, raw_data: List) -> 'ModelProperties':

        data = raw_data[0]

        Time = ''
        if data.get('isTimeContinuous', {}).get('value') == 'True':
            Time = 'continuous'
        elif data.get('isTimeDiscrete', {}).get('value') == 'True':
            Time = 'discrete'

        Space = ''
        if data.get('isSpaceContinuous', {}).get('value') == 'True':
            Space = 'continuous'
        elif data.get('isSpaceDiscrete', {}).get('value') == 'True':
            Space = 'discrete'

        return cls(
            Time = Time,
            Space = Space,
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
            ID = data.get('ID', {}).get('value'),
            Name = data.get('Name', {}).get('value'),
            Unit = data.get('Unit', {}).get('value'),
            Symbol = re.sub(r'(<math\b(?![^>]*\bdisplay=)[^>]*)(>)', r'\1 display="inline"\2', data.get('Symbol', {}).get('value')),
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
            Symbol = re.sub(r'(<math\b(?![^>]*\bdisplay=)[^>]*)(>)', r'\1 display="inline"\2', data.get('Symbol', {}).get('value')),
            Task = data.get('label', {}).get('value')
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
        order = add_reference_order('software')

        return cls(
            id = None,
            label = None,
            description = None,
            sourceCodeRepository = data.get('sourceCodeRepository', {}).get('value', '') ,
            userManualURL = data.get('userManualURL', {}).get('value', ''),
            reference = {order[key][0]: [order[key][1], value] for part in data.get('reference', {}).get('value', '').split(' | ') if (key := part.split(':')[0]) in order and (value := part.split(':')[1])} | ({order['url'][0]: [order['url'][1], url]} if (url := next((part for part in data.get('reference', {}).get('value', '').split(' | ') if part.startswith('https://')), None)) else {}),
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

@dataclass
class DataSet:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    size: Optional[List]
    fileFormat: Optional[str]
    binaryOrText: Optional[str]
    proprietary: Optional[str]
    reference: Optional[List]
    toArchive: Optional[List]
    dataType: Optional[List[Relatant]] = field(default_factory=list)
    representationFormat: Optional[List[Relatant]] = field(default_factory=list)
    
    @classmethod
    def from_query(cls, raw_data: dict) -> 'DataSet':

        # Load MSC Classification
        options = get_options()

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            size = [] if '' in (temp := [options[data['sizeUnit']['value']] if data.get('sizeUnit', {}).get('value', '') else options['items'] if data.get('sizeRecord', {}).get('value', '') else '', data['sizeValue']['value'] if data.get('sizeValue', {}).get('value', '') else data['sizeRecord']['value'] if data.get('sizeRecord', {}).get('value', '') else '']) else temp,
            fileFormat = data.get('fileFormat', {}).get('value'),
            binaryOrText = options[data['binaryOrText']['value']] if data.get('binaryOrText', {}).get('value') else '',
            proprietary = options[data['proprietary']['value']] if data.get('proprietary', {}).get('value') else '',
            reference = ({order_to_publish()[data['publish']['value']][0]: [order_to_publish()[data['publish']['value']][1], '']} if data.get('publish', {}).get('value') else {}) | ({order_to_publish()['doi'][0]: [order_to_publish()['doi'][1], data['DOI']['value']]} if data.get('DOI', {}).get('value') else {}) | ({order_to_publish()['url'][0]: [order_to_publish()['url'][1], data['URL']['value']]} if data.get('URL', {}).get('value') else {}),
            toArchive = (temp := [options[data['archive']['value']] if data.get('archive', {}).get('value') else '',data.get('endTime', {}).get('value', '')[:4] if data.get('endTime', {}).get('value') else '']) and temp if temp[0] != '' else [],
            dataType = [Relatant.from_query(dtype) for dtype in data.get('dataType', {}).get('value', '').split(" / ") if dtype] if 'dataType' in data else [],
            representationFormat = [Relatant.from_query(rformat) for rformat in data.get('representationFormat', {}).get('value', '').split(" / ") if rformat] if 'representationFormat' in data else [] 
        )



