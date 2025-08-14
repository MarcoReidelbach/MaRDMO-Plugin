def mapEntityQuantity(data, type, mapping):
    for key in data.get(type, {}):
        for key2 in data[type][key].get('element',{}):
            for k in data.get('quantity', {}):
                if data[type][key]['element'][key2].get('quantity', {}).get('Name', '').lower() == data['quantity'][k]['Name'].lower():
                    if data['quantity'][k].get('QorQK') == mapping['Quantity']:
                        data[type][key]['element'][key2].update(
                            {'Info': 
                                {'Type': mapping['Quantity'],
                                 'Name':data['quantity'][k].get('Name',''),
                                 'Description':data['quantity'][k].get('Description',''),
                                 'ID':data['quantity'][k].get('ID','') if data['quantity'][k].get('ID','') and data['quantity'][k].get('ID','') != 'not found' else data['quantity'][k].get('Reference','') if data['quantity'][k].get('Reference','') else '', 
                                 'QKName':data['quantity'][k].get('QKRelatant', {}).get(0, {}).get('Name', ''),
                                 'QKID':data['quantity'][k].get('QKRelatant', {}).get(0, {}).get('ID', '')}
                            })
                    elif data['quantity'][k].get('QorQK') == mapping['QuantityKind']:
                        data[type][key]['element'][key2].update(
                            {'Info':
                                {'Type': mapping['QuantityKind'],
                                 'Name':data['quantity'][k].get('Name',''),
                                 'Description':data['quantity'][k].get('Description',''),
                                 'ID':data['quantity'][k].get('ID','') if data['quantity'][k].get('ID','') and data['quantity'][k].get('ID','') != 'not found' else ''}
                            })
    return






                    
