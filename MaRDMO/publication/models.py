from dataclasses import dataclass, field
from typing import Optional, ClassVar

from ..getters import get_items, get_options

@dataclass
class Relatant:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    bsclass: Optional[str]
    
    @classmethod
    def from_query(cls, raw: str) -> 'Relatant':

        raw_split = raw.split(" | ")

        if len(raw_split) == 3:
            bsclass = None
        else:
            bsclass = raw_split[3]

        return cls(
            id = raw_split[0],
            label = raw_split[1],
            description = raw_split[2],
            bsclass = bsclass
        )
    
    @classmethod
    def from_language_dict(cls, raw: dict) -> 'Relatant':

        return cls(
            id = raw["ID"],
            label = raw["Name"],
            description = raw["Description"],
            bsclass = None
        )
    
@dataclass
class Author:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    orcid_id: Optional[str]
    zbmath_id: Optional[str]
    wikidata_id: Optional[str]

    @classmethod
    def from_query(cls, raw: str) -> 'Author':
        parts = raw.split(" <|> ")
        return cls(
            id = parts[0],
            label = parts[1],
            description = parts[2],
            orcid_id = parts[3],
            zbmath_id = parts[4],
            wikidata_id = parts[5]
        )
    
    @classmethod
    def from_crossref(cls, raw: str) -> 'Author':

        # Get Label
        label = None
        if raw.get('given') and raw.get('family'):
            label = f"{raw['given']} {raw['family']}"

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no author found'

        # Get ORCID ID
        orcid_id = None
        if raw.get('ORCID'):
            orcid_id = raw.get('ORCID').split('/')[-1]

        # Get ZBMath ID
        zbmath_id = None

        # Get Wikidata ID
        wikidata_id = None

        # Get Label
        label = None
        if raw.get('given') and raw.get('family'):
            label = f"{raw['given']} {raw['family']}"

        # Get Description
        description = None
        if label:
            if orcid_id:
                description = f'scientist (ORCID iD {orcid_id})'
            else:
                description = 'scientist'


        return cls(
            id = id,
            label = label,
            description = description,
            orcid_id = orcid_id,
            zbmath_id = zbmath_id,
            wikidata_id = wikidata_id
        )
    
    @classmethod
    def from_datacite(cls, raw: str) -> 'Author':

        # Get Label
        label = None
        if raw.get('givenName') and raw.get('familyName'):
            label = f"{raw['givenName']} {raw['familyName']}"

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no author found'

        # Get ORCID ID
        orcid_id = None
        for identifier in raw.get('nameIdentifiers', []):
            if identifier.get('nameIdentifierScheme') == 'ORCID':
                name_identifier = identifier.get('nameIdentifier', '')
                orcid_id = name_identifier.split('/')[-1]
                break

        # Get ZBMath ID
        zbmath_id = None

        # Get Wikidata ID
        wikidata_id = None

        # Get Description
        description = None
        if label:
            if orcid_id:
                description = f'scientist (ORCID iD {orcid_id})'
            else:
                description = 'scientist'

        return cls(
            id = id,
            label = label,
            description = description,
            orcid_id = orcid_id,
            zbmath_id = zbmath_id,
            wikidata_id = wikidata_id
        )
    
    @classmethod
    def from_doi(cls, raw: str) -> 'Author':

        # Get Label
        label = None
        if raw.get('given') and raw.get('family'):
            label = f"{raw['given']} {raw['family']}"

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no author found'

        # Get ORCID ID
        orcid_id = None
        if raw.get('ORCID'):
            orcid_id = raw.get('ORCID').split('/')[-1]

        # Get ZBMath ID
        zbmath_id = None

        # Get Wikidata ID
        wikidata_id = None

        # Get Description
        description = None
        if label:
            if orcid_id:
                description = f'scientist (ORCID iD {orcid_id})'
            else:
                description = 'scientist'

        return cls(
            id = id,
            label = label,
            description = description,
            orcid_id = orcid_id,
            zbmath_id = zbmath_id,
            wikidata_id = wikidata_id
        )
    
    @classmethod
    def from_zbmath(cls, raw: str) -> 'Author':

        # Get Label
        label = None
        if raw.get('name'):
            label = " ".join(reversed([s for s in raw['name'].split(", ")]))

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no author found'

        # Get ORCID ID
        orcid_id = None

        # Get zbMath ID
        zbmath_id = None
        if raw.get('codes'):
            zbmath_id = raw['codes'][0]

        # Get Wikidata ID
        wikidata_id = None

        # Get Description
        description = None
        if label:
            if zbmath_id:
                description = f'scientist (zbMath ID {zbmath_id})'
            else:
                description = 'scientist'

        return cls(
            id = id,
            label = label,
            description = description,
            orcid_id = orcid_id,
            zbmath_id = zbmath_id,
            wikidata_id = wikidata_id
        )
    
    @classmethod
    def from_orcid(cls, raw: str) -> 'Author':

        # Get Label
        label = None
        if raw.get('name', {}).get('given-names', {}).get('value') and raw.get('name', {}).get('family-name', '').get('value'):
            label = f"{raw['name']['given-names']['value']} {raw['name']['family-name']['value']}"

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no author found'

        # Get ORCID ID
        orcid_id = raw.get('name', {}).get('path')

        # Get ZBMath ID
        zbmath_id = None

        # Get Wikidata ID
        wikidata_id = None

        # Get Description
        description = None
        if label:
            if orcid_id:
                description = f'scientist (ORCID iD {orcid_id})'
            else:
                description = 'scientist'

        return cls(
            id = id,
            label = label,
            description = description,
            orcid_id = orcid_id,
            zbmath_id = zbmath_id,
            wikidata_id = wikidata_id
        )

@dataclass
class Journal:
    id: str
    issn: str
    label: str
    description: str

    @classmethod
    def from_query(cls, raw: str) -> 'Journal':
        id, label, description = raw.split(" <|> ")
        return cls(
            id = id,
            issn =None,
            label = label,
            description = description
        )
    
    @classmethod
    def from_crossref(cls, ids: list, item: list) -> 'Journal':

        # Get Label
        label = None
        if item:
            label = item[0]

        # Get ISSN
        issn = None
        if ids:
            issn = ids[0]

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no journal found'
        
        # Get Description
        description = None
        if label:
            if issn:
                description = f'scientific journal (ISSN {issn})'
            else:
                description = 'scientific journal'

        return cls(
            id = id,
            issn = issn,
            label = label,
            description = description,
        )
    
    @classmethod
    def from_datacite(cls, ids: list, item: list) -> 'Journal':

        # Get Label
        label = None
        if item:
            label = (item[0].get('titles') or [{}])[0].get('title')

        # Get ISSN
        issn = None
        if ids:
            if ids[0].get('relatedIdentifierType') == 'ISSN':
                issn = ids[0].get('relatedIdentifier') 

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no journal found'
        
        # Get Description
        description = None
        if label:
            if issn:
                description = f'scientific journal (ISSN {issn})'
            else:
                description = 'scientific journal'

        return cls(
            id = id,
            issn = issn,
            label = label,
            description = description,
        )
    
    @classmethod
    def from_doi(cls, ids: list, item: str) -> 'Journal':

        # Get Label
        label = None
        if item:
            label = item

        # Get ISSN
        issn = None
        if ids:
            issn = ids[0]

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no journal found'

        # Get Description
        description = None
        if label:
            if issn:
                description = f'scientific journal (ISSN {issn})'
            else:
                description = 'scientific journal'

        return cls(
            id = id,
            issn = issn,
            label = label,
            description = description,
        )
    
    @classmethod
    def from_zbmath(cls, raw: dict) -> 'Journal':

        series = (raw.get('series') or [{}])[0]

        # Get Label
        label = None
        if series.get('title'):
            label = series['title']

        # Get ISSN
        issn = None
        if (series.get('issn') or [{}])[0].get('number'):
            issn = series['issn'][0]['number']

        # Get MaRDI Portal ID
        id = None
        if label:
            id = 'no journal found'

        # Get Description
        description = None
        if label:
            if issn:
                description = f'scientific journal (ISSN {issn})'
            else:
                description = 'scientific journal'

        return cls(
            id = id,
            issn = issn,
            label = label,
            description = description,
        )


@dataclass
class Publication:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    entrytype: Optional[str]
    title: Optional[str]
    date: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    page: Optional[str]
    reference: Optional[str]
    journal: Optional[list[Journal]] = field(default_factory=list)
    authors: Optional[list[Author]] = field(default_factory=list)
    language: Optional[list[Relatant]] = field(default_factory=list)
    applies: Optional[list[Relatant]] = field(default_factory=list)
    analyzes: Optional[list[Relatant]] = field(default_factory=list)
    documents: Optional[list[Relatant]] = field(default_factory=list)
    invents: Optional[list[Relatant]] = field(default_factory=list)
    studies: Optional[list[Relatant]] = field(default_factory=list)
    surveys: Optional[list[Relatant]] = field(default_factory=list)
    uses: Optional[list[Relatant]] = field(default_factory=list)

    options: ClassVar[Optional[dict]] = None

    @classmethod
    def get_options(cls) -> dict:
        if cls.options is None:
            cls.options = get_options()
        return cls.options

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Publication':

        data = raw_data[0]

        options = cls.get_options()
        ITEMS = get_items()

        return cls(
            id = data.get('id', {}).get('value'),
            label = data.get('label', {}).get('value'),
            description = data.get('description', {}).get('value'),
            entrytype = data.get('entrytypelabel', {}).get('value'),
            language = [Relatant.from_language_dict({"ID": f"mardi:{ITEMS['english']}", "Name": "English", "Description": "West Germanic language"})] if data.get('langaugelabel', {}).get('value', '').lower() in {"en", "eng", "english"} else [],
            title = data.get('title', {}).get('value'),
            date = data.get('date', {}).get('value')[:10] if 'date' in data else None,
            volume = data.get('volume', {}).get('value'),
            issue = data.get('issue', {}).get('value'),
            page = data.get('page', {}).get('value'),
            reference = {idx: [options['DOI'], data[prop]['value']] for idx, prop in enumerate(['doi']) if data.get(prop, {}).get('value')},
            journal = [Journal.from_query(data.get('journalInfo', {}).get('value'))] if 'journalInfo' in data else [],
            authors = [
                Author.from_query(author)
                for author in data.get('authorInfos', {}).get('value', '').split(" | ")
                if author
            ] if 'authorInfos' in data else [],
            applies = [Relatant.from_query(publication) for publication in data.get('applies', {}).get('value', '').split(" / ") if publication] if 'applies' in data else [],
            analyzes = [Relatant.from_query(publication) for publication in data.get('analyzes', {}).get('value', '').split(" / ") if publication] if 'analyzes' in data else [],
            documents = [Relatant.from_query(publication) for publication in data.get('documents', {}).get('value', '').split(" / ") if publication] if 'documents' in data else [],
            invents = [Relatant.from_query(publication) for publication in data.get('invents', {}).get('value', '').split(" / ") if publication] if 'invents' in data else [],
            studies = [Relatant.from_query(publication) for publication in data.get('studies', {}).get('value', '').split(" / ") if publication] if 'studies' in data else [],
            surveys = [Relatant.from_query(publication) for publication in data.get('surveys', {}).get('value', '').split(" / ") if publication] if 'surveys' in data else [],
            uses = [Relatant.from_query(publication) for publication in data.get('uses', {}).get('value', '').split(" / ") if publication] if 'uses' in data else [],
        )
    
    @classmethod
    def from_crossref(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json().get('message', {})
        
        options = cls.get_options()
        ITEMS = get_items()

        # Get Publication MaRDI Portal ID
        id = None

        # Get Publication DOI
        doi = data.get('DOI')

        # Get Publication Label
        label = None

        # Get Publication Description
        if doi:
            description = f'scientific article (doi {doi})'
        else:
            description = f'scientific article'

        # Get Publication Entrytype
        if data.get('type') == 'journal-article':
            entrytype = 'scholarly article'
        else:
            entrytype = 'publication'

        # Get Publication Language
        language_code = (data.get('language') or '').lower()

        if language_code in {"en", "eng", "english"}:
            language = [
                Relatant.from_language_dict({
                    "ID": f"mardi:{ITEMS['english']}",
                    "Name": "English",
                    "Description": "West Germanic language",
                })
            ]
        else:
            language = []

        # Get Publication Title
        title = data.get('title', [''])[0]

        # Get Publication Date
        published = data.get('published', {}).get('date-parts', [])

        date_parts = published[0] if published else []

        if len(date_parts) == 1:
            date = f"{date_parts[0]:04d}-00-00T00:00:00Z"
        elif len(date_parts) == 2:
            date = f"{date_parts[0]:04d}-{date_parts[1]:02d}-00T00:00:00Z"
        elif len(date_parts) >= 3:
            date = f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}T00:00:00Z"
        else:
            date = None

        # Get Publication Volume
        volume = data.get('volume')

        # Get Publication Issue
        issue = data.get('issue')

        # Get Publication Page
        page = data.get('page')

        # Get Publication Reference
        reference = {}
        if doi:
            reference = {0: [options['DOI'], doi]}

        # Get Publication Journal
        journal = []
        if 'ISSN' in data or 'container-title' in data:
            journal = [
                Journal.from_crossref(
                    data.get('ISSN', []),
                    data.get('container-title', [])
                )
            ]

        # Get Publication Authors
        authors = []
        if 'author' in data:
            authors = [
                Author.from_crossref(author)
                for author in data.get('author', [])
                if author
            ]
        
        return cls(
            id = id,
            label = label,
            description = description,
            entrytype = entrytype,
            language = language,
            title = title,
            date = date,
            volume = volume,
            issue = issue,
            page = page,
            reference = reference,
            journal = journal,
            authors = authors
        )
    
    @classmethod
    def from_datacite(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json().get('data', {}).get('attributes', {})
        
        options = cls.get_options()
        ITEMS = get_items()

        # Get Publication MaRDI Portal ID
        id = None

        # Get Publication DOI
        doi = data.get('DOI')

        # Get Publication Label
        label = None

        # Get Publication Description
        if doi:
            description = f'scientific article (doi {doi})'
        else:
            description = f'scientific article'

        # Get Publication Entrytype
        if data.get('types', {}).get('bibtex') == 'article':
            entrytype = 'scholarly article'
        else:
            entrytype = 'publication'

        # Get Publication Language
        language_code = (data.get('language') or '').lower()

        if language_code in {"en", "eng", "english"}:
            language = [
                Relatant.from_language_dict({
                    "ID": f"mardi:{ITEMS['english']}",
                    "Name": "English",
                    "Description": "West Germanic language",
                })
            ]
        else:
            language = []

        # Get Publication Title
        title = data.get('titles', [''])[0].get('title')

        # Get Publication Date
        date = None
        for date_part in data.get('dates', []):
            if date_part.get('dateType') == 'Issued':
                raw_date = date_part.get('date')
                if raw_date:
                    parts = raw_date.split('-')
                    if len(parts) == 1:
                        date = f"{int(parts[0]):04d}-00-00T00:00:00Z"
                    elif len(parts) == 2:
                        date = f"{int(parts[0]):04d}-{int(parts[1]):02d}-00T00:00:00Z"
                    elif len(parts) >= 3:
                        date = f"{int(parts[0]):04d}-{int(parts[1]):02d}-{int(parts[2]):02d}T00:00:00Z"
                break

        # Get Publication Volume
        volume = (data.get('relatedItems') or [{}])[0].get('volume')

        # Get Publication Issue
        issue = (data.get('relatedItems') or [{}])[0].get('issue')

        # Get Publication Page
        page = None
        if data.get('relatedItems'):
            page = f"{data['relatedItems'][0].get('firstPage', '')}-{data['relatedItems'][0].get('lastPage', '')}"

        # Get Publication Reference
        reference = {}
        if doi:
            reference = {0: [options['DOI'], doi]}

        # Get Publication Journal
        journal = []
        if 'relatedIdentifiers' in data or 'relatedItems' in data:
            journal = [
                Journal.from_datacite(
                    data.get('relatedIdentifiers', [{}]),
                    data.get('relatedItems') or [{}],
                )
            ]

        # Get Publication Authors
        authors = []
        if 'creators' in data:
            authors = [
                Author.from_datacite(author)
                for author in data.get('creators', [])
                if author
            ]

        return cls(
            id = id,
            label = label,
            description = description,
            entrytype = entrytype,
            language = language,
            title = title,
            date = date,
            volume = volume,
            issue = issue,
            page = page,
            reference = reference,
            journal = journal,
            authors = authors
        )
    
    @classmethod
    def from_doi(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json()

        options = cls.get_options()
        ITEMS = get_items()

        # Get Publication MaRDI Portal ID
        id = None

        # Get Publication DOI
        doi = data.get('DOI')

        # Get Publication Label
        label = None

        # Get Publication Description
        if doi:
            description = f'scientific article (doi {doi})'
        else:
            description = f'scientific article'

        # Get Publication Entrytype
        if data.get('type') == 'journal-article' or data.get('type') == 'article-journal':
            entrytype = 'scholarly article'
        else:
            entrytype = 'publication'

        # Get Publication Language
        language_code = (data.get('language') or '').lower()

        if language_code in {"en", "eng", "english"}:
            language = [
                Relatant.from_language_dict({
                    "ID": f"mardi:{ITEMS['english']}",
                    "Name": "English",
                    "Description": "West Germanic language",
                })
            ]
        else:
            language = []

        # Get Publication Title
        title = data.get('title')

        # Get Publication Date
        published = data.get('published', {}).get('date-parts', [])

        date_parts = published[0] if published else []

        if len(date_parts) == 1:
            date = f"{date_parts[0]:04d}-00-00T00:00:00Z"
        elif len(date_parts) == 2:
            date = f"{date_parts[0]:04d}-{date_parts[1]:02d}-00T00:00:00Z"
        elif len(date_parts) >= 3:
            date = f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}T00:00:00Z"
        else:
            date = None

        # Get Publication Volume
        volume = data.get('volume')

        # Get Publication Issue
        issue = data.get('issue')

        # Get Publication Page
        page = data.get('page')

        # Get Publication Reference
        reference = {}
        if doi:
            reference = {0: [options['DOI'], doi]}

        # Get Publication Journal
        journal = []
        if 'ISSN' in data or 'container-title' in data:
            journal = [
                Journal.from_doi(
                    data.get('ISSN', []),
                    data.get('container-title', [])
                )
            ]

        # Get Publication Authors
        authors = []
        if 'author' in data:
            authors = [
                Author.from_doi(author)
                for author in data.get('author', [])
                if author
            ]

        return cls(
            id = id,
            label = label,
            description = description,
            entrytype = entrytype,
            language = language,
            title = title,
            date = date,
            volume = volume,
            issue = issue,
            page = page,
            reference = reference,
            journal = journal,
            authors = authors
        )
    
    @classmethod
    def from_zbmath(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json().get('result', [''])[0]

        options = cls.get_options()
        ITEMS = get_items()

        # Get Publication MaRDI Portal ID
        id = None

        # Get Publication DOI
        doi = None
        for link in data.get('links'):
            if link.get('type') == 'doi':
                doi = link.get('identifier')
                break

        # Get Publication Label
        label = None

        # Get Publication Description
        if doi:
            description = f'scientific article (doi {doi})'
        else:
            description = f'scientific article'

        # Get Publication Entrytype
        if data.get('document_type', {}).get('description') == 'journal article':
            entrytype = 'scholarly article'
        else:
            entrytype = 'publication'

        # Get Publication Language
        language_codes = data.get('language', {}).get('languages') or ['']

        if any(code.lower() in {"en", "eng", "english"} for code in language_codes):
            language = [
                Relatant.from_language_dict({
                    "ID": f"mardi:{ITEMS['english']}",
                    "Name": "English",
                    "Description": "West Germanic language",
                })
            ]
        else:
            language = []

        # Get Publication Date
        date = None
        if data.get('year'):
            date = f"{int(data['year']):04d}-00-00T00:00:00Z"

        # Get Publication Title
        title = data.get('title', {}).get('title')

        # Get Publication... 
        source = data.get('source', {})

        # Volume
        volume = (source.get('series') or [''])[0].get('volume')

        # Issue
        issue = (source.get('series') or [''])[0].get('issue')

        # Page
        page = source.get('page')

        # Get Publication Reference
        reference = {}
        if doi:
            reference = {0: [options['DOI'], doi]}

        # Get Publication Journal
        journal = []
        if 'source' in data:
            journal = [
                Journal.from_zbmath(
                    data.get('source', {})
                )
            ]

        # Get Publication Authors
        authors = []
        if 'contributors' in data:
            authors = [
                Author.from_zbmath(author)
                for author in data.get('contributors', {}).get('authors', [])
                if author
            ]

        return cls(
            id = id,
            label = label,
            description = description,
            entrytype = entrytype,
            language = language,
            title = title,
            date = date,
            volume = volume,
            issue = issue,
            page = page,
            reference = reference,
            journal = journal,
            authors = authors
        )
