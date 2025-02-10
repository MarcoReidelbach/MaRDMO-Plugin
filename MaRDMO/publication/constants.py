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
