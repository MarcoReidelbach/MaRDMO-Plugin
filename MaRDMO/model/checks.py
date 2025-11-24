'''Module containing Checks for the Model Documentation'''

from rdmo.domain.models import Attribute

from .constants import data_properties_check, section_map

from ..constants import BASE_URI
from ..getters import get_mathmoddb

class Checks:
    '''Check Class checks User Answers upon Transfer to MaRDI Portal'''
    def __init__(self):
        self.mathmoddb = get_mathmoddb()
        self.err = []

    def error_message(self, section, page, message):
        '''Generate Error Message'''
        return f"{section} (Page {page}): {message}"

    def id_name_description(self, project, data):
        '''Perform ID, Name and Description Checks:
            - ID, Name, Description present'''

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
                            self.error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Missing ID'
                            )
                        )
                    if not ivalue.get('Name'):
                        self.err.append(
                            self.error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Missing Name'
                            )
                        )
                    if not ivalue.get('Description'):
                        self.err.append(
                            self.error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Missing Short Description'
                            )
                        )
                    if ivalue.get('Name') == ivalue.get('Description'):
                        self.err.append(
                            self.error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Equal Name and Short Description Forbidden'
                            )
                        )
                    if ivalue.get('Description') and len(ivalue['Description']) > 250:
                        self.err.append(
                            self.error_message(
                                section = section_map[okey],
                                page = page_name,
                                message = 'Short Description Too Long'
                            )
                        )

    def properties(self, project,data):
        '''Perform Property Checks:
            - Properties present
            - Properties consistent'''

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
                if not ivalue.get('Properties'):
                    self.err.append(
                        self.error_message(
                            section = section_map[okey],
                            page = page_name,
                            message = 'Missing Properties'
                        )
                    )
                else:
                    properties = ivalue['Properties'].values()
                    for key, value in data_properties_check.items():
                        if {self.mathmoddb[key[0]], self.mathmoddb[key[1]]}.issubset(properties):
                            self.err.append(
                                self.error_message(
                                    section = section_map[okey],
                                    page = page_name,
                                    message = f'Inconsistent Properties {value}'
                                )
                            )

    def model(self, project, data):
        '''Perform Model Checks:
            - Connections present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/model"
            )
        )

        if not data.get('model'):
            self.err.append('Mathematical Model: No Mathematical Model Entered')
            return

        for ikey, ivalue in data.get('model',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check Connections
            if not ivalue.get('RelationRP'):
                self.err.append(
                    self.error_message(
                        'Mathematical Model',
                        page_name,
                        'Missing Research Problem'
                    )
                )
            if not ivalue.get('RelationT'):
                self.err.append(
                    self.error_message(
                        'Mathematical Model',
                        page_name,
                        'Missing Computational Task'
                    )
                )
            if not ivalue.get('RelationMF'):
                self.err.append(
                    self.error_message(
                        'Mathematical Model',
                        page_name,
                        'Missing Mathematical Expression'
                    )
                )
            # Relation Connections
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationMF', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Mathematical Model',
                        page_name,
                        'Missing Relation Type (Mathematical Expression)'
                    )
                )
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationMM', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Mathematical Model',
                        page_name,
                        'Missing Relation Type (Mathematical Model)'
                    )
                )
            # Check Qualifier
            for mkey, mval in ivalue.get('RelationMM', {}).items():
                if mval[0] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by']):
                    if not ivalue.get('assumption', {}).get(mkey):
                        self.err.append(
                            self.error_message(
                                'Mathematical Model',
                                page_name,
                                'Missing Assumption '
                                '(Specializes / Specialized By Mathematical Model)'
                            )
                        )
            if ivalue.get('number'):
                if not len(ivalue['number']) == len(ivalue['RelationMF']):
                    self.err.append(
                        self.error_message(
                            'Mathematical Model',
                            page_name,
                            'Missing Order Number (Mathematical Expression)'
                        )
                    )
                numbers = set(map(int, ivalue["number"].values()))
                expected = set(range(1, len(ivalue["number"]) + 1))
                if numbers != expected:
                    self.err.append(
                        self.error_message(
                            'Mathematical Model',
                            page_name,
                            'Incorrect Order Number (Mathematical Expression)'
                        )
                    )

    def task(self, project, data):
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

        if not data.get('task'):
            self.err.append('Computational Task: No Computational Task Entered')
            return

        for ikey, ivalue in data.get('task',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check Connections
            if not ivalue.get('RelationMF'):
                self.err.append(
                    self.error_message(
                        'Computational Task',
                        page_name,
                        'Missing Mathematical Expression'
                    )
                )
            if not ivalue.get('RelationQQK'):
                self.err.append(
                    self.error_message(
                        'Computational Task',
                        page_name,
                        'Missing Quantity / Quantity Kind'
                    )
                )
            # Relation Connections
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationMF', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Computational Task',
                        page_name,
                        'Missing Relation Type (Mathematical Expression)'
                    )
                )
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationQQK', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Computational Task',
                        page_name,
                        'Missing Relation Type (Quantity / Quantity Kind)'
                    )
                )
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationT', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Computational Task',
                        page_name,
                        'Missing Relation Type (Computational Task)'
                    )
                )
            # Check Qualifier
            for tkey, tval in ivalue.get('RelationT', {}).items():
                if tval[0] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by']):
                    if not ivalue.get('assumption', {}).get(tkey):
                        self.err.append(
                            self.error_message(
                                'Computational Task',
                                page_name,
                                'Missing Assumption'
                                '(Specializes / Specialized By Computational Task)'
                            )
                        )
            for tkey, tval in ivalue.get('RelationT', {}).items():
                if tval[0] in (self.mathmoddb['contains'], self.mathmoddb['contained_in']):
                    if not ivalue.get('task_number', {}).get(tkey):
                        self.err.append(
                            self.error_message(
                                'Computational Task',
                                page_name,
                                'Missing Order Number'
                                '(Conatins / Contained In Computational Task)'
                            )
                        )

    def formulation(self, project, data):
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

        if not data.get('formulation'):
            self.err.append('Mathematical Expression: No Mathematical Expression Entered')
            return

        for ikey, ivalue in data.get('formulation',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check Formula
            if not ivalue.get('Formula'):
                self.err.append(
                    self.error_message(
                        'Mathematical Expression',
                        page_name,
                        'Missing Mathematical Expression Formula'
                    )
                )
            # Check Element
            if not ivalue.get('element'):
                self.err.append(
                    self.error_message(
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
                        self.error_message(
                            'Mathematical Expression',
                            page_name,
                            'Missing Mathematical Expression Symbol'
                        )
                    )
                if not_quantity:
                    self.err.append(
                        self.error_message(
                            'Mathematical Expression',
                            page_name,
                            'Missing Mathematical Expression Quantity'
                        )
                    )
            # Relation Connections
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationMF1', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Mathematical Expression',
                        page_name,
                        'Missing Relation Type (Mathematical Expression I)'
                    )
                )
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationMF2', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Mathematical Expression',
                        page_name,
                        'Missing Relation Type (Mathematical Expression II)'
                    )
                )
            # Check Qualifier
            for mkey, mval in ivalue.get('RelationMF2', {}).items():
                if mval[0] in (self.mathmoddb['specializes'], self.mathmoddb['specialized_by']):
                    if not ivalue.get('assumption', {}).get(mkey):
                        self.err.append(
                            self.error_message(
                                'Mathematical Expression',
                                page_name,
                                'Missing Assumption '
                                '(Specializes / Specialized By Mathematical Expression)'
                            )
                        )

    def quantity(self, project, data):
        '''Perform Quantity Checks:
            - Class present
            - Formula is Definition 
            - Elements of Formula present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/quantity"
            )
        )

        if not data.get('quantity'):
            self.err.append('Quantity [Kind]: No Quantity [Kind] Entered')
            return

        for ikey, ivalue in data.get('quantity',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check Class
            if not ivalue.get('QorQK'):
                self.err.append(
                    self.error_message(
                        'Quantity [Kind]',
                        page_name,
                        'Missing [Kind] Class'
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
                            self.error_message(
                                'Quantity [Kind]',
                                page_name,
                                r'Inconsistent Quantity [Kind] Definition (missing \equiv)'
                            )
                        )
                # Check Element
                if not ivalue.get('element'):
                    self.err.append(
                        self.error_message(
                            'Quantity / Quantity Kind',
                            page_name,
                            'Missing Quantity [Kind] Definition Element Information'
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
                            self.error_message(
                                'Quantity [Kind]',
                                page_name,
                                'Missing Quantity [Kind] Definition Symbol'
                            )
                        )
                    if not_quantity:
                        self.err.append(
                            self.error_message(
                                'Quantity [Kind]',
                                page_name,
                                'Missing Quantity [Kind] Definition Quantity'
                            )
                        )
            # Relation Connections
            if ivalue.get('QorQK') == self.mathmoddb['Quantity']:
                if any(
                    'MISSING RELATION TYPE' in val
                    for val in ivalue.get('RelationQQ', {}).values()
                ):
                    self.err.append(
                        self.error_message(
                            'Quantity [Kind]',
                            page_name,
                            'Missing Relation Type (Quantity [Kind])'
                        )
                    )
                if any(
                    'MISSING RELATION TYPE' in val
                    for val in ivalue.get('RelationQQK', {}).values()
                ):
                    self.err.append(
                        self.error_message(
                            'Quantity [Kind]',
                            page_name,
                            'Missing Relation Type (Quantity [Kind])'
                        )
                    )
            elif ivalue.get('QorQK') == self.mathmoddb['QuantityKind']:
                if any(
                    'MISSING RELATION TYPE' in val
                    for val in ivalue.get('RelationQKQK', {}).values()
                ):
                    self.err.append(
                        self.error_message(
                            'Quantity [Kind]',
                            page_name,
                            'Missing Relation Type (Quantity [Kind])'
                        )
                    )
                if any(
                    'MISSING RELATION TYPE' in val
                    for val in ivalue.get('RelationQKQ', {}).values()
                ):
                    self.err.append(
                        self.error_message(
                            'Quantity [Kind]',
                            page_name,
                            'Missing Relation Type (Quantity [Kind])'
                        )
                    )

    def problem(self, project, data):
        '''Perform Problem Checks:
            - Connections present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/problem"
            )
        )

        if not data.get('problem'):
            self.err.append('Research Problem: No Research Problem Entered')
            return

        for ikey, ivalue in data.get('problem',{}).items():
            page_name = values.get(set_index=ikey).text
            # Check Connections
            if not ivalue.get('RelationRF'):
                self.err.append(
                    self.error_message(
                        'Research Problem',
                        page_name,
                        'Missing Academic Discipline'
                    )
                )
            # Relation Connections
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationRP', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Research Problem',
                        page_name,
                        'Missing Relation Type (Research Problem)'
                    )
                )

    def field(self, project, data):
        '''Perform Problem Checks:
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/field"
            )
        )

        if not data.get('field'):
            self.err.append('Academic Discipline: No Academic Discipline Entered')
            return

        for ikey, ivalue in data.get('field',{}).items():
            page_name = values.get(set_index=ikey).text
            # Relation Connections
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationRF', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Academic Discipline',
                        page_name,
                        'Missing Relation Type (Academic Discipline)'
                    )
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

        if not data.get('publication'):
            self.err.append('Publication: No Publication Entered')
            return

        for ikey, ivalue in data.get('publication',{}).items():
            page_name = values.get(set_index=ikey).text
            if ivalue.get('ID') == 'not found' and not ivalue.get('reference'):
                self.err.append(
                    self.error_message(
                        'Publication',
                        page_name,
                        'Missing Publication DOI or URL'
                    )
                )
            # Check Connections
            if not ivalue.get('RelationP'):
                self.err.append(
                    self.error_message(
                        'Publication',
                        page_name,
                        'Missing Mathematical Model Entity'
                    )
                )
            # Relation Connections
            if any(
                'MISSING RELATION TYPE' in val
                for val in ivalue.get('RelationP', {}).values()
            ):
                self.err.append(
                    self.error_message(
                        'Publication',
                        page_name,
                        'Missing Relation Type (Publication)'
                    )
                )

    def run(self, project, data):
        '''Run All Checks'''
        self.id_name_description(project, data)
        self.properties(project, data)
        self.model(project, data)
        self.task(project, data)
        self.formulation(project, data)
        self.quantity(project, data)
        self.problem(project, data)
        self.field(project, data)
        self.publication(project, data)
        if self.err:
            self.err.sort()
            self.err.insert(
                0,
                "Following incomplete or inconsistent aspects prevented the export:"
            )
        return self.err
