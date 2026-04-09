'''Data models for the Workflow Documentation module.'''

import re
from dataclasses import dataclass, field
from typing import Optional

from .constants import software_reference_ids
from .utils import get_archive, get_reference, get_size

from ..getters import get_data, get_options
from ..helpers import split_value
from ..models import Relatant

# Reverse lookup for MSC 2020: {msc_id: (label, quote)} — built once at import time.
# get_data is lru_cached so the JSON is read from disk only once.
_MSC_BY_ID: dict = {
    entry['id']: (label, entry['quote'])
    for label, entry in get_data('data/msc2020.json').items()
}


@dataclass
class ModelProperties:
    '''Properties (time/space discretisation) of a mathematical model.'''

    time: Optional[str] = None
    space: Optional[str] = None

    @classmethod
    def from_query(cls, raw_data: list) -> 'ModelProperties':
        '''Parse a single SPARQL result row into a ModelProperties instance.'''
        data = raw_data[0]

        if data.get('isTimeContinuous', {}).get('value') == 'True':
            time = 'continuous'
        elif data.get('isTimeDiscrete', {}).get('value') == 'True':
            time = 'discrete'
        else:
            time = ''

        if data.get('isSpaceContinuous', {}).get('value') == 'True':
            space = 'continuous'
        elif data.get('isSpaceDiscrete', {}).get('value') == 'True':
            space = 'discrete'
        else:
            space = ''

        return cls(
            time = time,
            space = space,
        )


@dataclass
class Variables:
    '''A single variable entry from MathModDB.'''

    identifier: Optional[str] = None
    name: Optional[str] = None
    unit: Optional[str] = None
    symbol: Optional[str] = None
    task: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_query(cls, data: dict) -> 'Variables':
        '''Parse one SPARQL result row into a Variables instance.'''

        variables = {
            # Identifier of Variable
            'identifier': data.get('ID', {}).get('value'),
            # Name of Variable
            'name': data.get('Name', {}).get('value'),
            # Unit of Variable
            'unit': data.get('Unit', {}).get('value'),
            # Symbol of Variable
            'symbol': re.sub(
                r'(<math\b(?![^>]*\bdisplay=)[^>]*)(>)',
                r'\1 display="inline"\2',
                data.get('Symbol', {}).get('value'),
            ),
            # Task Variable is Part Of
            'task': data.get('label', {}).get('value'),
            # Role of Variable in Task (Input/Output)
            'type': data.get('Type', {}).get('value'),
        }

        return cls(
            **variables
        )


@dataclass
class Parameters:
    '''A single parameter entry from MathModDB.'''

    identifier: Optional[str] = None
    name: Optional[str] = None
    unit: Optional[str] = None
    symbol: Optional[str] = None
    task: Optional[str] = None

    @classmethod
    def from_query(cls, data: dict) -> 'Parameters':
        '''Parse one SPARQL result row into a Parameters instance.'''

        parameters = {
            # Identifier of Parameter
            'identifier': data.get('ID', {}).get('value'),
            # Name of Parameter
            'name': data.get('Name', {}).get('value'),
            # Unit of Parameter
            'unit': data.get('Unit', {}).get('value'),
            # Symbol of Parameter
            'symbol': re.sub(
                r'(<math\b(?![^>]*\bdisplay=)[^>]*)(>)',
                r'\1 display="inline"\2',
                data.get('Symbol', {}).get('value'),
            ),
            # Task Parameter is Part Of
            'task': data.get('label', {}).get('value'),
        }

        return cls(
            **parameters
        )


@dataclass
class ProcessStep:
    '''Relations of a Process Step entity from MaRDI/Wikidata.'''

    input_data_set: list[Relatant] = field(default_factory=list)
    output_data_set: list[Relatant] = field(default_factory=list)
    uses: list[Relatant] = field(default_factory=list)
    platform_software: list[Relatant] = field(default_factory=list)
    platform_instrument: list[Relatant] = field(default_factory=list)
    field_of_work: list[Relatant] = field(default_factory=list)
    msc_id: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: list) -> 'ProcessStep':
        '''Parse a single-item SPARQL result (backward-compatible).'''
        return cls.from_query_single(raw_data[0])

    @classmethod
    def from_query_batch(cls, raw_data: list) -> 'dict[str, ProcessStep]':
        '''Parse a batch SPARQL result into {external_id: instance} dict.'''
        return {
            row['qid']['value']: cls.from_query_single(row)
            for row in raw_data
            if row.get('qid', {}).get('value')
        }

    @classmethod
    def from_query_single(cls, data: dict) -> 'ProcessStep':
        '''Parse one SPARQL result row into a ProcessStep instance.'''
        return cls(
            input_data_set=split_value(
                data=data, key='input_data_set', transform=Relatant.from_query
            ),
            output_data_set=split_value(
                data=data, key='output_data_set', transform=Relatant.from_query
            ),
            uses=split_value(
                data=data, key='uses', transform=Relatant.from_query
            ),
            platform_software=split_value(
                data=data, key='platform_software', transform=Relatant.from_query
            ),
            platform_instrument=split_value(
                data=data, key='platform_instrument', transform=Relatant.from_query
            ),
            field_of_work=split_value(
                data=data, key='field_of_work', transform=Relatant.from_query
            ),
            msc_id=[
                Relatant.from_msc(msc_id, *_MSC_BY_ID[msc_id])
                for msc_id in split_value(data, 'msc_id')
                if msc_id in _MSC_BY_ID
            ],
        )


@dataclass
class Method:
    '''Relations of a Method entity from MaRDI/Wikidata.'''

    implemented_by_software: list[Relatant] = field(default_factory=list)
    implemented_by_instrument: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: list) -> 'Method':
        '''Parse a single-item SPARQL result (backward-compatible).'''
        return cls.from_query_single(raw_data[0])

    @classmethod
    def from_query_batch(cls, raw_data: list) -> 'dict[str, Method]':
        '''Parse a batch SPARQL result into {external_id: instance} dict.'''
        return {
            row['qid']['value']: cls.from_query_single(row)
            for row in raw_data
            if row.get('qid', {}).get('value')
        }

    @classmethod
    def from_query_single(cls, data: dict) -> 'Method':
        '''Parse one SPARQL result row into a Method instance.'''
        return cls(
            implemented_by_software=split_value(
                data=data, key='implemented_by_software', transform=Relatant.from_query
            ),
            implemented_by_instrument=split_value(
                data=data, key='implemented_by_instrument', transform=Relatant.from_query
            ),
        )


@dataclass
class Software:
    '''References and relations of a Software entity from MaRDI/Wikidata.'''

    reference: dict[int, list[str]] = field(default_factory=dict)
    programmed_in: list[Relatant] = field(default_factory=list)
    depends_on_software: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Software':
        '''Parse a single-item SPARQL result (backward-compatible).'''
        return cls.from_query_single(raw_data[0])

    @classmethod
    def from_query_batch(cls, raw_data: list) -> 'dict[str, Software]':
        '''Parse a batch SPARQL result into {external_id: instance} dict.'''
        return {
            row['qid']['value']: cls.from_query_single(row)
            for row in raw_data
            if row.get('qid', {}).get('value')
        }

    @classmethod
    def from_query_single(cls, data: dict) -> 'Software':
        '''Parse one SPARQL result row into a Software instance.'''
        options = get_options()

        return cls(
            reference={
                idx: [options[prop], data[prop]['value']]
                for idx, prop in enumerate(software_reference_ids)
                if data.get(prop, {}).get('value')
            },
            programmed_in=split_value(
                data=data, key='programmed_in', transform=Relatant.from_query
            ),
            depends_on_software=split_value(
                data=data, key='depends_on_software', transform=Relatant.from_query
            ),
        )


@dataclass
class Hardware:
    '''Node/core counts and CPU relations of a Hardware entity.'''

    nodes: Optional[str] = None
    cores: Optional[str] = None
    cpu: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Hardware':
        '''Parse a single-item SPARQL result (backward-compatible).'''
        return cls.from_query_single(raw_data[0])

    @classmethod
    def from_query_batch(cls, raw_data: list) -> 'dict[str, Hardware]':
        '''Parse a batch SPARQL result into {external_id: instance} dict.'''
        return {
            row['qid']['value']: cls.from_query_single(row)
            for row in raw_data
            if row.get('qid', {}).get('value')
        }

    @classmethod
    def from_query_single(cls, data: dict) -> 'Hardware':
        '''Parse one SPARQL result row into a Hardware instance.'''
        return cls(
            nodes=data.get('nodes', {}).get('value', ''),
            cores=data.get('cores', {}).get('value', ''),
            cpu=split_value(data=data, key='cpu', transform=Relatant.from_query),
        )


@dataclass
class DataSet:
    '''Metadata and relations of a Data Set entity from MaRDI/Wikidata.'''

    size: list = field(default_factory=list)
    file_format: Optional[str] = None
    binary_or_text: Optional[str] = None
    proprietary: Optional[str] = None
    reference: list = field(default_factory=list)
    to_archive: list = field(default_factory=list)
    data_type: list[Relatant] = field(default_factory=list)
    representation_format: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'DataSet':
        '''Parse a single-item SPARQL result (backward-compatible).'''
        return cls.from_query_single(raw_data[0])

    @classmethod
    def from_query_batch(cls, raw_data: list) -> 'dict[str, DataSet]':
        '''Parse a batch SPARQL result into {external_id: instance} dict.'''
        return {
            row['qid']['value']: cls.from_query_single(row)
            for row in raw_data
            if row.get('qid', {}).get('value')
        }

    @classmethod
    def from_query_single(cls, data: dict) -> 'DataSet':
        '''Parse one SPARQL result row into a DataSet instance.'''
        options = get_options()

        return cls(
            size=get_size(data, options),
            file_format=data.get('file_format', {}).get('value'),
            binary_or_text=(
                options[data['binary_or_text']['value']]
                if data.get('binary_or_text', {}).get('value') else ''
            ),
            proprietary=(
                options[data['proprietary']['value']]
                if data.get('proprietary', {}).get('value') else ''
            ),
            reference=get_reference(data, options),
            to_archive=get_archive(data, options),
            data_type=split_value(
                data=data, key='data_type', transform=Relatant.from_query
            ),
            representation_format=split_value(
                data=data, key='representation_format', transform=Relatant.from_query
            ),
        )
