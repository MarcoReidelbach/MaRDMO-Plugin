PROPS = {
    'P2E': ['documents','invents','studies','surveys','uses'],
    'P2A': ['analyzes','applies','invents','studies','surveys'],
    'P2BS': ['documents', 'uses']
}

# Index counters for different cenchmarks and software
INDEX_COUNTERS = {
    "benchmark": 0,
    "software": 0
}

# URI mappings for quantity relations
RELATION_URIS = {
    "benchmark": "Publication P2B",
    "software": "Publication P2S",
}

# URI mappings for quantity relatants
RELATANT_URIS = {
    "benchmark": "Publication BRelatant",
    "software": "Publication SRelatant",
}

# URI mappings for publications
PUBLICATIONS = {
    "Publication Name": "title",
    "Publication Description": "description",
    "Publication Entrytype": "entrytype",
    "Publication Title": "title",
    "Publication Date": "date",
    "Publication Volume": "volume",
    "Publication Issue": "issue",
    "Publication Page": "page"
}

# URI mappings for languages
LANGUAGES = {
    "Publication Language ID": "id",
    "Publication Language Name": "label",
    "Publication Language Description": "description"
}

# URI mappings for journals
JOURNALS = {
    "Publication Journal ID": "id",
    "Publication Journal ISSN": "issn",
    "Publication Journal Name": "label",
    "Publication Journal Description": "description"
}

# URI mappings for author
AUTHORS = {
    "Publication Author ID": "id",
    "Publication Author ORCID": "orcid_id",
    "Publication Author ZBMath": "zbmath_id",
    "Publication Author Wikidata": "wikidata_id",
    "Publication Author Name": "label",
    "Publication Author Description": "description"
}