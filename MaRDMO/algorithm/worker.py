from ..helpers import entityRelations

def algorithm_relations(instance, answers, mathalgodb):
    '''Function to establish relations between Algorithm Documentation Data'''
     
    # Algorithmic Problem to Algorithm Relations
    entityRelations(answers,'algorithm','problem','A2P','PRelatant','RelationP','AP')

    # Software to Algorithm Relations
    entityRelations(answers,'algorithm','software','A2S','SRelatant','RelationS','S')

    # Algorithm to Algorithm Relations
    entityRelations(answers,'algorithm','algorithm','IntraClassRelation','IntraClassElement','RelationA','A')

    # Algorithmic Problem to Benchmark Relations
    entityRelations(answers,'problem','benchmark','P2B','BRelatant','RelationB','B')

    # Algorithmic Problem to Algorithmic Problem Relations
    entityRelations(answers,'problem','problem','IntraClassRelation','IntraClassElement','RelationP','AP')

    # Software to Benchmark Relations
    entityRelations(answers,'software','benchmark','S2B','BRelatant','RelationB','B')

    # Publication to Algorithm Relations
    entityRelations(answers,'publication','algorithm','P2A','ARelatant','RelationA','A')

    # Publication to Benchmark Relations
    entityRelations(answers,'publication','benchmark','P2B','BRelatant','RelationB','B')

    # Publication to Software Relations
    entityRelations(answers,'publication','software','P2S','SRelatant','RelationS','S')

    return answers