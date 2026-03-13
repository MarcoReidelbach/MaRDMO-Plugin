'''Worker Module for Algorithm Preview and Export'''

import logging
import time

from .constants import get_relations, preview_relations

from ..getters import get_items, get_mathalgodb, get_properties, get_url
from ..helpers import entity_relations, unique_items
from ..payload import GeneratePayload
from ..queries import query_sparql

from ..publication.worker import PublicationExport

class PrepareAlgorithm(PublicationExport):
    '''Class preparing Model Answers for Preview and Export'''
    def __init__(self):
        self.mathalgodb = get_mathalgodb()
        self.items = get_items()
        self.properties = get_properties()

    def preview(self, answers):
        '''Function to establish relations between Algorithm Documentation Data'''

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
                    'formulation': False,
                    'task': False
                },
                assumption = False,
                mapping = self.mathalgodb
            )

        return answers

    def export(self, data, url):
        """Function to create Payload for Model Export."""

        items, dependency = unique_items(data)

        payload = GeneratePayload(
            dependency = dependency,
            user_items = items,
            url = url,
            wikibase = {
                'items': get_items(),
                'properties': get_properties(),
                'relations': get_relations()
            }
        )

        # Add / Retrieve Components of Model Item
        payload.process_items()

        # Delegate to helper functions
        self._export_algorithms(
            payload = payload,
            algorithms = data.get("algorithm", {}),
        )
        self._export_problems(
            payload = payload,
            problems = data.get("problem", {})
        )
        self._export_softwares(
            payload = payload,
            softwares = data.get("software", {})
        )
        self._export_benchmarks(
            payload = payload,
            benchmarks = data.get("benchmark", {})
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
            publications = data.get("publication", {}),
            relations = [('P2A', 'ARelatant'), ('P2BS', 'BSRelatant')]
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
            object_and_type = [self.items["MathAlgoDB"], "wikibase-item"],
        )

        if qclass != self.items["benchmark"]:
            payload.add_answer(
                verb = self.properties["MaRDI profile type"],
                object_and_type = [self.items[profile_type], "wikibase-item"],
            )

    # ---------------------------
    # Entity export helpers
    # ---------------------------
    def _export_algorithms(self, payload, algorithms: dict):
        for entry in algorithms.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["algorithm"],
                profile_type = "MaRDI algorithm profile",
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["solved by"],
                    'relatant': "PRelatant"
                },
                reverse = True
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["implemented by"],
                    'relatant': "SRelatant"
                }
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
                qclass = self.items["algorithmic task"],
                profile_type = "MaRDI task profile",
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["manifestation of"],
                    'relatant': "BRelatant"
                },
                reverse = True
            )

            payload.add_multiple_relation(
                statement = {
                    'relation': "IntraClassRelation",
                    'relatant': "IntraClassElement"
                }
            )

    def _export_softwares(self, payload, softwares: dict):
        for entry in softwares.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["software"],
                profile_type = "MaRDI software profile",
            )

            payload.add_single_relation(
                statement = {
                    'relation': self.properties["tested by"],
                    'relatant': "BRelatant"
                },
                reverse = True
            )

            if entry.get("reference"):
                if entry['reference'].get(0):
                    payload.add_answer(
                        verb = self.properties["DOI"],
                        object_and_type = [entry["reference"][0][1], "external-id"],
                    )
                if entry['reference'].get(1):
                    payload.add_answer(
                        verb = self.properties["swMath work ID"],
                        object_and_type = [entry["reference"][1][1], "external-id"],
                    )
                if entry['reference'].get(2):
                    payload.add_answer(
                        verb = self.properties["described at URL"],
                        object_and_type = [entry["reference"][2][1], "URL"],
                    )
                if entry['reference'].get(3):
                    payload.add_answer(
                        verb = self.properties["source code repository URL"],
                        object_and_type = [entry["reference"][3][1], "URL"],
                    )
                
    def _export_benchmarks(self, payload, benchmarks: dict):
        for entry in benchmarks.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            self._add_common_metadata(
                payload = payload,
                qclass = self.items["benchmark"],
                profile_type = "MaRDI benchmark profile",
            )

            if entry.get("reference"):
                if entry['reference'].get(0):
                    payload.add_answer(
                        verb = self.properties["DOI"],
                        object_and_type = [entry["reference"][0][1], "external-id"],
                    )
                if entry['reference'].get(1):
                    payload.add_answer(
                        verb = self.properties["MORwiki ID"],
                        object_and_type = [entry["reference"][1][1], "external-id"],
                    )
                if entry['reference'].get(2):
                    payload.add_answer(
                        verb = self.properties["described at URL"],
                        object_and_type = [entry["reference"][2][1], "URL"],
                    )
                if entry['reference'].get(3):
                    payload.add_answer(
                        verb = self.properties["source code repository URL"],
                        object_and_type = [entry["reference"][3][1], "URL"],
                    )
