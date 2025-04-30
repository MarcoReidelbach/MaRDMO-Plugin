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
    
    @classmethod
    def from_relation(cls, id: str, label: str, description: str) -> 'Relatant':

        return cls(
            id = id,
            label = label,
            description = description,
        )
    
@dataclass
class RelatantWithQualifier:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    qualifier: Optional[str]
    
    @classmethod
    def from_query(cls, raw: str) -> 'RelatantWithQualifier':

        id, label, description, qualifier = raw.split(" | ", 3)
    
        return cls(
            id = id,
            label = label,
            description = description,
            qualifier = qualifier
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
    models: Optional[List[Relatant]] = field(default_factory=list)
    assumes: Optional[List[Relatant]] = field(default_factory=list)
    containsFormulation: Optional[List[Relatant]] = field(default_factory=list)
    containsBoundaryCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsConstraintCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsCouplingCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsInitialCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsFinalCondition: Optional[List[Relatant]] = field(default_factory=list)
    usedBy: Optional[List[Relatant]] = field(default_factory=list)
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    approximates: Optional[List[Relatant]] = field(default_factory=list)
    approximatedBy: Optional[List[Relatant]] = field(default_factory=list)
    containsModel: Optional[List[Relatant]] = field(default_factory=list)
    containedInModel: Optional[List[Relatant]] = field(default_factory=list)
    discretizedBy: Optional[List[Relatant]] = field(default_factory=list)
    discretizes: Optional[List[Relatant]] = field(default_factory=list)
    linearizedBy: Optional[List[Relatant]] = field(default_factory=list)
    linearizes: Optional[List[Relatant]] = field(default_factory=list)
    similarTo: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'MathematicalModel':

        mathmoddb = get_data('model/data/mapping.json')

        data = raw_data[0]
        
        return cls(
            id = None,
            label = None,
            description = None,
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isSpaceContinuous','isSpaceDiscrete']) if data.get(prop, {}).get('value') == 'True'},
            models = [Relatant.from_query(problem) for problem in data.get('models', {}).get('value', '').split(" / ") if problem] if 'models' in data else [],
            assumes = [Relatant.from_query(formulation) for formulation in data.get('assumes', {}).get('value', '').split(" / ") if formulation] if 'assumes' in data else [],
            containsFormulation = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == ''] if 'containsFormulation' in data else [],            
            containsBoundaryCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == 'mardi:Q6534259'] if 'containsFormulation' in data else [],
            containsConstraintCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == 'mardi:Q6534262'] if 'containsFormulation' in data else [],
            containsCouplingCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == 'mardi:Q6534266'] if 'containsFormulation' in data else [],
            containsInitialCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == 'mardi:Q6534264'] if 'containsFormulation' in data else [],
            containsFinalCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == 'mardi:Q6534267'] if 'containsFormulation' in data else [],
            usedBy = [Relatant.from_query(task) for task in data.get('usedBy', {}).get('value', '').split(" / ") if task] if 'usedBy' in data else [],
            specializes = [RelatantWithQualifier.from_query(model) for model in data.get('specializes', {}).get('value', '').split(" / ") if model] if 'specializes' in data else [],
            specializedBy = [RelatantWithQualifier.from_query(model) for model in data.get('specializedBy', {}).get('value', '').split(" / ") if model] if 'specializedBy' in data else [],
            approximates = [Relatant.from_query(model) for model in data.get('approximates', {}).get('value', '').split(" / ") if model] if 'approximates' in data else [],
            approximatedBy = [Relatant.from_query(model) for model in data.get('approximatedBy', {}).get('value', '').split(" / ") if model] if 'approximatedBy' in data else [],
            containsModel = [Relatant.from_query(model) for model in data.get('containsModel', {}).get('value', '').split(" / ") if model] if 'containsModel' in data else [],
            containedInModel = [Relatant.from_query(model) for model in data.get('containedInModel', {}).get('value', '').split(" / ") if model] if 'containedInModel' in data else [],
            discretizedBy = [Relatant.from_query(model) for model in data.get('discretizedBy', {}).get('value', '').split(" / ") if model] if 'discretizedBy' in data else [],            
            discretizes = [Relatant.from_query(model) for model in data.get('discretizes', {}).get('value', '').split(" / ") if model] if 'discretizes' in data else [],
            linearizedBy = [Relatant.from_query(model) for model in data.get('linearizedBy', {}).get('value', '').split(" / ") if model] if 'linearizedBy' in data else [],            
            linearizes = [Relatant.from_query(model) for model in data.get('linearizes', {}).get('value', '').split(" / ") if model] if 'linearizes' in data else [],
            similarTo = [Relatant.from_query(model) for model in data.get('similarTo', {}).get('value', '').split(" / ") if model] if 'similarTo' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class QuantityOrQuantityKind:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    reference: Optional[str]
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
        options = get_data('data/options.json')

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            reference = {idx: [options['QUDT'], data[prop]['value'].removeprefix('https://qudt.org/vocab/')] for idx, prop in enumerate(['reference']) if data.get(prop, {}).get('value')},
            qclass = data.get('class', {}).get('value'),
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']) if data.get(prop, {}).get('value') == 'true'},
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
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']) if data.get(prop, {}).get('value') == 'true'},
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
    
@dataclass
class Task:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    subclass: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    appliesModel: Optional[List[Relatant]] = field(default_factory=list)
    containsFormulation: Optional[List[Relatant]] = field(default_factory=list)
    containsAssumption: Optional[List[Relatant]] = field(default_factory=list)
    containsBoundaryCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsFinalCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsInitialCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsConstraintCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsCouplingCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsInput: Optional[List[Relatant]] = field(default_factory=list)
    containsOutput: Optional[List[Relatant]] = field(default_factory=list)
    containsObjective: Optional[List[Relatant]] = field(default_factory=list)
    containsParameter: Optional[List[Relatant]] = field(default_factory=list)
    containsConstant: Optional[List[Relatant]] = field(default_factory=list)
    generalizedByTask: Optional[List[Relatant]] = field(default_factory=list)
    generalizesTask: Optional[List[Relatant]] = field(default_factory=list)
    approximatedByTask: Optional[List[Relatant]] = field(default_factory=list)
    approximatesTask: Optional[List[Relatant]] = field(default_factory=list)
    containsTask: Optional[List[Relatant]] = field(default_factory=list)
    containedInTask: Optional[List[Relatant]] = field(default_factory=list)
    linearizedByTask: Optional[List[Relatant]] = field(default_factory=list)
    linearizesTask: Optional[List[Relatant]] = field(default_factory=list)
    discretizedByTask: Optional[List[Relatant]] = field(default_factory=list)
    discretizesTask: Optional[List[Relatant]] = field(default_factory=list)
    similarToTask: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Task':

        mathmoddb = get_data('model/data/mapping.json')

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            subclass = data.get('class', {}).get('value', ''),
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']) if data.get(prop, {}).get('value') == 'true'},
            appliesModel = [Relatant.from_query(model) for model in data.get('appliesModel', {}).get('value', '').split(" / ") if model] if 'appliesModel' in data else [],
            containsFormulation = [Relatant.from_query(formulation) for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation] if 'containsFormulation' in data else [],
            containsAssumption = [Relatant.from_query(formulation) for formulation in data.get('containsAssumption', {}).get('value', '').split(" / ") if formulation] if 'containsAssumption' in data else [],
            containsBoundaryCondition = [Relatant.from_query(formulation) for formulation in data.get('containsBoundaryCondition', {}).get('value', '').split(" / ") if formulation] if 'containsBoundaryCondition' in data else [],
            containsConstraintCondition = [Relatant.from_query(formulation) for formulation in data.get('containsConstraintCondition', {}).get('value', '').split(" / ") if formulation] if 'containsConstraintCondition' in data else [],
            containsCouplingCondition = [Relatant.from_query(formulation) for formulation in data.get('containsCouplingCondition', {}).get('value', '').split(" / ") if formulation] if 'containsCouplingCondition' in data else [],
            containsInitialCondition = [Relatant.from_query(formulation) for formulation in data.get('containsInitialCondition', {}).get('value', '').split(" / ") if formulation] if 'containsInitialCondition' in data else [],
            containsFinalCondition = [Relatant.from_query(formulation) for formulation in data.get('containsFinalCondition', {}).get('value', '').split(" / ") if formulation] if 'containsFinalCondition' in data else [],
            containsInput = [Relatant.from_query(quantity) for quantity in data.get('containsInput', {}).get('value', '').split(" / ") if quantity] if 'containsInput' in data else [],
            containsOutput = [Relatant.from_query(quantity) for quantity in data.get('containsOutput', {}).get('value', '').split(" / ") if quantity] if 'containsOutput' in data else [],
            containsObjective = [Relatant.from_query(quantity) for quantity in data.get('containsObjective', {}).get('value', '').split(" / ") if quantity] if 'containsObjective' in data else [],
            containsParameter = [Relatant.from_query(quantity) for quantity in data.get('containsParameter', {}).get('value', '').split(" / ") if quantity] if 'containsParameter' in data else [],
            containsConstant = [Relatant.from_query(quantity) for quantity in data.get('containsConstant', {}).get('value', '').split(" / ") if quantity] if 'containsConstant' in data else [],
            generalizedByTask = [Relatant.from_query(task) for task in data.get('generalizedByTask', {}).get('value', '').split(" / ") if task] if 'generalizedByTask' in data else [],
            generalizesTask = [Relatant.from_query(task) for task in data.get('generalizesTask', {}).get('value', '').split(" / ") if task] if 'generalizesTask' in data else [],
            approximatedByTask = [Relatant.from_query(task) for task in data.get('approximatedByTask', {}).get('value', '').split(" / ") if task] if 'approximatedByTask' in data else [],
            approximatesTask = [Relatant.from_query(task) for task in data.get('approximatesTask', {}).get('value', '').split(" / ") if task] if 'approximatesTask' in data else [],
            containsTask = [Relatant.from_query(task) for task in data.get('containsTask', {}).get('value', '').split(" / ") if task] if 'containsTask' in data else [],
            containedInTask = [Relatant.from_query(task) for task in data.get('containedInTask', {}).get('value', '').split(" / ") if task] if 'containedInTask' in data else [],
            linearizedByTask = [Relatant.from_query(task) for task in data.get('linearizedByTask', {}).get('value', '').split(" / ") if task] if 'linearizedByTask' in data else [],
            linearizesTask = [Relatant.from_query(task) for task in data.get('linearizesTask', {}).get('value', '').split(" / ") if task] if 'linearizesTask' in data else [],
            discretizedByTask = [Relatant.from_query(task) for task in data.get('discretizedByTask', {}).get('value', '').split(" / ") if task] if 'discretizedByTask' in data else [],
            discretizesTask = [Relatant.from_query(task) for task in data.get('discretizesTask', {}).get('value', '').split(" / ") if task] if 'discretizesTask' in data else [],
            similarToTask = [Relatant.from_query(task) for task in data.get('similarToTask', {}).get('value', '').split(" / ") if task] if 'similarToTask' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publications', {}).get('value', '').split(" / ") if publication] if 'publications' in data else []            
            )