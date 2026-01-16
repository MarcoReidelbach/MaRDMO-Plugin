def get_discipline(answers):
    ids = []
    md = 0
    nmd = 0
    for key in answers.get('processstep', []):
        for key2 in answers['processstep'][key].get('discipline', []):
            if answers['processstep'][key]['discipline'][key2].get('ID') and answers['processstep'][key]['discipline'][key2]['ID'] not in ids:
                if 'mardi' in answers['processstep'][key]['discipline'][key2]['ID'] or 'wikidata' in answers['processstep'][key]['discipline'][key2]['ID']:
                    answers.setdefault('nonmathdiscipline', {}).update({nmd: {'ID': answers['processstep'][key]['discipline'][key2]['ID'],
                                                                              'Name': answers['processstep'][key]['discipline'][key2]['Name']}})
                    nmd += 1
                    ids.append(answers['processstep'][key]['discipline'][key2]['ID'])
                elif 'msc' in answers['processstep'][key]['discipline'][key2]['ID']:
                    answers.setdefault('mathsubject', {}).update({md: {'ID': answers['processstep'][key]['discipline'][key2]['ID'],
                                                                       'Name': answers['processstep'][key]['discipline'][key2]['Name']}})
                    md += 1
                    ids.append(answers['processstep'][key]['discipline'][key2]['ID'])
    return answers


