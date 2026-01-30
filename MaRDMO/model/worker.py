'''Worker Module for Model Preview and Export'''

import logging
import time

from .utils import map_entity_quantity
from .constants import (
    preview_relations,
    preview_map_general,
    preview_map_quantity,
    get_relations,
    get_data_properties,
)

from ..getters import get_items, get_mathmoddb, get_properties, get_url
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
                },
                assumption = relation['assumption']
            )

        # Prepare Quantity Mapping
        for mapping in preview_map_quantity:
            map_entity_quantity(
                data = answers,
                entity_type = mapping,
                mapping = self.mathmoddb)

        return answers

    def export(self, data, url):
        """Function to create Payload for Model Export."""

        items, dependency = unique_items(data)

        payload = GeneratePayload(
            dependency = dependency,
            user_items = items,
            url = url,
            wikibase = {
                'data_properties': get_data_properties,
                'items': get_items(),
                'properties': get_properties(),
                'relations': get_relations()
            }
        )

        # Add / Retrieve Components of Model Item
        payload.process_items()

        # Delegate to helper functions
        self._export_fields(
            payload = payload,
            fields = data.get("field", {}),
        )
        self._export_problems(
            payload = payload,
            problems = data.get("problem", {})
        )
        self._export_models(
            payload = payload,
            models = data.get("model", {})
        )
        self._export_tasks(
            payload = payload,
            tasks = data.get("task", {})
        )
        self._export_formulations(
            payload = payload,
            formulations = data.get("formulation", {})
        )
        self._export_quantities(
            payload = payload,
            quantities = data.get("quantity", {})
        )
        self._export_authors(
            payload = payload,
            publications = data.get("publication", {})
        )
        self._export_journals(
            payload = payload,
            publications = data.get("publication", {})
        )
        self._export_publications(
            payload = payload,
            publications = data.get("publication", {})
        )

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
                    check = query_sparql(
                        query = query,
                        sparql_endpoint = get_url('mardi', 'sparql')
                    )
                    break
                except Exception as e:
                    logging.warning("SPARQL query attempt %s failed: %s", attempt + 1, e)
                    if attempt == 0:
                        time.sleep(1)  # short wait before retry
            if not check:
                # both attempts failed → pretend no results
                check = [{}]

            payload.add_check_results(
                check = check
            )
        return payload.get_dictionary(), payload.dependency

    # ---------------------------
    # Shared helper
    # ---------------------------
    def _add_common_metadata(self, payload, qclass, profile_type):
        """Add metadata common to most entities (except publication)."""
        payload.add_answer(
            verb = self.properties["instance of"],
            object_and_type = [qclass, "wikibase-item"],
        )

        payload.add_answer(
            verb = self.properties["community"],
            object_and_type = [self.items["MathModDB"], "wikibase-item"],
        )

        payload.add_answer(
            verb = self.properties["MaRDI profile type"],
            object_and_type = [self.items[profile_type], "wikibase-item"],
        )

        payload.add_answers(
            mardmo_property = "descriptionLong",
            wikibase_property = "description",
        )

    # ---------------------------
    # Entity export helpers
    # ---------------------------
    def _export_fields(self, payload, fields: dict):
        for entry in fields.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["academic discipline"],
                profile_type = "MaRDI research field profile",
            )

            payload.add_aliases(
                aliases_dict = entry.get('Alias')
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "IntraClassRelation",
                    'relatant': "IntraClassElement"
                }
            )

    def _export_problems(self, payload, problems: dict):
        for entry in problems.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["research problem"],
                profile_type = "MaRDI research problem profile",
            )

            payload.add_aliases(
                aliases_dict = entry.get('Alias')
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["contains"],
                    'relatant': "RFRelatant"
                },
                reverse = True
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "IntraClassRelation",
                    'relatant': "IntraClassElement"
                }
            )

    def _export_models(self, payload, models: dict):
        for entry in models.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["mathematical model"],
                profile_type = "MaRDI model profile",
            )

            payload.add_aliases(
                aliases_dict = entry.get('Alias')
            )

            payload.add_data_properties(
                item_class = "model"
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "MM2MF",
                    'relatant': "MFRelatant"
                },
                optional_qualifier = ['series ordinal']
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["modelled by"],
                    'relatant': "RPRelatant"
                },
                reverse = True
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["used by"],
                    'relatant': "TRelatant"
                }
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "IntraClassRelation",
                    'relatant': "IntraClassElement"
                },
                optional_qualifier = ['assumes']
            )

    def _export_tasks(self, payload, tasks: dict):
        for entry in tasks.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["computational task"],
                profile_type = "MaRDI task profile",
            )

            payload.add_aliases(
                aliases_dict = entry.get('Alias')
            )

            payload.add_data_properties(
                item_class = "task"
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "T2MF",
                    'relatant': "MFRelatant"
                }
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "T2Q",
                    'relatant': "QRelatant"
                }
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "IntraClassRelation",
                    'relatant': "IntraClassElement"
                },
                optional_qualifier = ['assumes', 'series ordinal']
            )

    def _export_formulations(self, payload, formulations: dict):
        for entry in formulations.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["mathematical expression"],
                profile_type = "MaRDI formula profile",
            )

            payload.add_aliases(
                aliases_dict = entry.get('Alias')
            )

            payload.add_data_properties(
                item_class = "equation"
            )

            if entry.get('reference'):
                payload.add_answer(
                    verb = self.properties["comment"],
                    object_and_type = [entry.get('reference'), "string"],
                )

            payload.add_answers(
                mardmo_property = "Formula",
                wikibase_property = "defining formula",
                datatype = "math",
            )

            payload.add_in_defining_formula()

            payload.add_multiple_relation(
                statement = {
                    'relation': "MF2MF",
                    'relatant': "MFRelatant"
                }
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "IntraClassRelation",
                    'relatant': "IntraClassElement"
                },
                optional_qualifier = ['assumes']
            )

    def _export_quantities(self, payload, quantities: dict):
        for entry in quantities.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            if entry.get("QorQK") == self.mathmoddb["Quantity"]:
                self._add_common_metadata(
                    payload = payload,
                    qclass = self.items["quantity"],
                    profile_type = "MaRDI quantity profile",
                )
                qtype = "quantity"

            elif entry.get("QorQK") == self.mathmoddb["QuantityKind"]:
                self._add_common_metadata(
                    payload = payload,
                    qclass = self.items["kind of quantity"],
                    profile_type = "MaRDI quantity profile",
                )
                qtype = "quantity kind"

            else:
                continue

            payload.add_aliases(
                aliases_dict = entry.get('Alias')
            )

            payload.add_data_properties(
                item_class = qtype
            )

            if (
                entry.get("reference")
                and qtype == "quantity kind"
            ):
                payload.add_answer(
                    verb = self.properties["QUDT quantity kind ID"],
                    object_and_type = [entry["reference"][0][1], "external-id"],
                )

            if (
                entry.get("reference")
                and qtype == "quantity"
            ):
                payload.add_answer(
                    verb = self.properties["QUDT constant ID"],
                    object_and_type = [entry["reference"][1][1], "external-id"],
                )

            payload.add_answers(
                mardmo_property = "Formula",
                wikibase_property = "defining formula",
                datatype = "math",
            )

            payload.add_in_defining_formula()

            if qtype == "quantity":
                payload.add_multiple_relation(
                    statement = {
                        'relation': "Q2Q",
                        'relatant': "QRelatant-Q"
                    }
                )

                payload.add_multiple_relation(
                    statement = {
                        'relation': "Q2QK",
                        'relatant': "QKRelatant-Q"
                    }
                )

            else:
                payload.add_multiple_relation(
                    statement = {
                        'relation': "QK2QK",
                        'relatant': "QKRelatant-QK"
                    }
                )

                payload.add_multiple_relation(
                    statement = {
                        'relation': "QK2Q",
                        'relatant': "QRelatant-QK"
                    }
                )

    def _export_journals(self, payload, publications: dict):
        for publication in publications.values():
            for entry in publication.get('journal', {}).values():
                if not entry.get("ID") or entry.get("ID") == 'no journal found':
                    continue

                payload.get_item_key(
                value = entry
                )

                payload.add_answer(
                    verb = self.properties["instance of"],
                    object_and_type = [self.items["scientific journal"], "wikibase-item"],
                )

                if entry.get('issn'):
                    payload.add_answer(
                        verb = self.properties["ISSN"],
                        object_and_type = [entry["issn"], "external-id"],
                    )

    def _export_authors(self, payload, publications: dict):
        for publication in publications.values():
            for entry in publication.get('author', {}).values():
                if not entry.get("ID") or entry.get("ID") == 'no author found':
                    continue

                payload.get_item_key(
                value = entry
                )

                payload.add_answer(
                    verb = self.properties["instance of"],
                    object_and_type = [self.items["human"], "wikibase-item"],
                )

                payload.add_answer(
                    verb = self.properties["MaRDI profile type"],
                    object_and_type = [self.items["Person"], "wikibase-item"],
                )

                if entry.get('orcid'):
                    payload.add_answer(
                        verb = self.properties["ORCID iD"],
                        object_and_type = [
                            entry['orcid'],
                            "external-id"
                        ],
                    )

                if entry.get('zbmath'):
                    payload.add_answer(
                        verb = self.properties["zbMATH author ID"],
                        object_and_type = [
                            entry['zbmath'],
                            "external-id"
                        ],
                    )

    def _export_publications(self, payload, publications: dict):
        for entry in publications.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            # Only add class, profile, and DOI for non-MaRDI items
            if "mardi" not in entry["ID"]:

                 # Set and add Publication Class
                if entry.get("entrytype") == "scholarly article":
                    pclass = self.items["scholarly article"]
                else:
                    pclass = self.items["publication"]

                payload.add_answer(
                    verb = self.properties["instance of"],
                    object_and_type = [pclass, "wikibase-item"],
                )

                # Add Publication Profile
                payload.add_answer(
                        verb = self.properties["MaRDI profile type"],
                        object_and_type = [
                            self.items["MaRDI publication profile"],
                            "wikibase-item"
                        ],
                    )

                # Add DOI
                if entry.get("reference", {}).get(0):
                    payload.add_answer(
                        verb = self.properties["DOI"],
                        object_and_type = [
                            entry["reference"][0][1].upper(),
                            "external-id"
                        ],
                    )

                # bibliographic data
                if entry.get("title"):
                    payload.add_answer(
                        verb = self.properties["title"],
                        object_and_type = [
                            {"text": entry["title"], "language": "en"},
                            "monolingualtext",
                        ],
                    )

                if entry.get("volume"):
                    payload.add_answer(
                        verb = self.properties["volume"],
                        object_and_type = [entry["volume"], "string"],
                    )

                if entry.get("issue"):
                    payload.add_answer(
                        verb = self.properties["issue"],
                        object_and_type = [entry["issue"], "string"],
                    )

                if entry.get("page"):
                    payload.add_answer(
                        verb = self.properties["page(s)"],
                        object_and_type = [entry["page"], "string"],
                    )

                if entry.get("date"):
                    payload.add_answer(
                        verb = self.properties["publication date"],
                        object_and_type = [
                            {
                                "time": f"+{entry['date']}",
                                "precision": date_precision(
                                    date_str = entry['date']
                                ),
                                "calendarmodel": (
                                    "http://www.wikidata.org/entity/Q1985727"
                                ),
                            },
                            "time",
                        ],
                    )

                # Add Language
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties["language of work or name"],
                        'relatant': "language"
                    }
                )
                # Add Journal
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties["published in"],
                        'relatant': "journal"
                    }
                )
                # Add Authors
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties["author"],
                        'relatant': "author"
                    },
                    alt_statement = {
                        "relation": self.properties["author name string"],
                        "relatant": "Name",
                    },
                )

            # Add relations to Entities of Mathematical Model
            payload.add_multiple_relation(
                statement = {
                    'relation': "P2E",
                    'relatant': "EntityRelatant"
                },
                reverse = True,
            )
