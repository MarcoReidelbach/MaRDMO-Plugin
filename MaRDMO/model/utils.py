'''Module containing Utility Functions for the Model Documentation'''

def build_quantity_info(quantity, qtype):
    """Build the Info dict for a Quantity or QuantityKind."""
    base_info = {
        "Type": qtype,
        "Name": quantity.get("Name", ""),
        "Description": quantity.get("Description", ""),
        "ID": (
            quantity.get("ID", "")
            if quantity.get("ID", "") and quantity.get("ID", "") != "not found"
            else quantity.get("Reference", "")
            if qtype == "Quantity" and quantity.get("Reference", "")
            else ""
        ),
    }

    # Only Quantity has QKRelatant
    if qtype == "Quantity":
        base_info["QKName"] = quantity.get("QKRelatant", [{}])[0].get("Name", "")
        base_info["QKID"] = quantity.get("QKRelatant", [{}])[0].get("ID", "")

    return base_info


def map_entity_quantity(data, entity_type, mapping):
    """Map quantities or quantity kinds to entity elements."""
    for entity in data.get(entity_type, {}).values():
        for element in entity.get("element", {}).values():
            element_quantity_name = element.get("quantity", {}).get("Name", "").lower()

            for quantity in data.get("quantity", {}).values():
                quantity_name = quantity.get("Name", "").lower()

                if element_quantity_name != quantity_name:
                    continue

                qtype = quantity.get("QorQK")
                if qtype in mapping.values():
                    element["Info"] = build_quantity_info(quantity, qtype)
