import os
import json
import re
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from .sparql import queryModelDocumentation
from .config import mardi_api, mathmoddb_endpoint

@dataclass
class EntityRelation:
    id: str
    label: str
    relation: str

@dataclass
class Entity:
    math_mod_id: str
    name: str
    description: Optional[str] = None
    properties: Dict = field(default_factory=dict)
    relations: Dict[str, List[EntityRelation]] = field(default_factory=dict)

@dataclass
class Answers:
    Task: Dict[str, Entity] = field(default_factory=dict)
    MathematicalModel: Dict[str, Entity] = field(default_factory=dict)
    MathematicalFormulation: Dict[str, Entity] = field(default_factory=dict)
    Quantity: Dict[str, Entity] = field(default_factory=dict)
    ResearchField: Dict[str, Entity] = field(default_factory=dict)
    ResearchProblem: Dict[str, Entity] = field(default_factory=dict)
    Models: Dict[str, Entity] = field(default_factory=dict)
    PublicationModel: Dict[str, Entity] = field(default_factory=dict)

@dataclass
class ModelRetriever:
    answers: Answers
    mathmoddb: Dict
    inverse_property_mapping: Dict

    formulation_kinds: List[str] = field(default_factory=lambda: ['Formulation', 'Assumption', 'BoundaryCondition', 'ConstraintCondition', 'CouplingCondition', 'InitialCondition', 'FinalCondition'])
    quantity_kinds: List[str] = field(default_factory=lambda: ['Input', 'Output', 'Objective', 'Parameter', 'Constant'])
    intra_class_relations: List[str] = field(default_factory=lambda: ['generalizedBy', 'generalizes', 'approximatedBy', 'approximates', 'discretizedBy', 'discretizes', 'linearizedBy', 'linearizes', 'nondimensionalizedBy', 'nondimensionalizes', 'similarTo'])
    publication_relations: List[str] = field(default_factory=lambda: ['documentedIn', 'inventedIn', 'studiedIn', 'surveyedIn', 'usedIn'])
    data_properties: List[str] = field(default_factory=lambda: ['isLinear', 'isNotLinear', 'isConvex', 'isNotConvex', 'isDynamic', 'isStatic', 'isDeterministic', 'isStochastic', 'isDimensionless', 'isDimensional', 'isTimeContinuous', 'isTimeDiscrete', 'isTimeIndependent', 'isSpaceContinuous', 'isSpaceDiscrete', 'isSpaceIndependent'])

    def retrieve_models(self):
        # Flag all Tasks as unwanted by User in Workflow Documentation
        for task in self.answers.Task.values():
            task.properties['Include'] = False

        self._process_class('MathematicalModel')
        self._process_class('Task')

        # Add Mathematical Formulations from Task to Formulation List
        self._add_mathematical_formulations()

    def _process_class(self, q_class: str):
        search_string = self._search_generator([q_class])
        results = queryMathModDB(queryModelDocumentation[q_class].format(search_string))

        mathmodid_to_key = {self.answers.Task[key].math_mod_id: key for key in self.answers.Task}

        for result in results:
            math_mod_id = result.get(q_class, {}).get('value')
            if math_mod_id in mathmodid_to_key:
                key = mathmodid_to_key[math_mod_id]
                self._assign_value(q_class, ['quote'], 'Description', result, key)
                self._assign_properties(self.answers.Task[key], result)

    def _add_mathematical_formulations(self):
        name_to_key = {v.name: k for k, v in self.answers.MathematicalFormulation.items()}

        for idx, task in enumerate(self.answers.Task.values()):
            for relation, label in task.relations.get('T2MF', {}).items():
                if label in name_to_key:
                    math_form = self.answers.MathematicalFormulation[name_to_key[label]]
                    math_form.relations.setdefault('MF2T', {})[f'TF{task.math_mod_id}{idx}'] = self.inverse_property_mapping[relation]
                else:
                    new_key = str(max(map(int, self.answers.MathematicalFormulation.keys()), default=-1) + 1)
                    new_formulation = Entity(math_mod_id=task.math_mod_id, name=label)
                    self.answers.MathematicalFormulation[new_key] = new_formulation
                    name_to_key[label] = new_key

    def _search_generator(self, class_list: List[str]) -> str:
        return " ".join(f":{entity.math_mod_id.split('#')[1]}" for cls in class_list for entity in getattr(self.answers, cls).values() if entity.math_mod_id)

    def _assign_value(self, q_class, key_old, key_new, result, key):
        if result.get(key_old[0], {}).get('value'):
            self.answers.Task[key].description = result[key_old[0]]['value']

    def _assign_properties(self, entity: Entity, result: Dict):
        for property in self.data_properties:
            if result.get(property, {}).get('value') == 'true':
                entity.properties[property] = self.mathmoddb.get(property)


def queryMathModDB(query, endpoint=mathmoddb_endpoint):
    response = requests.post(endpoint, data=query, headers={"Content-Type": "application/sparql-query", "Accept": "application/sparql-results+json"})
    if response.status_code == 200:
        return response.json().get('results', {}).get('bindings', [])
    return []
