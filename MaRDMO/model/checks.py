'''Module containing Checks for the Model Documentation'''

from rdmo.domain.models import Attribute

from .constants import data_properties_check, section_map
from .utils import error_message, check_relation_flexible, check_relation_static

from ..constants import BASE_URI
from ..getters import get_mathmoddb

class Checks:
    '''Check Class checks User Answers upon Transfer to MaRDI Portal'''
    def __init__(self):
        self.mathmoddb = get_mathmoddb()
        self.err = []

    def id_name_description(self, project, data, catalog):
        '''Perform ID, Name and Description Checks:
            - ID, Name, Description present'''

        if 'basics' in catalog:
            okeys = ('model', 'task', 'problem', 'formulation', 'publication')
        else:
            okeys = ('model', 'formulation', 'quantity', 'task', 'problem', 'field', 'publication')

        for okey, ovalue in data.items():
            if okey in okeys:
                values = project.values.filter(
                    snapshot=None,
                    attribute=Attribute.objects.get(
                        uri=f'{BASE_URI}domain/{okey}'
                    )
                )
                for ikey, ivalue in ovalue.items():
                    page_name = values.get(set_index=ikey).text
                    if not ivalue.get('ID'):
                        self.err.append(
                            error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Missing ID'
                            )
                        )
                    if not ivalue.get('Name'):
                        self.err.append(
                            error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Missing Name'
                            )
                        )
                    if not ivalue.get('Description'):
                        self.err.append(
                            error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Missing Short Description'
                            )
                        )
                    if ivalue.get('Name') == ivalue.get('Description'):
                        self.err.append(
                            error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Equal Name and Short Description Forbidden'
                            )
                        )
                    if ivalue.get('Description') and len(ivalue['Description']) > 250:
                        self.err.append(
                            error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Short Description Too Long'
                            )
                        )

    def properties(self, project, data, catalog):
        '''Perform Property Checks:
            - Properties present
            - Properties consistent'''

        if 'basics' in catalog:
            okeys = ('model', 'formulation', 'task',)
        else:
            okeys = ('model', 'formulation', 'quantity', 'task')

        for okey, ovalue in data.items():
            if okey not in okeys:
                continue
            values = project.values.filter(
                snapshot=None,
                attribute=Attribute.objects.get(
                    uri = f'{BASE_URI}domain/{okey}'
                )
            )
            for ikey, ivalue in ovalue.items():
                page_name = values.get(set_index=ikey).text
                if ivalue.get('Properties'):
                    properties = ivalue['Properties'].values()
                    for key, value in data_properties_check.items():
                        if {self.mathmoddb[key[0]], self.mathmoddb[key[1]]}.issubset(properties):
                            self.err.append(
                                error_message(
                                    section = section_map[okey],
                                    page = page_name,
                                    message = f'Inconsistent Properties {value}'
                                )
                            )

    def model(self, project, data, catalog):
        '''Perform Model Checks:
            - Connections present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/model"
            )
        )

        for ikey, ivalue in data.get('model',{}).items():
            page_name = values.get(set_index=ikey).text

            # Check mandatory static MM-RP Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationRP',
                from_class = 'Mathematical Model',
                to_class = 'Research Problem'
            )

            # Check mandatory static MM-CT Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationT',
                from_class = 'Mathematical Model',
                to_class = 'Computational Task'
            )

            # Check optional flexible MM-MM Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationMM',
                from_class = 'Mathematical Model'
            )

            # Check mandatory flexible MM-MF Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationMF',
                from_class = 'Mathematical Model',
                to_class = 'Mathematical Expression',
                optional = False
            )

            # Complete Documentation Only Checks
            if 'basics' in catalog:
                return

            # Check Qualifier Existance
            if any(
                mval['relation'] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by'])
                and not mval.get('assumption')
                for mval in ivalue.get('RelationMM', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Mathematical Model',
                        page_name,
                        'Missing Assumption '
                        '(Specializes / Specialized By Mathematical Model)'
                    )
                )

            # Check Expression Existance in Qualifier
            if any(
                mval['relation'] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by'])
                and 'not found' in mval.get('assumption', {}).values()
                for mval in ivalue.get('RelationMM', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Mathematical Model',
                        page_name,
                        'Selected Mathematical Expression '
                        'not found in Mathematical Expression Section'
                    )
                )

            # Check Order Numbers
            relation_mf = ivalue.get('RelationMF', {})
            if relation_mf:
                # Extract all order values
                orders = [val.get('order') for val in relation_mf.values()]
                # Check if any order is assigned
                has_any_order = any(order is not None for order in orders)
                if has_any_order:
                    # 1) Check all subdicts have an order number
                    if not all(order is not None for order in orders):
                        self.err.append(
                            error_message(
                                'Mathematical Model',
                                page_name,
                                'Missing Order Number (Mathematical Expression)'
                            )
                        )
                    # 2) Check the numbers form a correct sequence starting at 1
                    else:
                        order_numbers = order_numbers = set(int(order) for order in orders)
                        expected = set(range(1, len(relation_mf) + 1))
                        if order_numbers != expected:
                            self.err.append(
                                error_message(
                                    'Mathematical Model',
                                    page_name,
                                    'Incorrect Order Number (Mathematical Expression)'
                                )
                            )

    def task(self, project, data, catalog):
        '''Perform Task Checks:
            - Connections present
            - Relations present
            - Qualifier present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/task"
            )
        )

        for ikey, ivalue in data.get('task',{}).items():
            page_name = values.get(set_index=ikey).text

            # Check optional flexible T-T Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationT',
                from_class = 'Computational Task'
            )

            # Check mandatory flexible T-MF Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationMF',
                from_class = 'Computational Task',
                to_class = 'Mathematical Expression',
                optional = False
            )

            # Complete Documentation Only Checks
            if 'basics' in catalog:
                return

            # Check Qualifier Existance
            if any(
                tval['relation'] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by'])
                and not tval.get('assumption')
                for tval in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Computational Task',
                        page_name,
                        'Missing Assumption '
                        '(Specializes / Specialized By Mathematical Model)'
                    )
                )

            # Check Existance of Expression in Qualifier
            if any(
                tval['relation'] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by'])
                and 'not found' in tval.get('assumption', {}).values()
                for tval in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Computational Task',
                        page_name,
                        'Selected Mathematical Expression '
                        'not found in Mathematical Expression Section'
                    )
                )

            # Check Order Number Qualifier
            if any(
                tval['relation'] in (self.mathmoddb['contains'], self.mathmoddb['contained_in'])
                and not tval.get('order')
                for tval in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Computational Task',
                        page_name,
                        'Missing Order Number'
                        '(Conatins / Contained In Computational Task)'
                    )
                )

            # Check mandatory flexible T-QQK Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationQQK',
                from_class = 'Computational Task',
                to_class = 'Quantity',
                optional = False
            )

    def formulation(self, project, data, catalog):
        '''Perform Formulation Checks:
            - Formula present
            - Element present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/formulation"
            )
        )

        for ikey, ivalue in data.get('formulation',{}).items():
            page_name = values.get(set_index=ikey).text

            # Check optional flexible MF-MF (II) Statements
            check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationMF2',
                    from_class = 'Mathematical Expression'
                )

            # Complete Documentation Only Checks
            if 'basics' in catalog:
                # Check Reference
                if ivalue.get('ID') == 'not found':
                    if not ivalue.get('reference'):
                        self.err.append(
                            error_message(
                                'Mathematical Expression',
                                page_name,
                                'Missing Reference'
                            )
                        )

            # Complete Documentation Only Checks
            if 'basics' in catalog:
                return

            # Check Qualifier Existance
            if any(
                mval['relation'] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by'])
                and not mval.get('assumption')
                for mval in ivalue.get('RelationMF2', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Mathematical Expression',
                        page_name,
                        'Missing Assumption '
                        '(Specializes / Specialized By Mathematical Expression)'
                    )
                )

            # Check Existance of Expression Qualifier
            if any(
                mval['relation'] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by'])
                and 'not found' in mval.get('assumption', {}).values()
                for mval in ivalue.get('RelationMF2', {}).values()
            ):
                self.err.append(
                    error_message(
                        'Mathematical Expression',
                        page_name,
                        'Selected Mathematical Expression not found in Mathematical Expression Section'
                    )
                )

            # Check Formula
            if not ivalue.get('Formula'):
                self.err.append(
                    error_message(
                        'Mathematical Expression',
                        page_name,
                        'Missing Mathematical Expression Formula'
                    )
                )

            # Check Element
            if not ivalue.get('element'):
                self.err.append(
                    error_message(
                        'Mathematical Expression',
                        page_name,
                        'Missing Mathematical Expression Element Information'
                    )
                )
            else:
                not_symbol = False
                not_quantity = False
                for evalue in ivalue['element'].values():
                    if not evalue.get('symbol'):
                        not_symbol = True
                    if not evalue.get('quantity'):
                        not_quantity = True
                if not_symbol:
                    self.err.append(
                        error_message(
                            'Mathematical Expression',
                            page_name,
                            'Missing Mathematical Expression Symbol'
                        )
                    )
                if not_quantity:
                    self.err.append(
                        error_message(
                            'Mathematical Expression',
                            page_name,
                            'Missing Mathematical Expression Quantity'
                        )
                    )

            # Check optional flexible MF-MF (I) Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationMF1',
                from_class = 'Mathematical Expression'
            )

    def quantity(self, project, data, catalog):
        '''Perform Quantity Checks:
            - Class present
            - Formula is Definition 
            - Elements of Formula present
            - Relations present'''

        if 'basics' in catalog:
            return

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/quantity"
            )
        )

        for ikey, ivalue in data.get('quantity',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check Class
            if not ivalue.get('QorQK'):
                self.err.append(
                    error_message(
                        'Quantity',
                        page_name,
                        'Missing [Kind] Class'
                    )
                )
            # QUDT Reference IDs
            if ivalue.get('reference'):
                # Check if ID for selected Option is provided
                if ivalue['reference'].get(0) and not ivalue['reference'][0][1]:
                    self.err.append(
                        error_message(
                            'Quantity',
                            page_name,
                            'QUDT Quantity Kind ID selected, but no ID provided!'
                        )
                    )
                elif ivalue['reference'].get(1) and not ivalue['reference'][1][1]:
                    self.err.append(
                        error_message(
                            'Quantity',
                            page_name,
                            'QUDT Constant ID selected, but no ID provided!'
                        )
                    )
                # Check if Quantity Kind ID is selected for Quantity Kinds
                if ivalue.get('QorQK') == self.mathmoddb['Quantity']:
                    if ivalue['reference'].get(0):
                        self.err.append(
                            error_message(
                                'Quantity',
                                page_name,
                                'QUDT Quantity Kind ID limited to Quantity Kinds!'
                            )
                        )
                # Check if Constant ID is selected for Quantities
                if ivalue.get('QorQK') == self.mathmoddb['QuantityKind']:
                    if ivalue['reference'].get(1):
                        self.err.append(
                            error_message(
                                'Quantity',
                                page_name,
                                'QUDT Constant ID limited to Quantities!'
                            )
                        )
            # Check Formula
            if ivalue.get('Formula'):
                # Check \equiv sign
                for formula in ivalue['Formula'].values():
                    if not any(
                        equiv in formula
                        for equiv in ('>≡</', '>&#x2261;</', '>&equiv;</', '\\equiv', '\\Equiv')
                    ):
                        self.err.append(
                            error_message(
                                'Quantity',
                                page_name,
                                r'Inconsistent Quantity Definition (missing \equiv)'
                            )
                        )
                # Check Element
                if not ivalue.get('element'):
                    self.err.append(
                        error_message(
                            'Quantity / Quantity Kind',
                            page_name,
                            'Missing Quantity Definition Element Information'
                        )
                    )
                else:
                    not_symbol = False
                    not_quantity = False
                    for evalue in ivalue['element'].values():
                        if not evalue.get('symbol'):
                            not_symbol = True
                        if not evalue.get('quantity'):
                            not_quantity = True
                    if not_symbol:
                        self.err.append(
                            error_message(
                                'Quantity',
                                page_name,
                                'Missing Quantity Definition Symbol'
                            )
                        )
                    if not_quantity:
                        self.err.append(
                            error_message(
                                'Quantity',
                                page_name,
                                'Missing Quantity Definition Quantity'
                            )
                        )
            # Relation Connections
            if ivalue.get('QorQK') == self.mathmoddb['Quantity']:
                # Check optional flexible Q-Q Statements
                check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationQQ',
                    from_class = 'Quantity'
                )

                # Check optional flexible Q-QK Statements
                check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationQQK',
                    from_class = 'Quantity'
                )

            elif ivalue.get('QorQK') == self.mathmoddb['QuantityKind']:
                # Check optional flexible Q-Q Statements
                check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationQKQK',
                    from_class = 'Quantity'
                )

                # Check optional flexible Q-QK Statements
                check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationQKQ',
                    from_class = 'Quantity'
                )

    def problem(self, project, data, catalog):
        '''Perform Problem Checks:
            - Connections present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/problem"
            )
        )

        for ikey, ivalue in data.get('problem',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check optional flexible RP-RP Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationRP',
                from_class = 'Research Problem'
            )

            if 'basics' in catalog:
                return

            # Check mandatory static MM-RP Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationRF',
                from_class = 'Research Problem',
                to_class = 'Academic Discipline'
            )

    def field(self, project, data, catalog):
        '''Perform Problem Checks:
            - Relations present'''

        if 'basics' in catalog:
            return

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/field"
            )
        )

        for ikey, ivalue in data.get('field',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check optional flexible AD-AD Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationRF',
                from_class = 'Academic Discipline'
            )

    def publication(self, project, data):
        '''Perform Problem Checks:
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/publication"
            )
        )

        for ikey, ivalue in data.get('publication',{}).items():
            page_name = values.get(set_index=ikey).text
            if ivalue.get('ID') == 'not found' and not ivalue.get('reference'):
                self.err.append(
                    error_message(
                        'Publication',
                        page_name,
                        'Missing Publication DOI or URL'
                    )
                )
            # Check optional flexible P-E Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationP',
                from_class = 'Publication',
                to_class = 'Mathematical Model Entity',
                optional = False
            )

    def run(self, project, data, catalog):
        '''Run All Checks'''
        self.id_name_description(project, data, catalog)
        self.properties(project, data, catalog)
        self.model(project, data, catalog)
        self.task(project, data, catalog)
        self.formulation(project, data, catalog)
        self.quantity(project, data, catalog)
        self.problem(project, data, catalog)
        self.field(project, data, catalog)
        self.publication(project, data)
        if self.err:
            self.err.sort()
            self.err.insert(
                0,
                "Following incomplete or inconsistent aspects prevented the export:"
            )
        return self.err
