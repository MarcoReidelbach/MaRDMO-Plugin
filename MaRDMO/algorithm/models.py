'''Module containing Models for the Algorithm Documentation'''

from dataclasses import dataclass, field

from .constants import software_reference_ids, benchmark_reference_ids

from ..getters import get_options
from ..helpers import split_value
from ..models import Relatant

@dataclass
class Benchmark:
    '''Data Class For Benchmark Item'''
    reference: dict[int, list[str]] = field(default_factory=dict)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Benchmark':
        '''Generate Class Item From Query'''
        options = get_options()

        data = raw_data[0]

        benchmark = {
            # Benchmark Reference (DOI, MORWIKI, URL)
            'reference': {
                idx: [options[prop], data[prop]['value']]
                for idx, prop in enumerate(benchmark_reference_ids)
                if data.get(prop, {}).get('value')
            },
            # Get Publication(s)
            'publications': split_value(
                data = data,
                key = 'publication',
                transform = Relatant.from_query
            )
        }

        return cls(
            **benchmark
        )

@dataclass
class Software:
    '''Data Class for Software Item'''
    reference: dict[int, list[str]] = field(default_factory=dict)
    tested_by: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Software':
        '''Generate Class Item From Query'''
        options = get_options()

        data = raw_data[0]

        software = {
            # Software Reference (DOI, SWMATH, and URL)
            'reference': {
                idx: [options[prop], data[prop]['value']]
                for idx, prop in enumerate(software_reference_ids)
                if data.get(prop, {}).get('value')
            },
            # Related Benchmarks
            'tested_by': split_value(
                data = data,
                key = 'tested_by',
                transform = Relatant.from_query
            ),
            # Get Publication(s)
            'publications': split_value(
                data = data,
                key = 'publication',
                transform = Relatant.from_query
            )
        }

        return cls(
            **software
        )

@dataclass
class Problem:
    '''Data Class for Problem Item'''
    specializes: list[Relatant] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    manifests: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Problem':
        '''Generate Class Item From Query'''
        data = raw_data[0]

        problem = {
            # Get manifests Statements
            'manifests': split_value(
                data = data,
                key = 'manifests',
                transform = Relatant.from_query
            ),
            # Get specializes Statements
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = Relatant.from_query
            ),
            # Get specialized by Statements
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = Relatant.from_query
            ),
        }

        return cls(
            **problem
        )

@dataclass
class Algorithm:
    '''Data Class for Algorithm Item'''
    component_of: list[Relatant] = field(default_factory=list)
    has_component: list[Relatant] = field(default_factory=list)
    subclass_of: list[Relatant] = field(default_factory=list)
    has_subclass: list[Relatant] = field(default_factory=list)
    related_to: list[Relatant] = field(default_factory=list)
    solves: list[Relatant] = field(default_factory=list)
    implemented_by: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Algorithm':
        '''Generate Class Item From Query'''

        data = raw_data[0]

        algorithm = {
            # Get Problems Solved
            'solves': split_value(
                data = data,
                key = 'solved_by',
                transform = Relatant.from_query
            ),
            # Get implementing Software
            'implemented_by': split_value(
                data = data,
                key = 'implementation_of',
                transform = Relatant.from_query
            ),
            # Get has Components
            'has_component': split_value(
                data = data,
                key = 'has_parts',
                transform = Relatant.from_query
            ),
            # Get Component Of
            'component_of': split_value(
                data = data,
                key = 'part_of',
                transform = Relatant.from_query
            ),
            # Get has Subclass
            'has_subclass': split_value(
                data = data,
                key = 'has_subclass',
                transform = Relatant.from_query
            ),
            # Get Subclass Of
            'subclass_of': split_value(
                data = data,
                key = 'subclass_of',
                transform = Relatant.from_query
            ),
            # Get related to
            'related_to': split_value(
                data = data,
                key = 'similar_to',
                transform = Relatant.from_query
            ),
            # Get Publication(s)
            'publications': split_value(
                data = data,
                key = 'publication',
                transform = Relatant.from_query
            )
        }

        return cls(
            **algorithm
        )

