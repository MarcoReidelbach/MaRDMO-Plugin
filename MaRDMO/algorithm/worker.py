from ..helpers import entity_relations

def algorithm_relations(answers):
    '''Function to establish relations between Algorithm Documentation Data'''
     
    # Algorithmic Problem to Algorithm Relations
    entity_relations(answers,'algorithm','problem','A2P','PRelatant','RelationP','AP')

    # Software to Algorithm Relations
    entity_relations(answers,'algorithm','software','A2S','SRelatant','RelationS','S')

    # Algorithm to Algorithm Relations
    entity_relations(answers,'algorithm','algorithm','IntraClassRelation','IntraClassElement','RelationA','A')

    # Algorithmic Problem to Benchmark Relations
    entity_relations(answers,'problem','benchmark','P2B','BRelatant','RelationB','B')

    # Algorithmic Problem to Algorithmic Problem Relations
    entity_relations(answers,'problem','problem','IntraClassRelation','IntraClassElement','RelationP','AP')

    # Software to Benchmark Relations
    entity_relations(answers,'software','benchmark','S2B','BRelatant','RelationB','B')

    # Publication to Algorithm Relations
    entity_relations(answers,'publication','algorithm','P2A','ARelatant','RelationA','A')

    # Publication to Benchmark Relations
    entity_relations(answers,'publication','benchmark','P2B','BRelatant','RelationB','B')

    # Publication to Software Relations
    entity_relations(answers,'publication','software','P2S','SRelatant','RelationS','S')

    return answers