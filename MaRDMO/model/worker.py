'''Worker Module for Model Preview and Export'''

import logging
import time

from .utils import map_entity_quantity
from .constants import (
    preview_relations,
    preview_map_general,
    preview_map_quantity,
    get_relations,
    get_data_properties
)

from ..config import endpoint
from ..getters import get_items, get_mathmoddb, get_properties
from ..helpers import entity_relations, map_entity, unique_items, date_precision
from ..queries import query_sparql
from ..payload import GeneratePayload


class PrepareModel:
    '''Class preparing Model Answers for Preview and Export'''
    def __init__(self):

        self.mathmoddb = get_mathmoddb()
        self.items = get_items()
        self.properties = get_properties()

    def preview(self, answers):
        '''Function to establish relations between Model Documentation Data'''

        # Prepare Relations for Preview
        for relation in preview_relations:
            entity_relations(
                data = answers,
                idx = {
                    'from': relation['from_idx'],
                    'to': relation['to_idx']
                },
                entity = {
                    'relation': relation['relation'],
                    'old_name': relation['old_name'],
                    'new_name': relation['new_name'],
                    'encryption': relation['encryption']
                },
                order = {
                    'formulation': relation['formulation'],
                    'task': relation['task']
                }
            )

        # Prepare General Mappings
        for mapping in preview_map_general:
            map_entity(
                data = answers,
                idx = {
                    'from': mapping[0], 
                    'to': mapping[1]
                },
                entity = {
                    'old_name': mapping[2], 
                    'new_name': mapping[3], 
                    'encryption': mapping[4]
                }
            )

        # Prepare Quantity Mapping
        for mapping in preview_map_quantity:
            map_entity_quantity(
                data= answers,
                entity_type = mapping,
                mapping = self.mathmoddb)

        return answers

    def export(self, data, url):
        """Function to create Payload for Model Export."""

        items = unique_items(data)

        payload = GeneratePayload(
            url,
            items,
            get_relations(),
            get_data_properties,
        )

        # Add / Retrieve Components of Model Item
        payload.process_items()

        # Delegate to helper functions
        self._export_fields(payload, data.get("field", {}), data.get("problem", {}))
        self._export_problems(payload, data.get("model", {}), data.get("problem", {}))
        self._export_models(payload, data.get("model", {}))
        self._export_tasks(payload, data.get("task", {}))
        self._export_formulations(payload, data.get("formulation", {}))
        self._export_quantities(payload, data.get("quantity", {}))
        self._export_publications(payload, data.get("publication", {}))

        # Construct Item Payloads
        payload.add_item_payload()

        # If Relations are added, check if they exist
        if any(
            key.startswith("RELATION")
            for key in payload.get_dictionary()
        ):
            query = payload.build_relation_check_query()

            check = None
            for attempt in range(2):  # try twice
                try:
                    check = query_sparql(query, endpoint["mardi"]["sparql"])
                    break
                except Exception as e:
                    logging.warning("SPARQL query attempt %s failed: %s", attempt + 1, e)
                    if attempt == 0:
                        time.sleep(1)  # short wait before retry
            if check is None:
                # both attempts failed → pretend no results
                check = [{}]

            payload.add_check_results(check)

        return payload.get_dictionary()

    # ---------------------------
    # Shared helper
    # ---------------------------
    def _add_common_metadata(self, payload, qclass, profile_type):
        """Add metadata common to most entities (except publication)."""
        payload.add_answer(
            self.properties["instance of"],
            [qclass, "wikibase-item"],
        )
        payload.add_answer(
            self.properties["community"],
            [self.items["MathModDB"], "wikibase-item"],
        )
        payload.add_answer(
            self.properties["MaRDI profile type"],
            [self.items[profile_type], "wikibase-item"],
        )
        payload.add_answers(
            "descriptionLong",
            "description",
        )

    # ---------------------------
    # Entity export helpers
    # ---------------------------
    def _export_fields(self, payload, fields: dict, problems: dict):
        for entry in fields.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)
            self._add_common_metadata(
                payload,
                self.items["academic discipline"],
                "MaRDI research field profile",
            )

            payload.add_backward_relation(
                problems.values(),
                self.properties["contains"],
                "RFRelatant",
            )

            payload.add_intra_class_relation(
                "IntraClassRelation",
                "IntraClassElement",
            )

    def _export_problems(self, payload, models: dict, problems: dict):
        for entry in problems.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)
            self._add_common_metadata(
                payload,
                self.items["research problem"],
                "MaRDI research problem profile",
            )

            payload.add_backward_relation(
                models.values(),
                self.properties["modelled by"],
                "RPRelatant",
            )

            payload.add_intra_class_relation(
                "IntraClassRelation",
                "IntraClassElement",
            )

    def _export_models(self, payload, models: dict):
        for entry in models.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)
            self._add_common_metadata(
                payload,
                self.items["mathematical model"],
                "MaRDI model profile",
            )

            payload.add_data_properties("model")
            payload.add_forward_relation_multiple(
                "MM2MF",
                "MFRelatant",
            )
            payload.add_forward_relation_single(
                self.properties["used by"],
                "TRelatant",
            )
            payload.add_intra_class_relation(
                "IntraClassRelation",
                "IntraClassElement",
            )

    def _export_tasks(self, payload, tasks: dict):
        for entry in tasks.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)
            self._add_common_metadata(
                payload,
                self.items["computational task"],
                "MaRDI task profile",
            )

            payload.add_data_properties("task")
            payload.add_forward_relation_multiple(
                "T2MF",
                "MFRelatant",
            )
            payload.add_forward_relation_multiple(
                "T2Q",
                "QRelatant",
            )
            payload.add_intra_class_relation(
                "IntraClassRelation",
                "IntraClassElement",
            )

    def _export_formulations(self, payload, formulations: dict):
        for entry in formulations.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)
            self._add_common_metadata(
                payload,
                self.items["mathematical expression"],
                "MaRDI formula profile",
            )

            payload.add_data_properties("equation")
            payload.add_answers(
                "Formula",
                "defining formula",
                "math",
            )
            payload.add_in_defining_formula()
            payload.add_forward_relation_multiple(
                "MF2MF",
                "MFRelatant",
            )
            payload.add_intra_class_relation(
                "IntraClassRelation",
                "IntraClassElement",
            )

    def _export_quantities(self, payload, quantities: dict):
        for entry in quantities.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)

            if entry.get("QorQK") == self.mathmoddb["Quantity"]:
                self._add_common_metadata(
                    payload,
                    self.items["quantity"],
                    "MaRDI quantity profile",
                )
                qtype = "quantity"

            elif entry.get("QorQK") == self.mathmoddb["QuantityKind"]:
                self._add_common_metadata(
                    payload,
                    self.items["kind of quantity"],
                    "MaRDI quantity profile",
                )
                qtype = "quantity kind"

            else:
                continue

            payload.add_data_properties(qtype)

            if (
                entry.get("reference")
                and qtype == "quantity kind"
            ):
                payload.add_answer(
                    self.properties["QUDT quantity kind ID"],
                    [entry["reference"][0][1], "external-id"],
                )

            payload.add_answers(
                "Formula",
                "defining formula",
                "math",
            )
            payload.add_in_defining_formula()

            if qtype == "quantity":
                payload.add_intra_class_relation(
                    "Q2Q",
                    "QRelatant",
                )
                payload.add_intra_class_relation(
                    "Q2QK",
                    "QKRelatant",
                )
            else:
                payload.add_intra_class_relation(
                    "QK2QK",
                    "QKRelatant",
                )
                payload.add_intra_class_relation(
                    "QK2Q",
                    "QRelatant",
                )

    def _export_publications(self, payload, publications: dict):
        for entry in publications.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(entry)

            # Only add bibliographic statements for non-MaRDI / non-Wikidata items
            if "mardi" not in entry["ID"] and "wikidata" not in entry["ID"]:
                # class
                if entry.get("entrytype") == "scholarly article":
                    pclass = self.items["scholarly article"]
                else:
                    pclass = self.items["publication"]

                payload.add_answer(
                    self.properties["instance of"],
                    [pclass, "wikibase-item"],
                )

                # bibliographic data
                if entry.get("title"):
                    payload.add_answer(
                        self.properties["title"],
                        [
                            {"text": entry["title"], "language": "en"},
                            "monolingualtext",
                        ],
                    )

                if entry.get("volume"):
                    payload.add_answer(
                        self.properties["volume"],
                        [entry["volume"], "string"],
                    )

                if entry.get("issue"):
                    payload.add_answer(
                        self.properties["issue"],
                        [entry["issue"], "string"],
                    )

                if entry.get("page"):
                    payload.add_answer(
                        self.properties["page(s)"],
                        [entry["page"], "string"],
                    )

                if entry.get("date"):
                    payload.add_answer(
                        self.properties["publication date"],
                        [
                            {
                                "time": f"+{entry['date']}",
                                "precision": date_precision(entry['date']),
                                "calendarmodel": (
                                    "http://www.wikidata.org/entity/Q1985727"
                                ),
                            },
                            "time",
                        ],
                    )

                if entry.get("reference", {}).get(0):
                    payload.add_answer(
                        self.properties["DOI"],
                        [entry["reference"][0][1].upper(), "external-id"],
                    )

                # relations
                payload.add_forward_relation_single(
                    self.properties["language of work or name"],
                    "language",
                )
                payload.add_forward_relation_single(
                    self.properties["published in"],
                    "journal",
                )
                payload.add_forward_relation_single(
                    self.properties["author"],
                    "author",
                    alternative={
                        "relation": self.properties["author name string"],
                        "relatant": "Name",
                    },
                )

                payload.add_answer(
                    self.properties["MaRDI profile type"],
                    [self.items["MaRDI publication profile"], "wikibase-item"],
                )

            # Add relations to Entities of Mathematical Model
            payload.add_forward_relation_multiple(
                "P2E",
                "EntityRelatant",
                True,
            )
