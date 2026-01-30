'''Module containing Models for the Model Documentation'''

from dataclasses import dataclass, field
from typing import Optional

from .constants import data_properties_per_class, qudt_reference_ids

from ..getters import get_items, get_mathmoddb, get_options
from ..helpers import split_value
from ..models import Relatant, RelatantWithClass

@dataclass
class RelatantWithQualifier:
    '''Data Class For Relatant Items With Qualifier'''
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    qualifier: Optional[str]
    order: Optional[str]

    @classmethod
    def from_query(cls, raw: str) -> 'RelatantWithQualifier':
        '''Generate Class Item From Query'''
        if ">|<" in raw:
            raw, order = raw.split(" >|< ")
        else:
            order = None
        identifier, label, description, qualifier = raw.split(" | ", 3)
        return cls(
            id = identifier,
            label = label,
            description = description,
            qualifier = qualifier,
            order = order
        )

@dataclass
class ResearchField:
    '''Data Class For Research Field Item'''
    aliases: list[str] = field(default_factory=list)
    description_long: list[str] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    specializes: list[Relatant] = field(default_factory=list)
    similar_to: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'ResearchField':
        '''Generate Class Item From Query'''

        data = raw_data[0]

        research_field = {
            # Get Aliases
            'aliases': split_value(
                data = data,
                key = 'aliases'
            ),
            # Get Long Description(s)
            'description_long': split_value(
                data = data,
                key = 'description_long'
            ),
            # Get Specialized By Relation(s)
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = Relatant.from_query
            ),
            # Get Specializes Relation(s)
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = Relatant.from_query
            ),
            # Get Similar To Relation(s)
            'similar_to': split_value(
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
            **research_field
        )

@dataclass
class ResearchProblem:
    '''Data Class For Research Problem Item'''
    aliases: list[str] = field(default_factory=list)
    description_long: list[str] = field(default_factory=list)
    contained_in_field: list[Relatant] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    specializes: list[Relatant] = field(default_factory=list)
    similar_to: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'ResearchProblem':
        '''Generate Class Item From Query'''

        data = raw_data[0]

        research_problem = {
            # Get Aliases
            'aliases': split_value(
                data = data,
                key = 'aliases'
            ),
            # Get Long Description(s)
            'description_long': split_value(
                data = data,
                key = 'description_long'
            ),
            # Get Field Relation(s)
            'contained_in_field': split_value(
                data = data,
                key = 'contained_in_field',
                transform = Relatant.from_query
            ),
            # Get Specialized By Relation(s)
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = Relatant.from_query
            ),
            # Get Specializes Relation(s)
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = Relatant.from_query
            ),
            # Get Similar To Relation(s)
            'similar_to': split_value(
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
            **research_problem
        )

@dataclass
class MathematicalModel:
    '''Data Class For Mathematical Model Item'''
    aliases: list[str] = field(default_factory=list)
    description_long: list[str] = field(default_factory=list)
    properties: dict[int, str] = field(default_factory=dict)
    models: list[Relatant] = field(default_factory=list)
    assumes: list[Relatant] = field(default_factory=list)
    contains_formulation: list[Relatant] = field(default_factory=list)
    contains_boundary_condition: list[Relatant] = field(default_factory=list)
    contains_constraint_condition: list[Relatant] = field(default_factory=list)
    contains_coupling_condition: list[Relatant] = field(default_factory=list)
    contains_initial_condition: list[Relatant] = field(default_factory=list)
    contains_final_condition: list[Relatant] = field(default_factory=list)
    contains_analytical_solution: list[Relatant] = field(default_factory=list)
    contains_physical_law: list[Relatant] = field(default_factory=list)
    contains_computational_domain: list[Relatant] = field(default_factory=list)
    contains_constitutive_equation: list[Relatant] = field(default_factory=list)
    contains_weak_formulation: list[Relatant] = field(default_factory=list)
    contains_strong_formulation: list[Relatant] = field(default_factory=list)
    used_by: list[Relatant] = field(default_factory=list)
    specializes: list[Relatant] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    approximates: list[Relatant] = field(default_factory=list)
    approximated_by: list[Relatant] = field(default_factory=list)
    contains_model: list[Relatant] = field(default_factory=list)
    contained_in_model: list[Relatant] = field(default_factory=list)
    discretized_by: list[Relatant] = field(default_factory=list)
    discretizes: list[Relatant] = field(default_factory=list)
    linearized_by: list[Relatant] = field(default_factory=list)
    linearizes: list[Relatant] = field(default_factory=list)
    similar_to: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'MathematicalModel':
        '''Generate Class Item From Query'''

        mathmoddb = get_mathmoddb()
        items = get_items()

        data = raw_data[0]

        mathematical_model = {
            # Get Aliases
            'aliases': split_value(
                data = data,
                key = 'aliases'
            ),
            # Get Long Description(s)
            'description_long': split_value(
                data = data,
                key = 'description_long'
            ),
            # Get Properties
            'properties': {
                idx: [mathmoddb[prop]]
                for idx, prop in enumerate(data_properties_per_class['model'])
                if data.get(prop, {}).get('value') == 'True'
            },
            # Get Problem Relation(s)
            'models': split_value(
                data = data,
                key = 'models',
                transform = Relatant.from_query
            ),
            # Get Assumption Relation(s)
            'assumes': split_value(
                data = data,
                key = 'assumes',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Contains Formulation Relation(s)
            'contains_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == ''
            ),
            # Get Contains Boundary Condition Relation(s)
            'contains_boundary_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["boundary condition"]}'
            ),
            # Get Contains Constraint Condition Relation(s)
            'contains_constraint_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["constraint"]}'
            ),
            # Get Contains Coupling Condition Relation(s)
            'contains_coupling_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["coupling condition"]}'
            ),
            # Get Contains Initial Condition Relation(s)
            'contains_initial_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["initial condition"]}'
            ),
            # Get Contains Final Condition Relation(s)
            'contains_final_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["final condition"]}'
            ),
            # Get Contains Analytical Solution Relation(s)
            'contains_analytical_solution': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["analytical solution"]}'
            ),
            # Get Contains Physical Law Relation(s)
            'contains_physical_law': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["physical law"]}'
            ),
            # Get Contains Computational Domain Relation(s)
            'contains_computational_domain': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["computational domain"]}'
            ),
            # Get Contains Constitutive Equation Relation(s)
            'contains_constitutive_equation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["constitutive equation"]}'
            ),
            # Get Contains Weak Formulation Relation(s)
            'contains_weak_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["weak formulation"]}'
            ),
            # Get Contains Strong Formulation Relation(s)
            'contains_strong_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["strong formulation"]}'
            ),
            # Get Task Relation(s)
            'used_by': split_value(
                data = data,
                key = 'used_by',
                transform = Relatant.from_query
            ),
            # Get Specialized By Relation(s)
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Specializes Relation(s)
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Approximated By Relation(s)
            'approximated_by': split_value(
                data = data,
                key = 'approximated_by',
                transform = Relatant.from_query
            ),
            # Get Approximates Relation(s)
            'approximates': split_value(
                data = data,
                key = 'approximates',
                transform = Relatant.from_query
            ),
            # Get Contained In Model Relation(s)
            'contained_in_model': split_value(
                data = data,
                key = 'contained_in_model',
                transform = Relatant.from_query
            ),
            # Get Contains Model Relation(s)
            'contains_model': split_value(
                data = data,
                key = 'contains_model',
                transform = Relatant.from_query
            ),
            # Get Discretized By Relation(s)
            'discretized_by': split_value(
                data = data,
                key = 'discretized_by',
                transform = Relatant.from_query
            ),
            # Get Discretizes Relation(s)
            'discretizes': split_value(
                data = data,
                key = 'discretizes',
                transform = Relatant.from_query
            ),
            # Get Linearized By Relation(s)
            'linearized_by': split_value(
                data = data,
                key = 'linearized_by',
                transform = Relatant.from_query
            ),
            # Get Linearizes Relation(s)
            'linearizes': split_value(
                data = data,
                key = 'linearizes',
                transform = Relatant.from_query
            ),
            # Get Similar To Relation(s)
            'similar_to': split_value(
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
            **mathematical_model
        )

@dataclass
class QuantityOrQuantityKind:
    '''Data Class For Quantity [Kind] Item'''
    aliases: list[str] = field(default_factory=list)
    description_long: list[str] = field(default_factory=list)
    reference: dict[int, list[str]] = field(default_factory=dict)
    qclass: Optional[str] = None
    properties: dict[int, str] = field(default_factory=dict)
    formulas: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    contains_quantity: list[Relatant] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    specializes: list[Relatant] = field(default_factory=list)
    approximated_by: list[Relatant] = field(default_factory=list)
    approximates: list[Relatant] = field(default_factory=list)
    discretized_by: list[Relatant] = field(default_factory=list)
    discretizes: list[Relatant] = field(default_factory=list)
    linearized_by: list[Relatant] = field(default_factory=list)
    linearizes: list[Relatant] = field(default_factory=list)
    nondimensionalized_by: list[Relatant] = field(default_factory=list)
    nondimensionalizes: list[Relatant] = field(default_factory=list)
    similar_to: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'QuantityOrQuantityKind':
        '''Generate Class Item From Query'''

        mathmoddb = get_mathmoddb()
        options = get_options()

        data = raw_data[0]

        quantity = {
            # Get Aliases
            'aliases': split_value(
                data = data,
                key = 'aliases'
            ),
            # Get Long Description(s)
            'description_long': split_value(
                data = data,
                key = 'description_long'
            ),
            # Get Reference
            'reference': {
                idx: [mathmoddb[prop], data[prop]['value']]
                for idx, prop in enumerate(qudt_reference_ids)
                if data.get(prop, {}).get('value')
            },
            # Get Quantity or Quantity Kind Class
            'qclass': data.get('class', {}).get('value'),
            # Get Properties
            'properties': {
                idx: [mathmoddb[prop]]
                for idx, prop in enumerate(data_properties_per_class['quantity'])
                if data.get(prop, {}).get('value') == 'True'
            },
            # Get Formulas
            'formulas': split_value(
                data = data,
                key = 'formulas'
            ),
            # Get Symbols
            'symbols': split_value(
                data = data,
                key = 'contains_quantity',
                transform = lambda s: s.split(' | ', 1)[0]
            ),
            # Get contained Quantities
            'contains_quantity': split_value(
                data = data,
                key = 'contains_quantity',
                transform = lambda q: Relatant.from_query(q.split(' | ', 1)[1])
            ),
            # Get Specialized By Relation(s)
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = RelatantWithClass.from_query
            ),
            # Get Specializes Relation(s)
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = RelatantWithClass.from_query
            ),
            # Get Approximated By Relation(s)
            'approximated_by': split_value(
                data = data,
                key = 'approximated_by',
                transform = RelatantWithClass.from_query
            ),
            # Get Approximates Relation(s)
            'approximates': split_value(
                data = data,
                key = 'approximates',
                transform = RelatantWithClass.from_query
            ),
            # Get Discretized By Relation(s)
            'discretized_by': split_value(
                data = data,
                key = 'discretized_by',
                transform = RelatantWithClass.from_query
            ),
            # Get Discretizes Relation(s)
            'discretizes': split_value(
                data = data,
                key = 'discretizes',
                transform = RelatantWithClass.from_query
            ),
            # Get Linearized By Relation(s)
            'linearized_by': split_value(
                data = data,
                key = 'linearized_by',
                transform = RelatantWithClass.from_query
            ),
            # Get Linearizes Relation(s)
            'linearizes': split_value(
                data = data,
                key = 'linearizes',
                transform = RelatantWithClass.from_query
            ),
            # Get Nondimesionalized By Relation(s)
            'nondimensionalized_by': split_value(
                data = data,
                key = 'nondimensionalized_by',
                transform = RelatantWithClass.from_query
            ),
            # Get Nondimensionalizes Relation(s)
            'nondimensionalizes': split_value(
                data = data,
                key = 'nondimensionalizes',
                transform = RelatantWithClass.from_query
            ),
            # Get Similar To Relation(s)
            'similar_to': split_value(
                data = data,
                key = 'similar_to',
                transform = RelatantWithClass.from_query
            ),
            # Get Publication(s)
            'publications': split_value(
                data = data,
                key = 'publication',
                transform = Relatant.from_query
            )
        }

        return cls(
            **quantity
        )

@dataclass
class MathematicalFormulation:
    '''Data Class For Formulation Item'''
    reference: Optional[str] = None
    aliases: list[str] = field(default_factory=list)
    description_long: list[str] = field(default_factory=list)
    properties: dict[int, str] = field(default_factory=dict)
    formulas: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)
    contains_quantity: list[Relatant] = field(default_factory=list)
    assumes: list[Relatant] = field(default_factory=list)
    contains_formulation: list[Relatant] = field(default_factory=list)
    contains_assumption: list[Relatant] = field(default_factory=list)
    contains_boundary_condition: list[Relatant] = field(default_factory=list)
    contains_final_condition: list[Relatant] = field(default_factory=list)
    contains_initial_condition: list[Relatant] = field(default_factory=list)
    contains_constraint_condition: list[Relatant] = field(default_factory=list)
    contains_coupling_condition: list[Relatant] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    specializes: list[Relatant] = field(default_factory=list)
    discretized_by: list[Relatant] = field(default_factory=list)
    discretizes: list[Relatant] = field(default_factory=list)
    approximated_by: list[Relatant] = field(default_factory=list)
    approximates: list[Relatant] = field(default_factory=list)
    linearized_by: list[Relatant] = field(default_factory=list)
    linearizes: list[Relatant] = field(default_factory=list)
    nondimensionalized_by: list[Relatant] = field(default_factory=list)
    nondimensionalizes: list[Relatant] = field(default_factory=list)
    similar_to: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)


    @classmethod
    def from_query(cls, raw_data: dict) -> 'MathematicalFormulation':
        '''Generate Class Item From Query'''

        mathmoddb = get_mathmoddb()
        items = get_items()

        data = raw_data[0]

        mathematical_formulation = {
            # Get Aliases
            'aliases': split_value(
                data = data,
                key = 'aliases'
            ),
            # Get Long Description(s)
            'description_long': split_value(
                data = data,
                key = 'description_long'
            ),
            # Get Properties
            'properties': {
                idx: [mathmoddb[prop]]
                for idx, prop in enumerate(data_properties_per_class['formulation'])
                if data.get(prop, {}).get('value') == 'True'
            },
            # Get Reference
            'reference': data.get('reference', {}).get('value'),
            # Get Formulas
            'formulas': split_value(
                data = data,
                key = 'formulas'
            ),
            # Get Symbols
            'symbols': split_value(
                data = data,
                key = 'contains_quantity',
                transform = lambda s: s.split(' | ', 1)[0]
            ),
            # Get contained Quantities
            'contains_quantity': split_value(
                data = data,
                key = 'contains_quantity',
                transform = lambda q: Relatant.from_query(q.split(' | ', 1)[1])
            ),
            # Get Assumption Relation(s)
            'assumes': split_value(
                data = data,
                key = 'assumes',
                transform = Relatant.from_query
            ),
            # Get Contains Formulation Relation(s)
            'contains_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == ''
            ),
            # Get Contains Boundary Condition Relation(s)
            'contains_boundary_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["boundary condition"]}'
            ),
            # Get Contains Constraint Condition Relation(s)
            'contains_constraint_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["constraint"]}'
            ),
            # Get Contains Coupling Condition Relation(s)
            'contains_coupling_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["coupling condition"]}'
            ),
            # Get Contains Initial Condition Relation(s)
            'contains_initial_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["initial condition"]}'
            ),
            # Get Contains Final Condition Relation(s)
            'contains_final_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["final condition"]}'
            ),
            # Get Specialized By Relation(s)
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Specializes Relation(s)
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Approximated By Relation(s)
            'approximated_by': split_value(
                data = data,
                key = 'approximated_by',
                transform = Relatant.from_query
            ),
            # Get Approximates Relation(s)
            'approximates': split_value(
                data = data,
                key = 'approximates',
                transform = Relatant.from_query
            ),
            # Get Discretized By Relation(s)
            'discretized_by': split_value(
                data = data,
                key = 'discretized_by',
                transform = Relatant.from_query
            ),
            # Get Discretizes Relation(s)
            'discretizes': split_value(
                data = data,
                key = 'discretizes',
                transform = Relatant.from_query
            ),
            # Get Linearized By Relation(s)
            'linearized_by': split_value(
                data = data,
                key = 'linearized_by',
                transform = Relatant.from_query
            ),
            # Get Linearizes Relation(s)
            'linearizes': split_value(
                data = data,
                key = 'linearizes',
                transform = Relatant.from_query
            ),
            # Get Nondimensionalized By Relation(s)
            'nondimensionalized_by': split_value(
                data = data,
                key = 'nondimensionalized_by',
                transform = Relatant.from_query
            ),
            # Get Nondimesionalizes Relation(s)
            'nondimensionalizes': split_value(
                data = data,
                key = 'nondimensionalizes',
                transform = Relatant.from_query
            ),
            # Get Similar To Relation(s)
            'similar_to': split_value(
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
            **mathematical_formulation
        )

@dataclass
class Task:
    '''Data Class For Task Item'''
    aliases: list[str] = field(default_factory=list)
    description_long: list[str] = field(default_factory=list)
    properties: dict[int, str] = field(default_factory=dict)
    assumes: list[Relatant] = field(default_factory=list)
    contains_formulation: list[Relatant] = field(default_factory=list)
    contains_boundary_condition: list[Relatant] = field(default_factory=list)
    contains_final_condition: list[Relatant] = field(default_factory=list)
    contains_initial_condition: list[Relatant] = field(default_factory=list)
    contains_constraint_condition: list[Relatant] = field(default_factory=list)
    contains_coupling_condition: list[Relatant] = field(default_factory=list)
    contains_analytical_solution: list[Relatant] = field(default_factory=list)
    contains_physical_law: list[Relatant] = field(default_factory=list)
    contains_computational_domain: list[Relatant] = field(default_factory=list)
    contains_constitutive_equation: list[Relatant] = field(default_factory=list)
    contains_weak_formulation: list[Relatant] = field(default_factory=list)
    contains_strong_formulation: list[Relatant] = field(default_factory=list)
    contains_input: list[Relatant] = field(default_factory=list)
    contains_output: list[Relatant] = field(default_factory=list)
    contains_objective: list[Relatant] = field(default_factory=list)
    contains_parameter: list[Relatant] = field(default_factory=list)
    contains_constant: list[Relatant] = field(default_factory=list)
    specializes: list[Relatant] = field(default_factory=list)
    specialized_by: list[Relatant] = field(default_factory=list)
    approximates: list[Relatant] = field(default_factory=list)
    approximated_by: list[Relatant] = field(default_factory=list)
    contains_task: list[Relatant] = field(default_factory=list)
    contained_in_task: list[Relatant] = field(default_factory=list)
    discretized_by: list[Relatant] = field(default_factory=list)
    discretizes: list[Relatant] = field(default_factory=list)
    linearized_by: list[Relatant] = field(default_factory=list)
    linearizes: list[Relatant] = field(default_factory=list)
    similar_to: list[Relatant] = field(default_factory=list)
    publications: list[Relatant] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Task':
        '''Generate Class Item From Query'''

        mathmoddb = get_mathmoddb()
        items = get_items()

        data = raw_data[0]

        task = {
            # Get Aliases
            'aliases': split_value(
                data = data,
                key = 'aliases'
            ),
            # Get Long Description(s)
            'description_long': split_value(
                data = data,
                key = 'description_long'
            ),
            # Get Properties
            'properties': {
                idx: [mathmoddb[prop]]
                for idx, prop in enumerate(data_properties_per_class['task'])
                if data.get(prop, {}).get('value') == 'True'
            },
            # Get Assumption Relation(s)
            'assumes': split_value(
                data = data,
                key = 'assumes',
                transform = Relatant.from_query
            ),
            # Get Contains Formulation Relation(s)
            'contains_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == ''
            ),
            # Get Contains Boundary Condition Relation(s)
            'contains_boundary_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["boundary condition"]}'
            ),
            # Get Contains Constraint Condition Relation(s)
            'contains_constraint_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["constraint"]}'
            ),
            # Get Contains Coupling Condition Relation(s)
            'contains_coupling_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["coupling condition"]}'
            ),
            # Get Contains Initial Condition Relation(s)
            'contains_initial_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["initial condition"]}'
            ),
            # Get Contains Final Condition Relation(s)
            'contains_final_condition': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["final condition"]}'
            ),
            # Get Contains Analytical Solution Relation(s)
            'contains_analytical_solution': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["analytical solution"]}'
            ),
            # Get Contains Physical Law Relation(s)
            'contains_physical_law': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["physical law"]}'
            ),
            # Get Contains Computational Domain Relation(s)
            'contains_computational_domain': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["computational domain"]}'
            ),
            # Get Contains Constitutive Equation Relation(s)
            'contains_constitutive_equation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["constitutive equation"]}'
            ),
            # Get Contains Weak Formulation Relation(s)
            'contains_weak_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["weak formulation"]}'
            ),
            # Get Contains Strong Formulation Relation(s)
            'contains_strong_formulation': split_value(
                data = data,
                key = 'contains_formulation',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["strong formulation"]}'
            ),
            # Get Contains Input Relation(s)
            'contains_input': split_value(
                data = data,
                key = 'contains_quantity',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["input"]}'
            ),
            # Get Contains Output Relation(s)
            'contains_output': split_value(
                data = data,
                key = 'contains_quantity',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["output"]}'
            ),
            # Get Contains Objective Relation(s)
            'contains_objective': split_value(
                data = data,
                key = 'contains_quantity',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["objective function"]}'
            ),
            # Get Contains Parameter Relation(s)
            'contains_parameter': split_value(
                data = data,
                key = 'contains_quantity',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["parameter"]}'
            ),
            # Get Contains Constant Relation(s)
            'contains_constant': split_value(
                data = data,
                key = 'contains_quantity',
                transform = RelatantWithQualifier.from_query,
                object_role = lambda item: item.qualifier == f'mardi:{items["constant"]}'
            ),
            # Get Specialized By Relation(s)
            'specialized_by': split_value(
                data = data,
                key = 'specialized_by',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Specializes Relation(s)
            'specializes': split_value(
                data = data,
                key = 'specializes',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Approximated By Relation(s)
            'approximated_by': split_value(
                data = data,
                key = 'approximated_by',
                transform = Relatant.from_query
            ),
            # Get Approximates Relation(s)
            'approximates': split_value(
                data = data,
                key = 'approximates',
                transform = Relatant.from_query
            ),
            # Get Contained In Relation(s)
            'contained_in_task': split_value(
                data = data,
                key = 'contained_in_task',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Contains Relation(s)
            'contains_task': split_value(
                data = data,
                key = 'contains_task',
                transform = RelatantWithQualifier.from_query
            ),
            # Get Discretized By Relation(s)
            'discretized_by': split_value(
                data = data,
                key = 'discretized_by',
                transform = Relatant.from_query
            ),
            # Get Discretizes Relation(s)
            'discretizes': split_value(
                data = data,
                key = 'discretizes',
                transform = Relatant.from_query
            ),
            # Get Linearized By Relation(s)
            'linearized_by': split_value(
                data = data,
                key = 'linearized_by',
                transform = Relatant.from_query
            ),
            # Get Linearizes Relation(s)
            'linearizes': split_value(
                data = data,
                key = 'linearizes',
                transform = Relatant.from_query
            ),
            # Get Similar To Relation(s)
            'similar_to': split_value(
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
            **task
            )
