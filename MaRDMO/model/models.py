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
class QRelatant:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    qclass: Optional[str]
    
    @classmethod
    def from_query(cls, raw: str) -> 'QRelatant':

        id, label, description, qclass = raw.split(" | ")

        return cls(
            id = id,
            label = label,
            description = description,
            qclass = qclass
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
    
@dataclass
class QuantityOrQuantityKind:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    qudtID: Optional[str]
    qclass: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    definedBy: Optional[List[Relatant]] = field(default_factory=list)
    generalizedByQuantity: Optional[List[Relatant]] = field(default_factory=list)
    generalizesQuantity: Optional[List[Relatant]] = field(default_factory=list)
    approximatedByQuantity: Optional[List[Relatant]] = field(default_factory=list)
    approximatesQuantity: Optional[List[Relatant]] = field(default_factory=list)
    linearizedByQuantity: Optional[List[Relatant]] = field(default_factory=list)
    linearizesQuantity: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizedByQuantity: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizesQuantity: Optional[List[Relatant]] = field(default_factory=list)
    similarToQuantity: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'QuantityOrQuantityKind':

        mathmoddb = get_data('model/data/mapping.json')

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            qudtID = data.get('qudtID', {}).get('value', '').removeprefix('https://qudt.org/vocab/'),
            qclass = data.get('class', {}).get('value'),
            properties = {idx: mathmoddb[prop] for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']) if data.get(prop, {}).get('value') == 'true'},
            definedBy = [Relatant.from_query(formulation) for formulation in data.get('definedBy', {}).get('value', '').split(" / ") if formulation] if 'definedBy' in data else [],
            generalizedByQuantity = [QRelatant.from_query(quantity) for quantity in data.get('generalizedByQuantity', {}).get('value', '').split(" / ") if quantity] if 'generalizedByQuantity' in data else [],            
            generalizesQuantity = [QRelatant.from_query(quantity) for quantity in data.get('generalizesQuantity', {}).get('value', '').split(" / ") if quantity] if 'generalizesQuantity' in data else [],
            approximatedByQuantity = [QRelatant.from_query(quantity) for quantity in data.get('approximatedByQuantity', {}).get('value', '').split(" / ") if quantity] if 'approximatedByQuantity' in data else [],            
            approximatesQuantity = [QRelatant.from_query(quantity) for quantity in data.get('approximatesQuantity', {}).get('value', '').split(" / ") if quantity] if 'approximatesQuantity' in data else [],
            linearizedByQuantity = [QRelatant.from_query(quantity) for quantity in data.get('linearizedByQuantity', {}).get('value', '').split(" / ") if quantity] if 'linearizedByQuantity' in data else [],            
            linearizesQuantity = [QRelatant.from_query(quantity) for quantity in data.get('linearizesQuantity', {}).get('value', '').split(" / ") if quantity] if 'linearizesQuantity' in data else [],
            nondimensionalizedByQuantity = [QRelatant.from_query(quantity) for quantity in data.get('nondimensionalizedByQuantity', {}).get('value', '').split(" / ") if quantity] if 'nondimensionalizedByQuantity' in data else [],            
            nondimensionalizesQuantity = [QRelatant.from_query(quantity) for quantity in data.get('nondimensionalizesQuantity', {}).get('value', '').split(" / ") if quantity] if 'nondimensionalizesQuantity' in data else [],
            similarToQuantity = [QRelatant.from_query(quantity) for quantity in data.get('similarToQuantity', {}).get('value', '').split(" / ") if quantity] if 'similarToQuantity' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class MathematicalFormulation:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    formulas: Optional[List] = field(default_factory=list)
    terms: Optional[List] = field(default_factory=list)
    defines: Optional[List[Relatant]] = field(default_factory=list)
    containsQuantity: Optional[List[Relatant]] = field(default_factory=list)
    containedAsFormulationInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsAssumptionInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsBoundaryConditionInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsFinalConditionInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsInitialConditionInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsConstraintConditionInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsCouplingConditionInMM: Optional[List[Relatant]] = field(default_factory=list)
    containedAsFormulationInMF: Optional[List[Relatant]] = field(default_factory=list)
    containedAsAssumptionInMF: Optional[List[Relatant]] = field(default_factory=list)
    containedAsBoundaryConditionInMF: Optional[List[Relatant]] = field(default_factory=list)
    containedAsFinalConditionInMF: Optional[List[Relatant]] = field(default_factory=list)
    containedAsInitialConditionInMF: Optional[List[Relatant]] = field(default_factory=list)
    containedAsConstraintConditionInMF: Optional[List[Relatant]] = field(default_factory=list)
    containedAsCouplingConditionInMF: Optional[List[Relatant]] = field(default_factory=list)
    containsFormulationMF: Optional[List[Relatant]] = field(default_factory=list)
    containsAssumptionMF: Optional[List[Relatant]] = field(default_factory=list)
    containsBoundaryConditionMF: Optional[List[Relatant]] = field(default_factory=list)
    containsFinalConditionMF: Optional[List[Relatant]] = field(default_factory=list)
    containsInitialConditionMF: Optional[List[Relatant]] = field(default_factory=list)
    containsConstraintConditionMF: Optional[List[Relatant]] = field(default_factory=list)
    containsCouplingConditionMF: Optional[List[Relatant]] = field(default_factory=list)
    generalizedByFormulation: Optional[List[Relatant]] = field(default_factory=list)
    generalizesFormulation: Optional[List[Relatant]] = field(default_factory=list)
    discretizedByFormulation: Optional[List[Relatant]] = field(default_factory=list)
    discretizesFormulation: Optional[List[Relatant]] = field(default_factory=list)
    approximatedByFormulation: Optional[List[Relatant]] = field(default_factory=list)
    approximatesFormulation: Optional[List[Relatant]] = field(default_factory=list)
    linearizedByFormulation: Optional[List[Relatant]] = field(default_factory=list)
    linearizesFormulation: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizedByFormulation: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizesFormulation: Optional[List[Relatant]] = field(default_factory=list)
    similarToFormulation: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'MathematicalFormulation':

        mathmoddb = get_data('model/data/mapping.json')

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            properties = {idx: mathmoddb[prop] for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']) if data.get(prop, {}).get('value') == 'true'},
            formulas = [formula for formula in data.get('formulas', {}).get('value', '').split(" / ") if formula] if 'formulas' in data else [],
            terms = [term for term in data.get('terms', {}).get('value', '').split(" / ") if term] if 'terms' in data else [],   
            defines = [Relatant.from_query(quantity) for quantity in data.get('defines', {}).get('value', '').split(" / ") if quantity] if 'defines' in data else [],
            containsQuantity = [Relatant.from_query(quantity) for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity] if 'containsQuantity' in data else [],
            containedAsFormulationInMM = [Relatant.from_query(model) for model in data.get('containedAsFormulationInMM', {}).get('value', '').split(" / ") if model] if 'containedAsFormulationInMM' in data else [],
            containedAsAssumptionInMM = [Relatant.from_query(model) for model in data.get('containedAsAssumptionInMM', {}).get('value', '').split(" / ") if model] if 'containedAsAssumptionInMM' in data else [],
            containedAsBoundaryConditionInMM = [Relatant.from_query(model) for model in data.get('containedAsBoundaryConditionInMM', {}).get('value', '').split(" / ") if model] if 'containedAsBoundaryConditionInMM' in data else [],
            containedAsFinalConditionInMM = [Relatant.from_query(model) for model in data.get('containedAsFinalConditionInMM', {}).get('value', '').split(" / ") if model] if 'containedAsFinalConditionInMM' in data else [],
            containedAsInitialConditionInMM = [Relatant.from_query(model) for model in data.get('containedAsInitialConditionInMM', {}).get('value', '').split(" / ") if model] if 'containedAsInitialConditionInMM' in data else [],
            containedAsConstraintConditionInMM = [Relatant.from_query(model) for model in data.get('containedAsConstraintConditionInMM', {}).get('value', '').split(" / ") if model] if 'containedAsConstraintConditionInMM' in data else [],
            containedAsCouplingConditionInMM = [Relatant.from_query(model) for model in data.get('containedAsCouplingConditionInMM', {}).get('value', '').split(" / ") if model] if 'containedAsCouplingConditionInMM' in data else [],
            containedAsFormulationInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsFormulationInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsFormulationInMF' in data else [],
            containedAsAssumptionInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsAssumptionInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsAssumptionInMF' in data else [],
            containedAsBoundaryConditionInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsBoundaryConditionInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsBoundaryConditionInMF' in data else [],
            containedAsFinalConditionInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsFinalConditionInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsFinalConditionInMF' in data else [],
            containedAsInitialConditionInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsInitialConditionInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsInitialConditionInMF' in data else [],
            containedAsConstraintConditionInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsConstraintConditionInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsConstraintConditionInMF' in data else [],
            containedAsCouplingConditionInMF = [Relatant.from_query(formulation) for formulation in data.get('containedAsCouplingConditionInMF', {}).get('value', '').split(" / ") if formulation] if 'containedAsCouplingConditionInMF' in data else [],
            containsFormulationMF = [Relatant.from_query(formulation) for formulation in data.get('containsFormulationMF', {}).get('value', '').split(" / ") if formulation] if 'containsFormulationMF' in data else [],
            containsAssumptionMF = [Relatant.from_query(formulation) for formulation in data.get('containsAssumptionMF', {}).get('value', '').split(" / ") if formulation] if 'containsAssumptionMF' in data else [],
            containsBoundaryConditionMF = [Relatant.from_query(formulation) for formulation in data.get('containsBoundaryConditionMF', {}).get('value', '').split(" / ") if formulation] if 'containsBoundaryConditionMF' in data else [], 
            containsFinalConditionMF = [Relatant.from_query(formulation) for formulation in data.get('containsFinalConditionMF', {}).get('value', '').split(" / ") if formulation] if 'containsFinalConditionMF' in data else [],
            containsInitialConditionMF = [Relatant.from_query(formulation) for formulation in data.get('containsInitialConditionMF', {}).get('value', '').split(" / ") if formulation] if 'containsInitialConditionMF' in data else [],
            containsConstraintConditionMF = [Relatant.from_query(formulation) for formulation in data.get('containsConstraintConditionMF', {}).get('value', '').split(" / ") if formulation] if 'containsConstraintConditionMF' in data else [],
            containsCouplingConditionMF = [Relatant.from_query(formulation) for formulation in data.get('containsCouplingConditionMF', {}).get('value', '').split(" / ") if formulation] if 'containsCouplingConditionMF' in data else [],
            generalizedByFormulation = [Relatant.from_query(formulation) for formulation in data.get('generalizedByFormulation', {}).get('value', '').split(" / ") if formulation] if 'generalizedByFormulation' in data else [],            
            generalizesFormulation = [Relatant.from_query(formulation) for formulation in data.get('generalizesFormulation', {}).get('value', '').split(" / ") if formulation] if 'generalizesFormulation' in data else [],
            discretizedByFormulation = [Relatant.from_query(formulation) for formulation in data.get('discretizedByFormulation', {}).get('value', '').split(" / ") if formulation] if 'discretizedByFormulation' in data else [],            
            discretizesFormulation = [Relatant.from_query(formulation) for formulation in data.get('discretizesFormulation', {}).get('value', '').split(" / ") if formulation] if 'discretizesFormulation' in data else [],
            approximatedByFormulation = [Relatant.from_query(formulation) for formulation in data.get('approximatedByFormulation', {}).get('value', '').split(" / ") if formulation] if 'approximatedByFormulation' in data else [],            
            approximatesFormulation = [Relatant.from_query(formulation) for formulation in data.get('approximatesFormulation', {}).get('value', '').split(" / ") if formulation] if 'approximatesFormulation' in data else [],
            linearizedByFormulation = [Relatant.from_query(formulation) for formulation in data.get('linearizedByFormulation', {}).get('value', '').split(" / ") if formulation] if 'linearizedByFormulation' in data else [],            
            linearizesFormulation = [Relatant.from_query(formulation) for formulation in data.get('linearizesFormulation', {}).get('value', '').split(" / ") if formulation] if 'linearizesFormulation' in data else [],
            nondimensionalizedByFormulation = [Relatant.from_query(formulation) for formulation in data.get('nondimensionalizedByFormulation', {}).get('value', '').split(" / ") if formulation] if 'nondimensionalizedByFormulation' in data else [],            
            nondimensionalizesFormulation = [Relatant.from_query(formulation) for formulation in data.get('nondimensionalizesFormulation', {}).get('value', '').split(" / ") if formulation] if 'nondimensionalizesFormulation' in data else [],
            similarToFormulation = [Relatant.from_query(formulation) for formulation in data.get('similarToFormulation', {}).get('value', '').split(" / ") if formulation] if 'similarToFormulation' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )