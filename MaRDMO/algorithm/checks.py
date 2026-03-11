'''Module containing Checks for the Model Documentation'''

from rdmo.domain.models import Attribute

from .constants import SECTION_MAP
from ..model.utils import error_message, check_relation_flexible, check_relation_static

from ..constants import BASE_URI
from ..getters import get_mathalgodb

class Checks:
    '''Check Class checks User Answers upon Transfer to MaRDI Portal'''
    def __init__(self):
        self.mathalgodb = get_mathalgodb()
        self.err = []

    def id_name_description(self, project, data):
        '''Perform ID, Name and Description Checks:
            - ID, Name, Description present'''

        okeys = ('algorithm', 'problem', 'software', 'benchmark', 'publication')

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
                                section = SECTION_MAP[okey],
                                page = page_name,
                                message = 'Missing ID'
                            )
                        )
                    if not ivalue.get('Name'):
                        self.err.append(
                            error_message(
                                section = SECTION_MAP[okey],
                                page = page_name,
                                message = 'Missing Name'
                            )
                        )
                    if not ivalue.get('Description'):
                        self.err.append(
                            error_message(
                                section = SECTION_MAP[okey],
                                page = page_name,
                                message = 'Missing Short Description'
                            )
                        )
                    if ivalue.get('Name') == ivalue.get('Description'):
                        self.err.append(
                            error_message(
                                section = SECTION_MAP[okey],
                                page = page_name,
                                message = 'Equal Name and Short Description Forbidden'
                            )
                        )
                    if ivalue.get('Description') and len(ivalue['Description']) > 250:
                        self.err.append(
                            error_message(
                                section = SECTION_MAP[okey],
                                page = page_name,
                                message = 'Short Description Too Long'
                            )
                        )

    def algorithm(self, project, data):
        '''Perform Algorithm Checks:
            - Connections present
            - Relations present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/algorithm"
            )
        )

        for ikey, ivalue in data.get('algorithm',{}).items():
            page_name = values.get(set_index=ikey).text

            # Check mandatory static AL-AT Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationP',
                from_class = 'Algorithm',
                to_class = 'Algorithmic Task'
            )

            # Check mandatory static AL-SO Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationS',
                from_class = 'Algorithm',
                to_class = 'Software'
            )

            # Check optional flexible AL-AL Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationA',
                from_class = 'Algorithm'
            )

    def problem(self, project, data):
        '''Perform Algorithmic Task Checks:
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

            # Check mandatory static AT-BE Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationB',
                from_class = 'Algorithmic Task',
                to_class = 'Benchmark'
            )

            # Check optional flexible AT-AT Statements
            check_relation_flexible(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationP',
                from_class = 'Algorithmic Task'
            )

    def software(self, project, data):
        '''Perform Software Checks:
            - Relations present
            - References present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/software"
            )
        )

        for ikey, ivalue in data.get('software',{}).items():
            page_name = values.get(set_index=ikey).text

            # Check mandatory static SO-BE Statements
            check_relation_static(
                data = ivalue,
                page_name = page_name,
                error = self.err,
                relation = 'RelationB',
                from_class = 'Software',
                to_class = 'Benchmark'
            )

            # Software Reference IDs
            if ivalue.get('reference'):
                # Check if ID for selected Option is provided
                if ivalue['reference'].get(0) and not ivalue['reference'][0][1]:
                    self.err.append(
                        error_message(
                            'Software',
                            page_name,
                            'DOI selected, but no ID provided!'
                        )
                    )
                if ivalue['reference'].get(1) and not ivalue['reference'][1][1]:
                    self.err.append(
                        error_message(
                            'Software',
                            page_name,
                            'swMath ID selected, but no ID provided!'
                        )
                    )
                if ivalue['reference'].get(2) and not ivalue['reference'][2][1]:
                    self.err.append(
                        error_message(
                            'Software',
                            page_name,
                            'Description URL selected, but no URL provided!'
                        )
                    )
                if ivalue['reference'].get(3) and not ivalue['reference'][3][1]:
                    self.err.append(
                        error_message(
                            'Software',
                            page_name,
                            'Repository URL selected, but no URL provided!'
                        )
                    )
                

    def benchmark(self, project, data):
        '''Perform Benchmark Checks:
            - References present'''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f"{BASE_URI}domain/benchmark"
            )
        )

        for ikey, ivalue in data.get('benchmark',{}).items():
            page_name = values.get(set_index=ikey).text
            
            # Software Reference IDs
            if ivalue.get('reference'):
                # Check if ID for selected Option is provided
                if ivalue['reference'].get(0) and not ivalue['reference'][0][1]:
                    self.err.append(
                        error_message(
                            'Benchmark',
                            page_name,
                            'DOI selected, but no ID provided!'
                        )
                    )
                if ivalue['reference'].get(1) and not ivalue['reference'][1][1]:
                    self.err.append(
                        error_message(
                            'Benchmark',
                            page_name,
                            'MORwiki ID selected, but no ID provided!'
                        )
                    )
                if ivalue['reference'].get(2) and not ivalue['reference'][2][1]:
                    self.err.append(
                        error_message(
                            'Benchmark',
                            page_name,
                            'Description URL selected, but no URL provided!'
                        )
                    )
                if ivalue['reference'].get(3) and not ivalue['reference'][3][1]:
                    self.err.append(
                        error_message(
                            'Benchmark',
                            page_name,
                            'Repository URL selected, but no URL provided!'
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

        for ikey, ivalue in data.get('publication',{}).items():
            page_name = values.get(set_index=ikey).text
            if ivalue.get('ID') == 'not found' and not ivalue.get('reference'):
                self.err.append(
                    error_message(
                        'Publication',
                        page_name,
                        'Missing Publication DOI'
                    )
                )

            if ivalue.get('RelationA') or ivalue.get('RelationBS'):
                # Check optional flexible P-A Statements
                check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationA',
                    from_class = 'Publication',
                    to_class = 'Algorithm',
                    optional = True
                )
                # Check optional flexible P-BS Statements
                check_relation_flexible(
                    data = ivalue,
                    page_name = page_name,
                    error = self.err,
                    relation = 'RelationBS',
                    from_class = 'Publication',
                    to_class = 'Benchmark/Software',
                    optional = True
                )
            else:
                self.err.append(
                    error_message(
                        'Publication',
                        page_name,
                        'Missing Algorithm, Benchmark, or Software '
                    )
                )

    def run(self, project, data):
        '''Run All Checks'''
        self.id_name_description(project, data)
        self.algorithm(project, data)
        self.problem(project, data)
        self.software(project, data)
        self.benchmark(project, data)
        self.publication(project, data)
        if self.err:
            self.err.sort()
            self.err.insert(
                0,
                "Following incomplete or inconsistent aspects prevented the export:"
            )
        return self.err
