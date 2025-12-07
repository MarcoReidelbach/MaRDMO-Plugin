'''Module containing Constants for the Publication Documentation'''

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
    "benchmark": "P2B",
    "software": "P2S",
}

# URI mappings for quantity relatants
RELATANT_URIS = {
    "benchmark": "BRelatant",
    "software": "SRelatant",
}

# URI mappings for item infos
ITEMINFOS = {
    "Name": "title",
    "Description": "description"
}

# URI mappings for citation infos
CITATIONINFOS = {
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
