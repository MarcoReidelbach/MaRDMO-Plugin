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


