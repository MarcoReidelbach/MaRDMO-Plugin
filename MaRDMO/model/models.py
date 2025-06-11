from dataclasses import dataclass, field
from typing import List, Dict, Optional

from .utils import mathmlToLatex

from ..utils import get_data, get_mathmoddb
from ..id_testwiki import ITEMS

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
    order: Optional[str]
    
    @classmethod
    def from_query(cls, raw: str) -> 'RelatantWithQualifier':

        if ">|<" in raw:
            raw, order = raw.split(" >|< ")
        else:
            order = None

        id, label, description, qualifier = raw.split(" | ", 3)
    
        return cls(
            id = id,
            label = label,
            description = description,
            qualifier = qualifier,
            order = order
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
    descriptionLong: Optional[str]
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    similarTo: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'ResearchField':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            descriptionLong = [description for description in data.get('description', {}).get('value', '').split(" / ")] if 'description' in data else [],
            specializedBy = [Relatant.from_query(field) for field in data.get('specializedBy', {}).get('value', '').split(" / ") if field] if 'specializedBy' in data else [],
            specializes = [Relatant.from_query(field) for field in data.get('specializes', {}).get('value', '').split(" / ") if field] if 'specializes' in data else [],
            similarTo = [Relatant.from_query(field) for field in data.get('similarTo', {}).get('value', '').split(" / ") if field] if 'similarTo' in data else [],            
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class ResearchProblem:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    descriptionLong: Optional[str]
    containedInField: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    similarTo: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'ResearchProblem':

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            descriptionLong = [description for description in data.get('description', {}).get('value', '').split(" / ")] if 'description' in data else [],
            containedInField = [Relatant.from_query(field) for field in data.get('containedInField', {}).get('value', '').split(" / ") if field] if 'containedInField' in data else [],
            specializedBy = [Relatant.from_query(problem) for problem in data.get('specializedBy', {}).get('value', '').split(" / ") if problem] if 'specializedBy' in data else [],
            specializes = [Relatant.from_query(problem) for problem in data.get('specializes', {}).get('value', '').split(" / ") if problem] if 'specializes' in data else [],
            similarTo = [Relatant.from_query(problem) for problem in data.get('similarTo', {}).get('value', '').split(" / ") if problem] if 'similarTo' in data else [],            
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class MathematicalModel:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    descriptionLong: Optional[str]
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

        mathmoddb = get_mathmoddb()

        data = raw_data[0]
        
        return cls(
            id = None,
            label = None,
            description = None,
            descriptionLong = [description for description in data.get('description', {}).get('value', '').split(" / ")] if 'description' in data else [],
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isSpaceContinuous','isSpaceDiscrete']) if data.get(prop, {}).get('value') == 'True'},
            models = [Relatant.from_query(problem) for problem in data.get('models', {}).get('value', '').split(" / ") if problem] if 'models' in data else [],
            assumes = [Relatant.from_query(formulation) for formulation in data.get('assumes', {}).get('value', '').split(" / ") if formulation] if 'assumes' in data else [],
            containsFormulation = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == ''] if 'containsFormulation' in data else [],            
            containsBoundaryCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["boundary condition"]}'] if 'containsFormulation' in data else [],
            containsConstraintCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["constraint"]}'] if 'containsFormulation' in data else [],
            containsCouplingCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["coupling condition"]}'] if 'containsFormulation' in data else [],
            containsInitialCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["initial condition"]}'] if 'containsFormulation' in data else [],
            containsFinalCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["final condition"]}'] if 'containsFormulation' in data else [],
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
    descriptionLong: Optional[str]
    reference: Optional[str]
    qclass: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    formulas: Optional[List] = field(default_factory=list)
    symbols: Optional[List] = field(default_factory=list)
    containsQuantity: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    specializes: Optional[List[Relatant]] = field(default_factory=list)    
    approximatedBy: Optional[List[Relatant]] = field(default_factory=list)
    approximates: Optional[List[Relatant]] = field(default_factory=list)
    linearizedBy: Optional[List[Relatant]] = field(default_factory=list)
    linearizes: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizedBy: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizes: Optional[List[Relatant]] = field(default_factory=list)
    similarTo: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'QuantityOrQuantityKind':

        mathmoddb = get_mathmoddb()
        options = get_data('data/options.json')

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            descriptionLong = [description for description in data.get('description', {}).get('value', '').split(" / ")] if 'description' in data else [],
            reference = {idx: [options['QUDT'], data[prop]['value'].removeprefix('https://qudt.org/vocab/')] for idx, prop in enumerate(['reference']) if data.get(prop, {}).get('value')},
            qclass = data.get('class', {}).get('value'),
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isChemicalConstant','isMathematicalConstant','isPhysicalConstant','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isSpaceContinuous','isSpaceDiscrete']) if data.get(prop, {}).get('value') == 'True'},
            formulas = [mathmlToLatex(formula) for formula in data.get('formulas', {}).get('value', '').split(" / ") if formula] if 'formulas' in data else [],
            symbols = [mathmlToLatex(symbol.split(' | ', 1)[0]) for symbol in data.get('containsQuantity', {}).get('value', '').split(" / ") if symbol] if 'containsQuantity' in data else [],   
            containsQuantity = [Relatant.from_query(quantity.split(' | ', 1)[1]) for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity] if 'containsQuantity' in data else [],
            specializedBy = [QRelatant.from_query(quantity) for quantity in data.get('specializedBy', {}).get('value', '').split(" / ") if quantity] if 'specializedBy' in data else [],            
            specializes = [QRelatant.from_query(quantity) for quantity in data.get('specializes', {}).get('value', '').split(" / ") if quantity] if 'specializes' in data else [],
            approximatedBy = [QRelatant.from_query(quantity) for quantity in data.get('approximatedBy', {}).get('value', '').split(" / ") if quantity] if 'approximatedBy' in data else [],            
            approximates = [QRelatant.from_query(quantity) for quantity in data.get('approximates', {}).get('value', '').split(" / ") if quantity] if 'approximates' in data else [],
            linearizedBy = [QRelatant.from_query(quantity) for quantity in data.get('linearizedBy', {}).get('value', '').split(" / ") if quantity] if 'linearizedBy' in data else [],            
            linearizes = [QRelatant.from_query(quantity) for quantity in data.get('linearizes', {}).get('value', '').split(" / ") if quantity] if 'linearizes' in data else [],
            nondimensionalizedBy = [QRelatant.from_query(quantity) for quantity in data.get('nondimensionalizedBy', {}).get('value', '').split(" / ") if quantity] if 'nondimensionalizedBy' in data else [],            
            nondimensionalizes = [QRelatant.from_query(quantity) for quantity in data.get('nondimensionalizes', {}).get('value', '').split(" / ") if quantity] if 'nondimensionalizes' in data else [],
            similarTo = [QRelatant.from_query(quantity) for quantity in data.get('similarTo', {}).get('value', '').split(" / ") if quantity] if 'similarTo' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class MathematicalFormulation:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    descriptionLong: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    formulas: Optional[List] = field(default_factory=list)
    symbols: Optional[List] = field(default_factory=list)
    containsQuantity: Optional[List[Relatant]] = field(default_factory=list)
    assumes: Optional[List[Relatant]] = field(default_factory=list)
    containsFormulation: Optional[List[Relatant]] = field(default_factory=list)
    containsAssumption: Optional[List[Relatant]] = field(default_factory=list)
    containsBoundaryCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsFinalCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsInitialCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsConstraintCondition: Optional[List[Relatant]] = field(default_factory=list)
    containsCouplingCondition: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    discretizedBy: Optional[List[Relatant]] = field(default_factory=list)
    discretizes: Optional[List[Relatant]] = field(default_factory=list)
    approximatedBy: Optional[List[Relatant]] = field(default_factory=list)
    approximates: Optional[List[Relatant]] = field(default_factory=list)
    linearizedBy: Optional[List[Relatant]] = field(default_factory=list)
    linearizes: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizedBy: Optional[List[Relatant]] = field(default_factory=list)
    nondimensionalizes: Optional[List[Relatant]] = field(default_factory=list)
    similarTo: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'MathematicalFormulation':

        mathmoddb = get_mathmoddb()

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            descriptionLong = [description for description in data.get('description', {}).get('value', '').split(" / ")] if 'description' in data else [],
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isSpaceContinuous','isSpaceDiscrete']) if data.get(prop, {}).get('value') == 'True'},
            formulas = [mathmlToLatex(formula) for formula in data.get('formulas', {}).get('value', '').split(" / ") if formula] if 'formulas' in data else [],
            symbols = [symbol.split(' | ', 1)[0] for symbol in data.get('containsQuantity', {}).get('value', '').split(" / ") if symbol] if 'containsQuantity' in data else [],   
            containsQuantity = [Relatant.from_query(quantity.split(' | ', 1)[1]) for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity] if 'containsQuantity' in data else [],
            assumes = [Relatant.from_query(formulation) for formulation in data.get('assumes', {}).get('value', '').split(" / ") if formulation] if 'assumes' in data else [],
            containsFormulation = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == ''] if 'containsFormulation' in data else [],            
            containsBoundaryCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["boundary condition"]}'] if 'containsFormulation' in data else [],
            containsConstraintCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["constraint"]}'] if 'containsFormulation' in data else [],
            containsCouplingCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["coupling condition"]}'] if 'containsFormulation' in data else [],
            containsInitialCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["initial condition"]}'] if 'containsFormulation' in data else [],
            containsFinalCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["final condition"]}'] if 'containsFormulation' in data else [],
            specializedBy = [RelatantWithQualifier.from_query(formulation) for formulation in data.get('specializedBy', {}).get('value', '').split(" / ") if formulation] if 'specializedBy' in data else [],            
            specializes = [RelatantWithQualifier.from_query(formulation) for formulation in data.get('specializes', {}).get('value', '').split(" / ") if formulation] if 'specializes' in data else [],
            discretizedBy = [Relatant.from_query(formulation) for formulation in data.get('discretizedBy', {}).get('value', '').split(" / ") if formulation] if 'discretizedBy' in data else [],            
            discretizes = [Relatant.from_query(formulation) for formulation in data.get('discretizes', {}).get('value', '').split(" / ") if formulation] if 'discretizes' in data else [],
            approximatedBy = [Relatant.from_query(formulation) for formulation in data.get('approximatedBy', {}).get('value', '').split(" / ") if formulation] if 'approximatedBy' in data else [],            
            approximates = [Relatant.from_query(formulation) for formulation in data.get('approximates', {}).get('value', '').split(" / ") if formulation] if 'approximates' in data else [],
            linearizedBy = [Relatant.from_query(formulation) for formulation in data.get('linearizedBy', {}).get('value', '').split(" / ") if formulation] if 'linearizedBy' in data else [],            
            linearizes = [Relatant.from_query(formulation) for formulation in data.get('linearizes', {}).get('value', '').split(" / ") if formulation] if 'linearizes' in data else [],
            nondimensionalizedBy = [Relatant.from_query(formulation) for formulation in data.get('nondimensionalizedBy', {}).get('value', '').split(" / ") if formulation] if 'nondimensionalizedBy' in data else [],            
            nondimensionalizes = [Relatant.from_query(formulation) for formulation in data.get('nondimensionalizes', {}).get('value', '').split(" / ") if formulation] if 'nondimensionalizes' in data else [],
            similarTo = [Relatant.from_query(formulation) for formulation in data.get('similarTo', {}).get('value', '').split(" / ") if formulation] if 'similarTo' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publication', {}).get('value', '').split(" / ") if publication] if 'publication' in data else []
        )
    
@dataclass
class Task:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    descriptionLong: Optional[str]
    properties: Optional[Dict[int, str]] = field(default_factory=dict)
    assumes: Optional[List[Relatant]] = field(default_factory=list)
    containsFormulation: Optional[List[Relatant]] = field(default_factory=list)
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
    specializes: Optional[List[Relatant]] = field(default_factory=list)
    specializedBy: Optional[List[Relatant]] = field(default_factory=list)
    approximates: Optional[List[Relatant]] = field(default_factory=list)
    approximatedBy: Optional[List[Relatant]] = field(default_factory=list)
    containsTask: Optional[List[Relatant]] = field(default_factory=list)
    containedInTask: Optional[List[Relatant]] = field(default_factory=list)
    discretizedBy: Optional[List[Relatant]] = field(default_factory=list)
    discretizes: Optional[List[Relatant]] = field(default_factory=list)
    linearizedBy: Optional[List[Relatant]] = field(default_factory=list)
    linearizes: Optional[List[Relatant]] = field(default_factory=list)
    similarTo: Optional[List[Relatant]] = field(default_factory=list)
    publications: Optional[List[Relatant]] = field(default_factory=list)
    

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Task':

        mathmoddb = get_mathmoddb()

        data = raw_data[0]

        return cls(
            id = None,
            label = None,
            description = None,
            descriptionLong = [description for description in data.get('description', {}).get('value', '').split(" / ")] if 'description' in data else [],
            properties = {idx: [mathmoddb[prop]] for idx, prop in enumerate(['isLinear','isNotLinear','isTimeContinuous','isTimeDiscrete','isSpaceContinuous','isSpaceDiscrete']) if data.get(prop, {}).get('value') == 'True'},
            assumes = [Relatant.from_query(formulation) for formulation in data.get('assumes', {}).get('value', '').split(" / ") if formulation] if 'assumes' in data else [],
            containsFormulation = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == ''] if 'containsFormulation' in data else [],            
            containsBoundaryCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["boundary condition"]}'] if 'containsFormulation' in data else [],
            containsConstraintCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["constraint"]}'] if 'containsFormulation' in data else [],
            containsCouplingCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["coupling condition"]}'] if 'containsFormulation' in data else [],
            containsInitialCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["initial condition"]}'] if 'containsFormulation' in data else [],
            containsFinalCondition = [item for formulation in data.get('containsFormulation', {}).get('value', '').split(" / ") if formulation and (item := RelatantWithQualifier.from_query(formulation)).qualifier == f'mardi:{ITEMS["final condition"]}'] if 'containsFormulation' in data else [],
            containsInput = [item for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity and (item := RelatantWithQualifier.from_query(quantity)).qualifier == f'mardi:{ITEMS["input"]}'] if 'containsQuantity' in data else [],
            containsOutput = [item for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity and (item := RelatantWithQualifier.from_query(quantity)).qualifier == f'mardi:{ITEMS["output"]}'] if 'containsQuantity' in data else [],
            containsObjective = [item for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity and (item := RelatantWithQualifier.from_query(quantity)).qualifier == f'mardi:{ITEMS["objective function"]}'] if 'containsQuantity' in data else [],
            containsParameter = [item for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity and (item := RelatantWithQualifier.from_query(quantity)).qualifier == f'mardi:{ITEMS["parameter"]}'] if 'containsQuantity' in data else [],
            containsConstant = [item for quantity in data.get('containsQuantity', {}).get('value', '').split(" / ") if quantity and (item := RelatantWithQualifier.from_query(quantity)).qualifier == f'mardi:{ITEMS["constant"]}'] if 'containsQuantity' in data else [],
            specializes = [RelatantWithQualifier.from_query(model) for model in data.get('specializes', {}).get('value', '').split(" / ") if model] if 'specializes' in data else [],
            specializedBy = [RelatantWithQualifier.from_query(model) for model in data.get('specializedBy', {}).get('value', '').split(" / ") if model] if 'specializedBy' in data else [],
            approximates = [Relatant.from_query(model) for model in data.get('approximates', {}).get('value', '').split(" / ") if model] if 'approximates' in data else [],
            approximatedBy = [Relatant.from_query(model) for model in data.get('approximatedBy', {}).get('value', '').split(" / ") if model] if 'approximatedBy' in data else [],
            containsTask = [RelatantWithQualifier.from_query(model) for model in data.get('containsTask', {}).get('value', '').split(" / ") if model] if 'containsTask' in data else [],
            containedInTask = [RelatantWithQualifier.from_query(model) for model in data.get('containedInTask', {}).get('value', '').split(" / ") if model] if 'containedInTask' in data else [],
            discretizedBy = [Relatant.from_query(model) for model in data.get('discretizedBy', {}).get('value', '').split(" / ") if model] if 'discretizedBy' in data else [],            
            discretizes = [Relatant.from_query(model) for model in data.get('discretizes', {}).get('value', '').split(" / ") if model] if 'discretizes' in data else [],
            linearizedBy = [Relatant.from_query(model) for model in data.get('linearizedBy', {}).get('value', '').split(" / ") if model] if 'linearizedBy' in data else [],            
            linearizes = [Relatant.from_query(model) for model in data.get('linearizes', {}).get('value', '').split(" / ") if model] if 'linearizes' in data else [],
            similarTo = [Relatant.from_query(model) for model in data.get('similarTo', {}).get('value', '').split(" / ") if model] if 'similarTo' in data else [],
            publications = [Relatant.from_query(publication) for publication in data.get('publications', {}).get('value', '').split(" / ") if publication] if 'publications' in data else []            
            )
