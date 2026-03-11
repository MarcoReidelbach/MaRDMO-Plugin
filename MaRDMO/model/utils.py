'''Module containing Utility Functions for the Model Documentation'''

from .constants import DEPENDENT_PROPERTIES, INDEPENDENT_PROPERTIES

from ..getters import get_items, get_mathmoddb

def get_data_properties(item_type):
    """Get Data Properties Mapping"""

    # Get MathModDB Mapping and Items
    mathmoddb = get_mathmoddb()
    items = get_items()

    # Add class-independent Properties
    properties = {
        mathmoddb.get(key=k)["url"]: items.get(label)
        for k, label in INDEPENDENT_PROPERTIES
    }

    # Add class-dependent Properties
    properties.update({
        mathmoddb.get(key=k)["url"]: items.get(f'{label} {item_type}')
        for k, label in DEPENDENT_PROPERTIES
    })

    return properties

def build_quantity_info(quantity, qtype):
    """Build the Info dict for a Quantity or QuantityKind."""
    base_info = {
        "Type": qtype,
        "Name": quantity.get("Name", ""),
        "Description": quantity.get("Description", ""),
        "ID": quantity.get("ID", ""),
    }

    # Only Quantity has QKRelatant
    if qtype == "Quantity":
        base_info["QKName"] = quantity.get("QKRelatant-Q", {}).get(0, {}).get(0, {}).get("Name", "")
        base_info["QKID"] = quantity.get("QKRelatant-Q", {}).get(0, {}).get(0, {}).get("ID", "")

    return base_info


def map_entity_quantity(data, entity_type):
    """Map quantities or quantity kinds to entity elements."""
    for entity in data.get(entity_type, {}).values():
        for element in entity.get("element", {}).values():
            element_quantity_name = element.get("quantity", {}).get("Name", "").lower()

            for quantity in data.get("quantity", {}).values():
                quantity_name = quantity.get("Name", "").lower()

                if element_quantity_name != quantity_name:
                    continue

                qtype = quantity.get("QorQK")

                if qtype in ('Quantity', 'Quantity Kind'):
                    element["Info"] = build_quantity_info(quantity, qtype)

def error_message(section, page, message):
    '''Generate Error Message'''
    return f"{section} (Page {page}): {message}"

def check_relation_static(data, page_name, error, relation, from_class, to_class):
    '''Check Components of static Statements'''
    if not data.get(relation):
        error.append(
            error_message(
                section = from_class,
                page = page_name,
                message = f'Missing {to_class}'
            )
        )
    elif 'not found' in data.get(relation, {}).values():
        error.append(
            error_message(
                section = from_class,
                page = page_name,
                message = f'Selected {to_class} not found in {to_class} Section'
            )
        )

def check_relation_flexible(
        data,
        page_name,
        error,
        relation,
        from_class,
        to_class=None,
        optional=True
):
    '''Check Components of flexible Statements'''
    # If no section name provided use class name
    if not to_class:
        to_class = from_class
    # Check Expression Connections
    if not optional:
        if not data.get(relation):
            error.append(
                error_message(
                    section = from_class,
                    page = page_name,
                    message = f'Missing {to_class}'
                )
            )
    # Check Missing Relation Type
    if any(
        val['relation'] is None
        for val in data.get(relation, {}).values()
    ):
        error.append(
            error_message(
                section = from_class,
                page = page_name,
                message = f'Missing Relation Type ({to_class})'
            )
        )
    # Check Missing Object Item
    if any(
        val['relatant'] == 'MISSING OBJECT ITEM'
        for val in data.get(relation, {}).values()
    ):
        error.append(
            error_message(
                section = from_class,
                page = page_name,
                message = f'Missing Object Item ({to_class})'
            )
        )
    # Check Not Found Item
    if any(
        val['relatant'] == 'not found'
        for val in data.get(relation, {}).values()
    ):
        error.append(
            error_message(
                section = from_class,
                page = page_name,
                message = f'Selected {to_class} not found in {to_class} Section'
            )
        )
