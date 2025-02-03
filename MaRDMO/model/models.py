from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..utils import get_data

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
    
@dataclass
class ResearchProblem:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    containedInField: Optional[List[Relatant]] = field(default_factory=list)
    generalizedByProblem: Optional[List[Relatant]] = field(default_factory=list)
    generalizesProblem: Optional[List[Relatant]] = field(default_factory=list)
    similarToProblem: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'ResearchProblem':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            containedInField = [Relatant.from_query(field) for field in data.get('containedInField', {}).get('value', '').split(" / ") if field] if 'containedInField' in data else [],
            generalizedByProblem = [Relatant.from_query(problem) for problem in data.get('generalizedByProblem', {}).get('value', '').split(" / ") if problem] if 'generalizedByProblem' in data else [],
            generalizesProblem = [Relatant.from_query(problem) for problem in data.get('generalizesProblem', {}).get('value', '').split(" / ") if problem] if 'generalizesProblem' in data else [],
            similarToProblem = [Relatant.from_query(problem) for problem in data.get('similarToProblem', {}).get('value', '').split(" / ") if problem] if 'similarToProblem' in data else [],            
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class MathematicalModel:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    formulation: Optional[List[Relatant]] = field(default_factory=list)
    appliedByTask: Optional[List[Relatant]] = field(default_factory=list)
    models: Optional[List[Relatant]] = field(default_factory=list)
    generalizedByModel: Optional[List[Relatant]] = field(default_factory=list)
    generalizesModel: Optional[List[Relatant]] = field(default_factory=list)
    discretizedByModel: Optional[List[Relatant]] = field(default_factory=list)
    discretizesModel: Optional[List[Relatant]] = field(default_factory=list)
    containedInModel: Optional[List[Relatant]] = field(default_factory=list)
    containsModel: Optional[List[Relatant]] = field(default_factory=list)
    approximatedByModel: Optional[List[Relatant]] = field(default_factory=list)
    approximatesModel: Optional[List[Relatant]] = field(default_factory=list)
    linearizedByModel: Optional[List[Relatant]] = field(default_factory=list)
    linearizesModel: Optional[List[Relatant]] = field(default_factory=list)
    similarToModel: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'MathematicalModel':

        mathmoddb = get_data('model/data/mapping.json')

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            properties = {idx: mathmoddb[prop] for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']) if data.get(prop, {}).get('value') == 'true'},
            formulation = [Relatant.from_query(formulation) for formulation in data.get('formulation', {}).get('value', '').split(" / ") if formulation] if 'formulation' in data else [],
            appliedByTask = [Relatant.from_query(task) for task in data.get('appliedByTask', {}).get('value', '').split(" / ") if task] if 'appliedByTask' in data else [],
            models = [Relatant.from_query(problem) for problem in data.get('models', {}).get('value', '').split(" / ") if problem] if 'models' in data else [],
            generalizedByModel = [Relatant.from_query(model) for model in data.get('generalizedByModel', {}).get('value', '').split(" / ") if model] if 'generalizedByModel' in data else [],            
            generalizesModel = [Relatant.from_query(model) for model in data.get('generalizesModel', {}).get('value', '').split(" / ") if model] if 'generalizesModel' in data else [],
            discretizedByModel = [Relatant.from_query(model) for model in data.get('discretizedByModel', {}).get('value', '').split(" / ") if model] if 'discretizedByModel' in data else [],            
            discretizesModel = [Relatant.from_query(model) for model in data.get('discretizesModel', {}).get('value', '').split(" / ") if model] if 'discretizesModel' in data else [],
            containedInModel = [Relatant.from_query(model) for model in data.get('containedInModel', {}).get('value', '').split(" / ") if model] if 'containedInModel' in data else [],            
            containsModel = [Relatant.from_query(model) for model in data.get('containsModel', {}).get('value', '').split(" / ") if model] if 'containsModel' in data else [],
            approximatedByModel = [Relatant.from_query(model) for model in data.get('approximatedByModel', {}).get('value', '').split(" / ") if model] if 'approximatedByModel' in data else [],            
            approximatesModel = [Relatant.from_query(model) for model in data.get('approximatesModel', {}).get('value', '').split(" / ") if model] if 'approximatesModel' in data else [],
            linearizedByModel = [Relatant.from_query(model) for model in data.get('linearizedByModel', {}).get('value', '').split(" / ") if model] if 'linearizedByModel' in data else [],            
            linearizesModel = [Relatant.from_query(model) for model in data.get('linearizesModel', {}).get('value', '').split(" / ") if model] if 'linearizesModel' in data else [],
            similarToModel = [Relatant.from_query(model) for model in data.get('similarToModel', {}).get('value', '').split(" / ") if model] if 'similarToModel' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )