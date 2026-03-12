'''Module containing Checks for Model and Algorithm Documentation'''

from rdmo.domain.models import Attribute

from .model.constants import data_properties_check, data_properties_label
from .model.constants import SECTION_MAP as SECTION_MAP_MODEL
from .algorithm.constants import SECTION_MAP as SECTION_MAP_ALGO

from .constants import BASE_URI, CATALOG_ALGORITHM, CATALOG_MODEL, CATALOG_MODEL_BASICS
from .getters import get_mathmoddb, get_mathalgodb

class Checks:
    '''Check Class checks User Answers upon Transfer to MaRDI Portal'''
    def __init__(self):
        self.mathmoddb = get_mathmoddb()
        self.mathalgodb = get_mathalgodb()
        self.err = []

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _error(section, page, message):
        return f"{section} (Page {page}): {message}"

    def _check_static(self, data, page_name, relation, from_class, to_class):
        '''Append errors for a mandatory 1-value relation (must exist, must be found)'''
        if not data.get(relation):
            self.err.append(self._error(from_class, page_name, f'Missing {to_class}'))
        elif 'not found' in data[relation].values():
            self.err.append(self._error(from_class, page_name,
                f'Selected {to_class} not found in {to_class} Section'))

    def _check_flexible(self, data, page_name, relation, from_class, to_class=None, optional=True):
        '''Append errors for a multi-value relation block'''
        to_class = to_class or from_class
        entries = data.get(relation, {})

        if not optional and not entries:
            self.err.append(self._error(from_class, page_name, f'Missing {to_class}'))

        if any(v['relation'] is None for v in entries.values()):
            self.err.append(self._error(from_class, page_name, f'Missing Relation Type ({to_class})'))

        if any(v['relatant'] == 'MISSING OBJECT ITEM' for v in entries.values()):
            self.err.append(self._error(from_class, page_name, f'Missing Object Item ({to_class})'))

        if any(v['relatant'] == 'not found' for v in entries.values()):
            self.err.append(self._error(from_class, page_name,
                f'Selected {to_class} not found in {to_class} Section'))

    def id_name_description(self, project, data, catalog):
        '''Perform ID, Name and Description Checks'''

        if catalog == CATALOG_ALGORITHM:
            section_map = SECTION_MAP_ALGO
            okeys = ('algorithm', 'problem', 'software', 'benchmark', 'publication')
        elif catalog in (CATALOG_MODEL, CATALOG_MODEL_BASICS):
            section_map = SECTION_MAP_MODEL
            okeys = ('model', 'formulation', 'quantity', 'task', 'problem', 'field', 'publication')
        else:
            return

        for okey, ovalue in data.items():
            if okey not in okeys:
                continue
            values = project.values.filter(
                snapshot=None,
                attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{okey}')
            )
            for ikey, ivalue in ovalue.items():
                page_name = values.get(set_index=ikey).text
                if not ivalue.get('ID'):
                    self.err.append(self._error(section_map[okey], page_name, 'Missing ID'))
                if not ivalue.get('Name'):
                    self.err.append(self._error(section_map[okey], page_name, 'Missing Name'))
                if not ivalue.get('Description'):
                    self.err.append(self._error(section_map[okey], page_name, 'Missing Short Description'))
                if ivalue.get('Name') == ivalue.get('Description'):
                    self.err.append(self._error(section_map[okey], page_name, 'Equal Name and Short Description Forbidden'))
                if ivalue.get('Description') and len(ivalue['Description']) > 250:
                    self.err.append(self._error(section_map[okey], page_name, 'Short Description Too Long'))

    # -------------------------------------------------------------------------
    # Model Documentation Checks
    # -------------------------------------------------------------------------

    def properties(self, project, data, catalog):
        '''Perform Property Checks'''

        section_map = SECTION_MAP_MODEL

        if catalog == CATALOG_MODEL_BASICS:
            okeys = ('model', 'formulation', 'task') 
        elif catalog == CATALOG_MODEL:
            okeys = ('model', 'formulation', 'quantity', 'task')
        else:
            return

        for okey, ovalue in data.items():
            if okey not in okeys:
                continue
            values = project.values.filter(
                snapshot=None,
                attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{okey}')
            )
            for ikey, ivalue in ovalue.items():
                page_name = values.get(set_index=ikey).text
                if not ivalue.get('Properties'):
                    continue
                properties = ivalue['Properties'].values()
                for pair in data_properties_check:
                    if not {self.mathmoddb.get(key=pair[0])["url"], self.mathmoddb.get(key=pair[1])["url"]}.issubset(properties):
                        continue
                    self.err.append(self._error(
                        section_map[okey], page_name,
                        f'Inconsistent Properties ({data_properties_label[pair[0]]} and {data_properties_label[pair[1]]})'
                    ))

    def model(self, project, data, catalog):
        '''Perform Model Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/model')
        )
        for ikey, ivalue in data.get('model', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationRP', from_class='Mathematical Model', to_class='Research Problem')
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationT', from_class='Mathematical Model', to_class='Computational Task')
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationMM', from_class='Mathematical Model')
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationMF', from_class='Mathematical Model', to_class='Mathematical Expression', optional=False)

            if catalog == CATALOG_MODEL_BASICS:
                return

            if any(
                mval['relation'] in (self.mathmoddb.get(key='specializes')["url"], self.mathmoddb.get(key='specialized_by')["url"])
                and not mval.get('assumption')
                for mval in ivalue.get('RelationMM', {}).values()
            ):
                self.err.append(self._error('Mathematical Model', page_name,
                    'Missing Assumption (Specializes / Specialized By Mathematical Model)'))

            if any(
                mval['relation'] in (self.mathmoddb.get(key='specializes')["url"], self.mathmoddb.get(key='specialized_by')["url"])
                and 'not found' in mval.get('assumption', {}).values()
                for mval in ivalue.get('RelationMM', {}).values()
            ):
                self.err.append(self._error('Mathematical Model', page_name,
                    'Selected Mathematical Expression not found in Mathematical Expression Section'))

            relation_mf = ivalue.get('RelationMF', {})
            if relation_mf:
                orders = [val.get('order') for val in relation_mf.values()]
                if any(order is not None for order in orders):
                    if not all(order is not None for order in orders):
                        self.err.append(self._error('Mathematical Model', page_name,
                            'Missing Order Number (Mathematical Expression)'))
                    else:
                        order_numbers = set(int(order) for order in orders)
                        if order_numbers != set(range(1, len(relation_mf) + 1)):
                            self.err.append(self._error('Mathematical Model', page_name,
                                'Incorrect Order Number (Mathematical Expression)'))

    def task(self, project, data, catalog):
        '''Perform Task Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/task')
        )
        for ikey, ivalue in data.get('task', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationT', from_class='Computational Task')
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationMF', from_class='Computational Task', to_class='Mathematical Expression', optional=False)

            if catalog == CATALOG_MODEL_BASICS:
                return

            if any(
                tval['relation'] in (self.mathmoddb.get(key='specializes')["url"], self.mathmoddb.get(key='specialized_by')["url"])
                and not tval.get('assumption')
                for tval in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(self._error('Computational Task', page_name,
                    'Missing Assumption (Specializes / Specialized By Mathematical Model)'))

            if any(
                tval['relation'] in (self.mathmoddb.get(key='specializes')["url"], self.mathmoddb.get(key='specialized_by')["url"])
                and 'not found' in tval.get('assumption', {}).values()
                for tval in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(self._error('Computational Task', page_name,
                    'Selected Mathematical Expression not found in Mathematical Expression Section'))

            if any(
                tval['relation'] in (self.mathmoddb.get(key='contains_task')["url"], self.mathmoddb.get(key='contained_in_task')["url"])
                and not tval.get('order')
                for tval in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(self._error('Computational Task', page_name,
                    'Missing Order Number (Conatins / Contained In Computational Task)'))

            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationQQK', from_class='Computational Task', to_class='Quantity', optional=False)

    def formulation(self, project, data, catalog):
        '''Perform Formulation Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/formulation')
        )
        for ikey, ivalue in data.get('formulation', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationMF2', from_class='Mathematical Expression')

            if catalog == CATALOG_MODEL_BASICS:
                if ivalue.get('ID') == 'not found' and not ivalue.get('reference'):
                    self.err.append(self._error('Mathematical Expression', page_name, 'Missing Reference'))
                return

            if any(
                mval['relation'] in (self.mathmoddb.get(key='specializes')["url"], self.mathmoddb.get(key='specialized_by')["url"])
                and not mval.get('assumption')
                for mval in ivalue.get('RelationMF2', {}).values()
            ):
                self.err.append(self._error('Mathematical Expression', page_name,
                    'Missing Assumption (Specializes / Specialized By Mathematical Expression)'))

            if any(
                mval['relation'] in (self.mathmoddb.get(key='specializes')["url"], self.mathmoddb.get(key='specialized_by')["url"])
                and 'not found' in mval.get('assumption', {}).values()
                for mval in ivalue.get('RelationMF2', {}).values()
            ):
                self.err.append(self._error('Mathematical Expression', page_name,
                    'Selected Mathematical Expression not found in Mathematical Expression Section'))

            if not ivalue.get('Formula'):
                self.err.append(self._error('Mathematical Expression', page_name,
                    'Missing Mathematical Expression Formula'))

            if not ivalue.get('element'):
                self.err.append(self._error('Mathematical Expression', page_name,
                    'Missing Mathematical Expression Element Information'))
            else:
                not_symbol = any(not ev.get('symbol') for ev in ivalue['element'].values())
                not_quantity = any(not ev.get('quantity') for ev in ivalue['element'].values())
                if not_symbol:
                    self.err.append(self._error('Mathematical Expression', page_name,
                        'Missing Mathematical Expression Symbol'))
                if not_quantity:
                    self.err.append(self._error('Mathematical Expression', page_name,
                        'Missing Mathematical Expression Quantity'))

            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationMF1', from_class='Mathematical Expression')

    def quantity(self, project, data, catalog):
        '''Perform Quantity Checks'''
        if catalog == CATALOG_MODEL_BASICS:
            return
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/quantity')
        )
        for ikey, ivalue in data.get('quantity', {}).items():
            page_name = values.get(set_index=ikey).text
            if not ivalue.get('QorQK'):
                self.err.append(self._error('Quantity', page_name, 'Missing [Kind] Class'))

            if ivalue.get('reference'):
                ref = ivalue['reference']
                if ref.get(0) and not ref[0][1]:
                    self.err.append(self._error('Quantity', page_name, 'QUDT Quantity Kind ID selected, but no ID provided!'))
                elif ref.get(1) and not ref[1][1]:
                    self.err.append(self._error('Quantity', page_name, 'QUDT Constant ID selected, but no ID provided!'))
                if ivalue.get('QorQK') == self.mathmoddb.get(key='Quantity')["url"] and ref.get(0):
                    self.err.append(self._error('Quantity', page_name, 'QUDT Quantity Kind ID limited to Quantity Kinds!'))
                if ivalue.get('QorQK') == self.mathmoddb.get(key='QuantityKind')["url"] and ref.get(1):
                    self.err.append(self._error('Quantity', page_name, 'QUDT Constant ID limited to Quantities!'))

            if ivalue.get('Formula'):
                for formula in ivalue['Formula'].values():
                    if not any(equiv in formula for equiv in ('>≡</', '>&#x2261;</', '>&equiv;</', '\\equiv', '\\Equiv')):
                        self.err.append(self._error('Quantity', page_name, r'Inconsistent Quantity Definition (missing \equiv)'))
                if not ivalue.get('element'):
                    self.err.append(self._error('Quantity / Quantity Kind', page_name,
                        'Missing Quantity Definition Element Information'))
                else:
                    if any(not ev.get('symbol') for ev in ivalue['element'].values()):
                        self.err.append(self._error('Quantity', page_name, 'Missing Quantity Definition Symbol'))
                    if any(not ev.get('quantity') for ev in ivalue['element'].values()):
                        self.err.append(self._error('Quantity', page_name, 'Missing Quantity Definition Quantity'))

            if ivalue.get('QorQK') == self.mathmoddb.get(key='Quantity')["url"]:
                self._check_flexible(data=ivalue, page_name=page_name,
                    relation='RelationQQ', from_class='Quantity')
                self._check_flexible(data=ivalue, page_name=page_name,
                    relation='RelationQQK', from_class='Quantity')
            elif ivalue.get('QorQK') == self.mathmoddb.get(key='QuantityKind')["url"]:
                self._check_flexible(data=ivalue, page_name=page_name,
                    relation='RelationQKQK', from_class='Quantity')
                self._check_flexible(data=ivalue, page_name=page_name,
                    relation='RelationQKQ', from_class='Quantity')

    def model_problem(self, project, data, catalog):
        '''Perform Research Problem Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/problem')
        )
        for ikey, ivalue in data.get('problem', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationRP', from_class='Research Problem')
            if catalog == CATALOG_MODEL_BASICS:
                return
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationRF', from_class='Research Problem', to_class='Academic Discipline')

    def field(self, project, data, catalog):
        '''Perform Academic Discipline Checks'''
        if catalog == CATALOG_MODEL_BASICS:
            return
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/field')
        )
        for ikey, ivalue in data.get('field', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationRF', from_class='Academic Discipline')

    # -------------------------------------------------------------------------
    # Algorithm Documentation Checks
    # -------------------------------------------------------------------------

    def algorithm(self, project, data):
        '''Perform Algorithm Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/algorithm')
        )
        for ikey, ivalue in data.get('algorithm', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationP', from_class='Algorithm', to_class='Algorithmic Task')
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationS', from_class='Algorithm', to_class='Software')
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationA', from_class='Algorithm')

    def algo_problem(self, project, data):
        '''Perform Algorithmic Task Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/problem')
        )
        for ikey, ivalue in data.get('problem', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationB', from_class='Algorithmic Task', to_class='Benchmark')
            self._check_flexible(data=ivalue, page_name=page_name,
                relation='RelationP', from_class='Algorithmic Task')

    def software(self, project, data):
        '''Perform Software Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/software')
        )
        for ikey, ivalue in data.get('software', {}).items():
            page_name = values.get(set_index=ikey).text
            self._check_static(data=ivalue, page_name=page_name,
                relation='RelationB', from_class='Software', to_class='Benchmark')
            if ivalue.get('reference'):
                ref = ivalue['reference']
                for idx, label, noun in [(0, 'DOI', 'ID'), (1, 'swMath ID', 'ID'), (2, 'Description URL', 'URL'), (3, 'Repository URL', 'URL')]:
                    if ref.get(idx) and not ref[idx][1]:
                        self.err.append(self._error('Software', page_name, f'{label} selected, but no {noun} provided!'))

    def benchmark(self, project, data):
        '''Perform Benchmark Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/benchmark')
        )
        for ikey, ivalue in data.get('benchmark', {}).items():
            page_name = values.get(set_index=ikey).text
            if ivalue.get('reference'):
                ref = ivalue['reference']
                for idx, label, noun in [(0, 'DOI', 'ID'), (1, 'MORwiki ID', 'ID'), (2, 'Description URL', 'URL'), (3, 'Repository URL', 'URL')]:
                    if ref.get(idx) and not ref[idx][1]:
                        self.err.append(self._error('Benchmark', page_name, f'{label} selected, but no {noun} provided!'))

    # -------------------------------------------------------------------------
    # Publication Check (shared, behaviour differs by mode)
    # -------------------------------------------------------------------------

    def publication(self, project, data, catalog):
        '''Perform Publication Checks'''
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/publication')
        )
        for ikey, ivalue in data.get('publication', {}).items():
            page_name = values.get(set_index=ikey).text
            if ivalue.get('ID') == 'not found' and not ivalue.get('reference'):
                self.err.append(self._error('Publication', page_name,
                    'Missing Publication DOI' if catalog == CATALOG_ALGORITHM else 'Missing Publication DOI or URL'))

            if catalog == CATALOG_ALGORITHM:
                # Algorithm mode: optional links, but at least one required
                if ivalue.get('RelationA') or ivalue.get('RelationBS'):
                    self._check_flexible(data=ivalue, page_name=page_name,
                        relation='RelationA', from_class='Publication', to_class='Algorithm', optional=True)
                    self._check_flexible(data=ivalue, page_name=page_name,
                        relation='RelationBS', from_class='Publication', to_class='Benchmark/Software', optional=True)
                else:
                    self.err.append(self._error('Publication', page_name,
                        'Missing Algorithm, Benchmark, or Software'))
            else:
                # Model mode: mandatory link to a model entity
                self._check_flexible(data=ivalue, page_name=page_name,
                    relation='RelationP', from_class='Publication', to_class='Mathematical Model Entity', optional=False)

    # -------------------------------------------------------------------------
    # Run methods
    # -------------------------------------------------------------------------

    def run_model(self, project, data, catalog):
        '''Run all Model Documentation Checks'''
        self.id_name_description(project, data, catalog)
        self.properties(project, data, catalog)
        self.model(project, data, catalog)
        self.task(project, data, catalog)
        self.formulation(project, data, catalog)
        self.quantity(project, data, catalog)
        self.model_problem(project, data, catalog)
        self.field(project, data, catalog)
        self.publication(project, data, catalog)
        return self._finalise()

    def run_algorithm(self, project, data):
        '''Run all Algorithm Documentation Checks'''
        catalog = CATALOG_ALGORITHM
        self.id_name_description(project, data, catalog)
        self.algorithm(project, data)
        self.algo_problem(project, data)
        self.software(project, data)
        self.benchmark(project, data)
        self.publication(project, data, catalog)
        return self._finalise()

    def _finalise(self):
        if self.err:
            self.err.sort()
            self.err.insert(0, "Following incomplete or inconsistent aspects prevented the export:")
        return self.err
