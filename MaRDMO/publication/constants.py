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
    "Name": "title",
    "Description": "description",
    "Entrytype": "entrytype",
    "Title": "title",
    "Date": "date",
    "Volume": "volume",
    "Issue": "issue",
    "Page": "page"
}

# URI mappings for languages
LANGUAGES = {
    "Language ID": "id",
    "Language Name": "label",
    "Language Description": "description"
}

# URI mappings for journals
JOURNALS = {
    "Journal ID": "id",
    "Journal ISSN": "issn",
    "Journal Name": "label",
    "Journal Description": "description"
}

# URI mappings for author
AUTHORS = {
    "Author ID": "id",
    "Author ORCID": "orcid_id",
    "Author ZBMath": "zbmath_id",
    "Author Wikidata": "wikidata_id",
    "Author Name": "label",
    "Author Description": "description"
}