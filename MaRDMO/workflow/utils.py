'''Module containing Utility Functions for the Workflow Documentation'''

from .constants import data_set_reference_ids

def get_discipline(answers):
    ids = []
    md = 0
    nmd = 0
    for key in answers.get('processstep', []):
        for key2 in answers['processstep'][key].get('discipline', []):
            if not answers['processstep'][key]['discipline'][key2].get('ID'):
                continue
            if answers['processstep'][key]['discipline'][key2]['ID'] in ids:
                continue
            if answers['processstep'][key]['discipline'][key2]['ID'].split(':')[0] in ('mardi', 'wikidata'):
                answers.setdefault('nonmathdiscipline', {}).update(
                    {
                        nmd:
                            {
                                'ID': answers['processstep'][key]['discipline'][key2]['ID'],
                                'Name': answers['processstep'][key]['discipline'][key2]['Name']
                            }
                    }
                )
                nmd += 1
                ids.append(answers['processstep'][key]['discipline'][key2]['ID'])
            elif answers['processstep'][key]['discipline'][key2]['ID'].split(':')[0] == 'msc':
                answers.setdefault('mathsubject', {}).update(
                    {
                        md:
                            {
                                'ID': answers['processstep'][key]['discipline'][key2]['ID'],
                                'Name': answers['processstep'][key]['discipline'][key2]['Name']
                            }
                    }
                )
                md += 1
                ids.append(answers['processstep'][key]['discipline'][key2]['ID'])
    return answers

def get_size(data, options):
    '''Function which extracts the type and size of data set'''
    size_unit = data.get('size_unit', {}).get('value', '')
    size_value = data.get('size_value', {}).get('value', '')
    size_record = data.get('size_record', {}).get('value', '')

    unit = options.get(size_unit) if size_unit else (options['items'] if size_record else '')
    value = size_value or size_record

    return [unit, value] if unit and value else []

def get_reference(data, options):
    '''Function which extracts the references of a data set'''
    result = {}

    for idx, key in enumerate(data_set_reference_ids):
        if key in ('Yes', 'No'):
            if value := data.get('publish', {}).get('value') == key:
                result[idx] = [options[key], '']
        else:
            if value := data.get(key, {}).get('value'):
                result[idx] = [options[key], value]

    return result

def get_archive(data, options):
    '''Function which extracts the archival information of a data set'''
    archive = options[data['archive']['value']] if data.get('archive', {}).get('value') else ''
    year = data.get('end_time', {}).get('value', '')[:4]
    return [archive, year] if archive else []
