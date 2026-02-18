import json
import logging
import mimetypes

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from openai import OpenAI, OpenAIError
from rdmo.projects.imports import Import
from rdmo.projects.models import Value

logger = logging.getLogger(__name__)

BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/domain'


class MaRDMOImport(Import):

    def check(self):
        try:
            with open(self.file_name) as f:
                self.data = json.load(f)
                self.dmp = self.data.get('documentation-type')
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            return False

        return self.dmp == 'mardmo-model-documentation'

    def process(self):
        if self.current_project is None:
            raise ValidationError(_(
                'MaRDMO Model Documentations can only be imported into existing Projects. '
                'Please, create a project first!'
            ))

        self.catalog = self.current_project.catalog

        self._process_fields()
        self._process_problems()
        self._process_quantities()
        self._process_formulations()
        self._process_tasks()
        self._process_models()
        self._process_publications()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _uri(self, *parts):
        """Build a full RDMO attribute URI from path fragments."""
        return '/'.join([BASE_URI, *parts])

    def _attr(self, *parts):
        return self.get_attribute(self._uri(*parts))

    def _add(self, **kwargs):
        self.values.append(Value(**kwargs))

    def _add_text(self, uri_parts, set_index, text, set_prefix=None, collection_index=None):
        """Append a simple text Value."""
        kwargs = dict(attribute=self._attr(*uri_parts), set_index=set_index, text=text)
        if set_prefix is not None:
            kwargs['set_prefix'] = set_prefix
        if collection_index is not None:
            kwargs['collection_index'] = collection_index
        self._add(**kwargs)

    def _add_option(self, uri_parts, set_prefix, set_index, option):
        """Append a relation Value that carries an option."""
        self._add(
            attribute=self._attr(*uri_parts),
            set_prefix=set_prefix,
            set_index=int(set_index),
            option=self.get_option(option),
        )

    def _add_relatant(self, uri_parts, set_prefix, inner_set_index, collection_index, relatant):
        """Append a relatant Value with external_id and formatted text."""
        self._add(
            attribute=self._attr(*uri_parts),
            set_prefix=set_prefix,
            set_index=int(inner_set_index),
            collection_index=collection_index,
            external_id=relatant['ID'],
            text=f"{relatant['Name']} ({relatant['Description']})",
        )

    def _add_relation_and_relatants(self, data, relation_key, relatant_key,
                                    relation_uri, relatant_uri, set_index):
        """Append all option+relatant pairs for an intra/cross-class relation block."""
        for inner_set_index, option in data.get(relation_key, {}).items():
            self._add_option(relation_uri, set_index, inner_set_index, option)

        for inner_set_index, relatants in data.get(relatant_key, {}).items():
            for collection_index, relatant in enumerate(relatants.values()):
                self._add_relatant(relatant_uri, set_index, inner_set_index,
                                   collection_index, relatant)

    def _add_aliases_and_long_desc(self, data, domain, set_index):
        """Append Alias and descriptionLong collection values."""
        for col_idx, alias in data.get('Alias', {}).items():
            self._add_text([domain, 'alias'], 0, alias,
                           set_prefix=set_index, collection_index=int(col_idx))

        for col_idx, long_desc in data.get('descriptionLong', {}).items():
            self._add_text([domain, 'long-description'], 0, long_desc,
                           set_prefix=set_index, collection_index=int(col_idx))

    def _add_entity_id(self, data, domain, set_index):
        """Append the canonical ID Value (found or 'not found')."""
        if not data.get('ID'):
            return

        if data['ID'] != 'not found':
            self._add(
                attribute=self._attr(domain, 'id'),
                set_index=set_index,
                external_id=data['ID'],
                text=(
                    f"{data.get('Name', '')} ({data.get('Description', '')}) "
                    f"[{data['ID'].split(':')[0]}]"
                ),
            )
        else:
            self._add(
                attribute=self._attr(domain, 'id'),
                set_index=set_index,
                external_id='not found',
                text='not found',
            )

    def _add_entity_ref(self, uri_parts, set_prefix, col_idx, item):
        """Append a cross-entity relatant (e.g. field → problem reference)."""
        self._add(
            attribute=self._attr(*uri_parts),
            set_prefix=set_prefix,
            set_index=0,
            collection_index=int(col_idx),
            external_id=item['ID'],
            text=f"{item['Name']} ({item['Description']})",
        )

    def _add_formula_elements(self, data, domain, set_index):
        """Append Formula and element (symbol/quantity) Values."""
        for col_idx, formula in data.get('Formula', {}).items():
            self._add_text([domain, 'formula'], 0, formula,
                           set_prefix=f"{set_index}|0", collection_index=int(col_idx))

        for inner_set_index, sym_quan in data.get('element', {}).items():
            self._add(
                attribute=self._attr(domain, 'element', 'symbol'),
                set_prefix=f"{set_index}|0|0",
                set_index=int(inner_set_index),
                text=sym_quan['symbol'],
            )
            qty = sym_quan['quantity']
            self._add(
                attribute=self._attr(domain, 'element', 'quantity'),
                set_prefix=f"{set_index}|0|0",
                set_index=int(inner_set_index),
                external_id=qty['ID'],
                text=f"{qty['Name']} ({qty['Description']})",
            )

    # ------------------------------------------------------------------
    # Per-entity processors
    # ------------------------------------------------------------------

    def _process_fields(self):
        for set_index, data in enumerate(self.data.get('field', {}).values()):
            domain = 'field'
            self._add_text([domain], set_index, f"AD{set_index + 1}")
            self._add_text([domain, 'name'],        0, data.get('Name', ''),        set_prefix=set_index)
            self._add_text([domain, 'description'], 0, data.get('Description', ''), set_prefix=set_index)
            self._add_aliases_and_long_desc(data, domain, set_index)
            self._add_relation_and_relatants(
                data, 'IntraClassRelation', 'IntraClassElement',
                [domain, 'field-relation'], [domain, 'field-relatant'], set_index,
            )
            self._add_entity_id(data, domain, set_index)

    def _process_problems(self):
        for set_index, data in enumerate(self.data.get('problem', {}).values()):
            domain = 'problem'
            self._add_text([domain], set_index, f"RP{set_index + 1}")
            self._add_text([domain, 'name'],        0, data.get('Name', ''),        set_prefix=set_index)
            self._add_text([domain, 'description'], 0, data.get('Description', ''), set_prefix=set_index)
            self._add_aliases_and_long_desc(data, domain, set_index)

            for col_idx, field in data.get('RFRelatant', {}).items():
                self._add_entity_ref([domain, 'field-relatant'], set_index, col_idx, field)

            self._add_relation_and_relatants(
                data, 'IntraClassRelation', 'IntraClassElement',
                [domain, 'problem-relation'], [domain, 'problem-relatant'], set_index,
            )
            self._add_entity_id(data, domain, set_index)

    def _process_quantities(self):
        for set_index, data in enumerate(self.data.get('quantity', {}).values()):
            domain = 'quantity'
            self._add_text([domain], set_index, f"QQK{set_index + 1}")
            self._add_text([domain, 'name'],        0, data.get('Name', ''),        set_prefix=set_index)
            self._add_text([domain, 'description'], 0, data.get('Description', ''), set_prefix=set_index)
            self._add_aliases_and_long_desc(data, domain, set_index)

            for col_idx, ref in data.get('reference', {}).items():
                self._add(
                    attribute=self._attr(domain, 'reference'),
                    set_prefix=set_index, set_index=0,
                    collection_index=int(col_idx),
                    text=ref[1], option=self.get_option(ref[0]),
                )

            for col_idx, prop in data.get('Properties', {}).items():
                self._add(
                    attribute=self._attr(domain, 'properties'),
                    set_prefix=set_index, set_index=0,
                    collection_index=int(col_idx),
                    option=self.get_option(prop),
                )

            self._add(
                attribute=self._attr(domain, 'is-quantity-or-quantity-kind'),
                set_index=set_index,
                option=self.get_option(data.get('QorQK')),
            )

            self._add_formula_elements(data, domain, set_index)

            for relation_key, relatant_key, rel_uri, relant_uri in [
                ('Q2Q',   'QRelatant-Q',  [domain, 'quantity-to-quantity', 'relation'],      [domain, 'quantity-to-quantity', 'relatant']),
                ('QK2QK', 'QKRelatant-QK',[domain, 'quantity-kind-to-quantity-kind', 'relation'], [domain, 'quantity-kind-to-quantity-kind', 'relatant']),
                ('Q2QK',  'QRelatant-QK', [domain, 'quantity-to-quantity-kind', 'relation'],  [domain, 'quantity-to-quantity-kind', 'relatant']),
                ('QK2Q',  'QKRelatant-Q', [domain, 'quantity-kind-to-quantity', 'relation'],  [domain, 'quantity-kind-to-quantity', 'relatant']),
            ]:
                self._add_relation_and_relatants(data, relation_key, relatant_key,
                                                 rel_uri, relant_uri, set_index)

            self._add_entity_id(data, domain, set_index)

    def _process_formulations(self):
        for set_index, data in enumerate(self.data.get('formulation', {}).values()):
            domain = 'formulation'
            self._add_text([domain], set_index, f"ME{set_index + 1}")
            self._add_text([domain, 'name'],        0, data.get('Name', ''),        set_prefix=set_index)
            self._add_text([domain, 'description'], 0, data.get('Description', ''), set_prefix=set_index)
            self._add_aliases_and_long_desc(data, domain, set_index)

            for col_idx, prop in enumerate(data.get('Properties', {}).values()):
                self._add(
                    attribute=self._attr(domain, 'properties'),
                    set_prefix=set_index, set_index=0,
                    collection_index=col_idx,
                    option=self.get_option(prop),
                )

            self._add_formula_elements(data, domain, set_index)

            self._add_relation_and_relatants(
                data, 'MF2MF', 'MFRelatant',
                [domain, 'formulation-relation-1'], [domain, 'formulation-relatant-1'], set_index,
            )
            self._add_relation_and_relatants(
                data, 'IntraClassRelation', 'IntraClassElement',
                [domain, 'formulation-relation-2'], [domain, 'formulation-relatant-2'], set_index,
            )

            for inner_set_index, relatants in data.get('assumption', {}).items():
                for col_idx, relatant in enumerate(relatants.values()):
                    self._add_relatant([domain, 'formulation-assumption'],
                                       set_index, inner_set_index, col_idx, relatant)

            self._add_entity_id(data, domain, set_index)

    def _process_tasks(self):
        for set_index, data in enumerate(self.data.get('task', {}).values()):
            domain = 'task'
            self._add_text([domain], set_index, f"CT{set_index + 1}")
            self._add_text([domain, 'name'],        0, data.get('Name', ''),        set_prefix=set_index)
            self._add_text([domain, 'description'], 0, data.get('Description', ''), set_prefix=set_index)
            self._add_aliases_and_long_desc(data, domain, set_index)

            for col_idx, prop in data.get('Properties', {}).items():
                self._add(
                    attribute=self._attr(domain, 'properties'),
                    set_prefix=set_index, set_index=0,
                    collection_index=int(col_idx),
                    option=self.get_option(prop),
                )

            for relation_key, relatant_key, rel_uri, relant_uri in [
                ('T2MF', 'MFRelatant',        [domain, 'formulation-relation'], [domain, 'formulation-relatant']),
                ('T2Q',  'QRelatant',          [domain, 'quantity-relation'],    [domain, 'quantity-relatant']),
                ('IntraClassRelation', 'IntraClassElement',
                                               [domain, 'task-relation'],        [domain, 'task-relatant']),
            ]:
                self._add_relation_and_relatants(data, relation_key, relatant_key,
                                                 rel_uri, relant_uri, set_index)

            for inner_set_index, relatants in data.get('assumption', {}).items():
                for col_idx, relatant in enumerate(relatants.values()):
                    self._add_relatant([domain, 'task-assumption'],
                                       set_index, inner_set_index, col_idx, relatant)

            for inner_set_index, order_number in data.get('task_number', {}).items():
                self._add_option([domain, 'task-order-number'], set_index, inner_set_index, order_number)

            self._add_entity_id(data, domain, set_index)

    def _process_models(self):
        for set_index, data in enumerate(self.data.get('model', {}).values()):
            domain = 'model'
            self._add_text([domain], set_index, f"MM{set_index + 1}")
            self._add_text([domain, 'name'],        0, data.get('Name', ''),        set_prefix=set_index)
            self._add_text([domain, 'description'], 0, data.get('Description', ''), set_prefix=set_index)
            self._add_aliases_and_long_desc(data, domain, set_index)

            for col_idx, prop in data.get('Properties', {}).items():
                self._add(
                    attribute=self._attr(domain, 'properties'),
                    set_prefix=set_index, set_index=0,
                    collection_index=int(col_idx),
                    option=self.get_option(prop),
                )

            for col_idx, problem in data.get('RPRelatant', {}).items():
                self._add_entity_ref([domain, 'problem-relatant'], set_index, col_idx, problem)

            for col_idx, task in data.get('TRelatant', {}).items():
                self._add_entity_ref([domain, 'task-relatant'], set_index, col_idx, task)

            for relation_key, relatant_key, rel_uri, relant_uri in [
                ('MM2MF',           'MFRelatant',        [domain, 'formulation-relation'], [domain, 'formulation-relatant']),
                ('IntraClassRelation', 'IntraClassElement', [domain, 'model-relation'],    [domain, 'model-relatant']),
            ]:
                self._add_relation_and_relatants(data, relation_key, relatant_key,
                                                 rel_uri, relant_uri, set_index)

            for inner_set_index, relatants in data.get('assumption', {}).items():
                for col_idx, relatant in enumerate(relatants.values()):
                    self._add_relatant([domain, 'model-assumption'],
                                       set_index, inner_set_index, col_idx, relatant)

            for inner_set_index, order_number in data.get('formulation_number', {}).items():
                self._add(
                    attribute=self._attr(domain, 'formulation-order-number'),
                    set_prefix=set_index,
                    set_index=int(inner_set_index),
                    text=order_number,
                )

            self._add_entity_id(data, domain, set_index)

    def _process_publications(self):
        for set_index, data in enumerate(self.data.get('publication', {}).values()):
            domain = 'publication'
            self._add_text([domain], set_index, f"P{set_index + 1}")
            self._add_text([domain, 'name'],        set_index, data.get('Name', ''))
            self._add_text([domain, 'description'], set_index, data.get('Description', ''))

            for col_idx, ref in data.get('reference', {}).items():
                self._add(
                    attribute=self._attr(domain, 'reference'),
                    set_index=set_index,
                    collection_index=int(col_idx),
                    text=ref[1], option=self.get_option(ref[0]),
                )

            for field_name in ('entry-type', 'date', 'volume', 'issue', 'page'):
                self._add_text([domain, field_name], set_index,
                               data.get(field_name.replace('-', ''), data.get(field_name, '')))

            # Collections: language, journal, author each share the same ID/Name/Description pattern
            for col_idx, lang in data.get('language', {}).items():
                for sub_field in ('ID', 'Name', 'Description'):
                    self._add_text([domain, 'language', sub_field.lower()],
                                   set_index, lang.get(sub_field, ''),
                                   collection_index=int(col_idx))

            for col_idx, journal in data.get('journal', {}).items():
                for sub_field in ('ID', 'Name', 'Description'):
                    self._add_text([domain, 'journal', sub_field.lower()],
                                   set_index, journal.get(sub_field, ''),
                                   collection_index=int(col_idx))
                self._add_text([domain, 'journal', 'issn'], set_index,
                               journal.get('issn', ''), collection_index=int(col_idx))

            for col_idx, author in data.get('author', {}).items():
                for sub_field in ('ID', 'Name', 'Description'):
                    self._add_text([domain, 'author', sub_field.lower()],
                                   set_index, author.get(sub_field, ''),
                                   collection_index=int(col_idx))
                for sub_field in ('orcid', 'zbmath', 'wikidata'):
                    self._add_text([domain, 'author', sub_field], set_index,
                                   author.get(sub_field, ''), collection_index=int(col_idx))

            self._add_relation_and_relatants(
                data, 'P2E', 'EntityRelatant',
                [domain, 'entity-relation'], [domain, 'entity-relatant'], set_index,
            )
            self._add_entity_id(data, domain, set_index)


_OLLAMA_SYSTEM_PROMPT = """
Extract model documentation and return ONLY valid JSON. Your response must start with { and end with }.

REQUIRED STRUCTURE:
{
  "documentation-type": "mardmo-model-documentation",
  "model": {
    "0": {
      "ID": "not found",
      "Name": "<name>",
      "Alias": {
        "0": "<Alias>", ...
      },
      "Description": "<description>",
      "descriptionLong": {
        "0": "<long_description>", ...
      },
      "Properties: {
        "0": "<property>", ...
      }
    }
  }
}

FIELD RULES:
- Name: 5-10 words, lowercase except proper nouns, no abbreviations
- Alias: one or more aliasses including abbreviations
- Description: 4-12 words, no complete sentence, lowercase except proper nouns
- descriptionLong: Dictionary with key "0" containing 30-40 words as ONE string
  * Use additional keys ("1", "2") ONLY if source has distinct separate descriptions
  * Each value is a complete paragraph, NOT individual sentences
- property:
  * if stochstic <property> = "https://rdmo.mardi4nfdi.de/terms/options/mathmoddb/is-stochastic"
  * if time continuous <property> = "https://rdmo.mardi4nfdi.de/terms/options/mathmoddb/is-time-continuous",
- ID: Always exactly "not found"

CRITICAL OUTPUT RULES:
1. Output ONLY the JSON object
2. NO markdown (no ```, no ```json)
3. NO explanations before or after
4. NO line breaks inside string values - use spaces instead
5. NO quotes inside strings
6. Ensure ALL braces { } and brackets [ ] are properly closed
7. End with a complete, valid JSON object

Your response must be valid JSON that passes JSON.parse() / json.loads().

""".strip()

class MaRDMOPDFImport(MaRDMOImport):
    """Import MaRDMO model documentation from a PDF file.

    The PDF text is extracted with pypdf, sent to a local Ollama instance
    configured in Django settings, and the returned JSON is processed
    identically to a regular MaRDMO JSON import.

    Required Django settings
    ------------------------
    MARDMO_OLLAMA_URL   : str  – base URL, e.g. "https://ollama.example.org"
    MARDMO_OLLAMA_MODEL : str  – model tag,  e.g. "llama3:8b"
    """

    # ------------------------------------------------------------------ #
    # Public interface                                                     #
    # ------------------------------------------------------------------ #

    def check(self):
        """Return True only for readable, text-bearing PDF files."""
        try:
            reader = PdfReader(self.file_name)
            # Require at least one page with extractable text
            if not reader.pages or not any(
                page.extract_text() for page in reader.pages
            ):
                return False
        except (PdfReadError, Exception):
            # PdfReader raises PdfReadError for invalid PDFs,
            # but also generic exceptions for non-PDF files
            return False

        return True

    def process(self):
        if self.current_project is None:
            raise ValidationError(_(
                'MaRDMO PDF Imports can only be imported into existing Projects. '
                'Please create a project first!'
            ))

        self.catalog = self.current_project.catalog

        pdf_text = self._extract_text()
        raw_json = self._query_ollama(pdf_text)
        print(raw_json)
        try:
            self.data = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise ValidationError(
                _('The LLM response could not be parsed as JSON: %(err)s'),
                params={'err': str(exc)},
            ) from exc
        print(self.data)
        if self.data.get('documentation-type') != 'mardmo-model-documentation':
            raise ValidationError(_(
                'The LLM did not return a valid MaRDMO model documentation object.'
            ))

        # Delegate to the parent processors – identical to a JSON import
        self._process_fields()
        self._process_problems()
        self._process_quantities()
        self._process_formulations()
        self._process_tasks()
        self._process_models()
        self._process_publications()

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    def _extract_text(self):
        """Return the concatenated text content of all PDF pages."""
        reader = PdfReader(self.file_name)
        pages_text = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ''
            if text.strip():
                pages_text.append(f"--- Page {i} ---\n{text}")

        if not pages_text:
            raise ValidationError(_('No extractable text found in the PDF.'))

        return '\n\n'.join(pages_text)

    def _query_ollama(self, pdf_text):
        """Send pdf_text to the Ollama instance and return the reply string.

        Uses the openai SDK pointed at the institute's Ollama base URL.
        """
        base_url = getattr(settings, 'MARDMO_OLLAMA_URL', '').rstrip('/')
        model    = getattr(settings, 'MARDMO_OLLAMA_MODEL', '')
        api_key  = getattr(settings, 'MARDMO_OLLAMA_API_KEY', '')

        if not base_url or not model:
            raise ValidationError(_(
                'MARDMO_OLLAMA_URL and MARDMO_OLLAMA_MODEL must be set in Django settings.'
            ))

        client = OpenAI(base_url=base_url, api_key=api_key)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': _OLLAMA_SYSTEM_PROMPT},
                    {'role': 'user',   'content': pdf_text},
                ],
            )
        except OpenAIError as exc:
            logger.error('Ollama request failed: %s', exc)
            raise ValidationError(
                _('The request to the Ollama instance failed: %(err)s'),
                params={'err': str(exc)},
            ) from exc

        return response.choices[0].message.content