'''Module building handler maps for post_save and post_delete routing.'''

from .constants import BASE_URI
from .getters import get_questions
from .model.handlers import Information as ModelInformation
from .algorithm.handlers import Information as AlgorithmInformation
from .workflow.handlers import Information as WorkflowInformation
from .publication.handlers import Information as PublicationInformation
from .handlers import Information as GeneralInformation

def build_handler_map():
    """Build a global mapping of attribute URIs to handler functions."""
    #from .model import handlers as model_handlers
    base = BASE_URI
    handler_map = {}

    # Questions
    questions_model = get_questions('model')
    questions_algorithm = get_questions('algorithm')
    questions_workflow = get_questions('workflow')
    questions_publication = get_questions('publication')

    # Information Classes
    model = ModelInformation()
    algorithm = AlgorithmInformation()
    workflow = WorkflowInformation()
    publication = PublicationInformation()
    general = GeneralInformation()

    # Model handlers
    handler_map.update({
        'mardmo-model-catalog': {
            f"{base}{questions_model['Research Field']['ID']['uri']}":
                model.field,
            f"{base}{questions_model['Research Problem']['ID']['uri']}":
                model.problem,
            f"{base}{questions_model['Quantity']['ID']['uri']}":
                model.quantity,
            f"{base}{questions_model['Mathematical Formulation']['ID']['uri']}":
                model.formulation,
            f"{base}{questions_model['Task']['ID']['uri']}":
                model.task,
            f"{base}{questions_model['Mathematical Model']['ID']['uri']}":
                model.model,
            f'{base}{questions_model["Task"]["QRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Task"]["MFRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Formulation"]["Element Quantity"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Quantity"]["Element Quantity"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["MFRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["Assumption"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Task"]["Assumption"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Formulation"]["Assumption"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Formulation"]["MFRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Research Problem"]["RFRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["RPRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["TRelatant"]["uri"]}':
                general.relation,
            f"{base}{questions_publication['Publication']['ID']['uri']}":
                publication.citation,
        }
    })

    # Model handlers
    handler_map.update({
        'mardmo-model-basics-catalog': {
            f"{base}{questions_model['Research Problem']['ID']['uri']}":
                model.problem,
            f"{base}{questions_model['Task']['ID']['uri']}":
                model.task,
            f"{base}{questions_model['Mathematical Model']['ID']['uri']}":
                model.model,
            f"{base}{questions_model['Mathematical Formulation']['ID']['uri']}":
                model.formulation,
            f'{base}{questions_model["Mathematical Model"]["RPRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["TRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["MFRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Model"]["Assumption"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Task"]["Assumption"]["uri"]}':
                general.relation,
            f'{base}{questions_model["Mathematical Formulation"]["Assumption"]["uri"]}':
                general.relation,
            f"{base}{questions_publication['Publication']['ID']['uri']}":
                publication.citation,
        }
    })

    # Algorithm handlers
    handler_map.update({
        'mardmo-algorithm-catalog': {
            f"{base}{questions_algorithm['Benchmark']['ID']['uri']}":
                algorithm.benchmark,
            f"{base}{questions_algorithm['Software']['ID']['uri']}":
                algorithm.software,
            f"{base}{questions_algorithm['Problem']['ID']['uri']}":
                algorithm.problem,
            f"{base}{questions_algorithm['Algorithm']['ID']['uri']}":
                algorithm.algorithm,
            f'{base}{questions_algorithm["Problem"]["BRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_algorithm["Software"]["BRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_algorithm["Algorithm"]["PRelatant"]["uri"]}':
                general.relation,
            f'{base}{questions_algorithm["Algorithm"]["SRelatant"]["uri"]}':
                general.relation,
            f"{base}{questions_publication['Publication']['ID']['uri']}":
                publication.citation,
        }
    })

    # Workflow handlers
    handler_map.update({
        'mardmo-interdisciplinary-workflow-catalog': {
            f"{base}{questions_workflow['Software']['ID']['uri']}":
                workflow.software,
            f"{base}{questions_workflow['Hardware']['ID']['uri']}":
                workflow.hardware,
            f"{base}{questions_workflow['Instrument']['ID']['uri']}":
                workflow.instrument,
            f"{base}{questions_workflow['Data Set']['ID']['uri']}":
                workflow.data_set,
            f"{base}{questions_workflow['Method']['ID']['uri']}":
                workflow.method,
            f"{base}{questions_workflow['Process Step']['ID']['uri']}":
                workflow.process_step,
            f'{base}{questions_workflow["Process Step"]["Input"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Process Step"]["Output"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Process Step"]["Method"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Process Step"]["Environment-Software"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Process Step"]["Environment-Instrument"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Method"]["Software"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Method"]["Instrument"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Instrument"]["Software"]["uri"]}':
                general.relation,
            f'{base}{questions_workflow["Hardware"]["Software"]["uri"]}':
                general.relation,
            f"{base}{questions_publication['Publication']['ID']['uri']}":
                publication.citation,
        }
    })

    return handler_map
