from dataclasses import dataclass, field
from typing import List, Optional
from .id import *
import os, json


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
        return cls(
            id = None,
            label = f"{raw.get('given', '')} {raw.get('family', '')}",
            description = None,
            orcid_id = raw.get('ORCID').split('/')[-1] if raw.get('ORCID') else None,
            zbmath_id = None,
            wikidata_id = None
        )
    
    @classmethod
    def from_datacite(cls, raw: str) -> 'Author':
        return cls(
            id = None,
            label = f"{raw.get('givenName', '')} {raw.get('familyName', '')}",
            description = None,
            orcid_id = next((id.get('nameIdentifier', '').split('/')[-1] for id in raw.get('nameIdentifiers', []) if id.get('nameIdentifierScheme') == 'ORCID'), None),
            zbmath_id = None,
            wikidata_id = None
        )
    
    @classmethod
    def from_doi(cls, raw: str) -> 'Author':
        return cls(
            id = None,
            label = f"{raw.get('given', '')} {raw.get('family', '')}",
            description = None,
            orcid_id = raw.get('ORCID').split('/')[-1] if raw.get('ORCID') else None,
            zbmath_id = None,
            wikidata_id = None
        )
    
    @classmethod
    def from_zbmath(cls, raw: str) -> 'Author':
        return cls(
            id = None,
            label = " ".join(reversed([s for s in raw['name'].split(", ")])),
            description = None,
            orcid_id = None,
            zbmath_id = raw['codes'][0] if raw.get('codes') else None,
            wikidata_id = None
        )
    
    @classmethod
    def from_orcid(cls, raw: str) -> 'Author':
        return cls(
            id = None,
            label = f"{raw.get('name', {}).get('given-names', {}).get('value', '')} {raw.get('name', {}).get('family-name', '').get('value', '')}",
            description = None,
            orcid_id = raw.get('name', {}).get('path'),
            zbmath_id = None,
            wikidata_id = None
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
    def from_crossref(cls, id: str, label: str) -> 'Journal':
        return cls(
            id = None,
            issn = id[0] if id else None,
            label = label[0] if label else None,
            description = None,
        )
    
    @classmethod
    def from_datacite(cls, id: str, item: str) -> 'Journal':
        issn = None; label = None
        if id:
            issn = id[0].get('relatedIdentifier') if id[0].get('relatedIdentifierType') == 'ISSN' else None
        if item:
            label = item[0].get('titles', [{}])[0].get('title')
        return cls(
            id = None,
            issn = issn,
            label = label,
            description = None,
        )
    
    @classmethod
    def from_doi(cls, id: str, label: str) -> 'Journal':
        return cls(
            id = None,
            issn = id[0] if id else None,
            label = label,
            description = None,
        )
    
    @classmethod
    def from_zbmath(cls, raw: str) -> 'Journal':
        return cls(
            id = None,
            issn = raw.get('series', [{}])[0].get('issn', [{}])[0].get('number'),
            label = raw.get('series', [{}])[0].get('title'),
            description = None,
        )


@dataclass
class Publication:
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    entrytype: Optional[str]
    language: Optional[str]
    title: Optional[str]
    date: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    page: Optional[str]
    journal: Optional[List[Journal]] = field(default_factory=list)
    authors: Optional[List[Author]] = field(default_factory=list)

    @classmethod
    def from_query(cls, raw_data: dict) -> 'Publication':

        data = raw_data[0]

        path = os.path.join(os.path.dirname(__file__), 'data', 'lang.json')
        with open(path, "r") as json_file:
            lang_dict = json.load(json_file)

        return cls(
            id = data.get('id', {}).get('value'),
            label = data.get('label', {}).get('value'),
            description = data.get('description', {}).get('value'),
            entrytype = data.get('entrytypelabel', {}).get('value'),
            language = lang_dict[data.get('langaugelabel', {}).get('value').lower()][3] if data.get('langaugelabel', {}).get('value') else None,
            title = data.get('title', {}).get('value'),
            date = data.get('date', {}).get('value')[:10] if 'date' in data else None,
            volume = data.get('volume', {}).get('value'),
            issue = data.get('issue', {}).get('value'),
            page = data.get('page', {}).get('value'),
            journal = [Journal.from_query(data.get('journalInfo', {}).get('value'))] if 'journalInfo' in data else [],
            authors = [
                Author.from_query(author)
                for author in data.get('authorInfos', {}).get('value', '').split(" | ")
                if author
            ] if 'authorInfos' in data else [],
        )
    
    @classmethod
    def from_crossref(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json().get('message', {})

        path = os.path.join(os.path.dirname(__file__), 'data', 'lang.json')
        with open(path, "r") as json_file:
            lang_dict = json.load(json_file)

        return cls(
            id = None,
            label = None,
            description = None,
            entrytype = 'scholarly article' if data.get('type', '') == 'journal-article' else 'publication',
            language = lang_dict[data.get('language','').lower()][3] if data.get('language') else None,
            title = data.get('title', [''])[0],
            date = '{0[0]}-{0[1]:02d}-{0[2]:02d}'.format(data.get('published', {}).get('date-parts', [''])[0] + [1] * (3 - len(data.get('published', {}).get('date-parts', [''])))),
            volume = data.get('volume', ''),
            issue = data.get('issue', ''),
            page = data.get('page', ''),
            journal = [Journal.from_crossref(data.get('ISSN'), data.get('container-title'))] if 'ISSN' in data or 'container-title' in data else [],
            authors = [
                Author.from_crossref(author)
                for author in data.get('author', [])
                if author
            ] if 'author' in data else [],
        )
    
    @classmethod
    def from_datacite(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json().get('data', {}).get('attributes', {})

        path = os.path.join(os.path.dirname(__file__), 'data', 'lang.json')
        with open(path, "r") as json_file:
            lang_dict = json.load(json_file)

        return cls(
            id = None,
            label = None,
            description = None,
            entrytype = 'scholarly article' if data.get('types', {}).get('bibtex', '') == 'article' else 'publication',
            language = lang_dict[data['language'].lower()][3] if data.get('language') else None,
            title = data.get('titles', [''])[0].get('title', ''),
            date = next((date_part.get('date')+'-01-01' if len(date_part.get('date')) == 4 else date_part.get('date')+'-01' if len(date_part.get('date')) == 7 else date_part.get('date') for date_part in data.get('dates', []) if date_part.get('dateType') == 'Issued'), ''),
            volume = data['relatedItems'][0].get('volume') if data.get('relatedItems') else None,
            issue = data['relatedItems'][0].get('issue') if data.get('relatedItems') else None,
            page = f"{data['relatedItems'][0].get('firstPage', '')}-{data['relatedItems'][0].get('lastPage', '')}" if data.get('relatedItems') else None,
            journal = [Journal.from_datacite(data.get('relatedIdentifiers'), data.get('relatedItems'))] if 'relatedIdentifiers' in data or 'relatedItems' in data else [],            
            authors = [
                Author.from_datacite(author)
                for author in data.get('creators', [])
                if author
            ] if 'creators' in data else [],
        )
    
    @classmethod
    def from_doi(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json()

        path = os.path.join(os.path.dirname(__file__), 'data', 'lang.json')
        with open(path, "r") as json_file:
            lang_dict = json.load(json_file)

        return cls(
            id = None,
            label = None,
            description = None,
            entrytype = 'scholarly article' if data.get('type', {}) == 'journal-article' else 'publication',
            language = lang_dict[data.get('language','').lower()][3] if data.get('language') else None,
            title = data.get('title', ''),
            date = '{0[0]}-{0[1]:02d}-{0[2]:02d}'.format(data.get('published-online', {}).get('date-parts', [''])[0] + [1] * (3 - len(data.get('published-online', {}).get('date-parts', [''])))),
            volume = data.get('volume'),
            issue = data.get('issue'),
            page = data.get('page'),
            journal = [Journal.from_doi(data.get('ISSN'), data.get('container-title'))] if 'ISSN' in data or 'container-title' in data else [],
            authors = [
                Author.from_doi(author)
                for author in data.get('author', [])
                if author
            ] if 'author' in data else [],
        )
    
    @classmethod
    def from_zbmath(cls, raw_data: dict) -> 'Publication':

        data = raw_data.json().get('result', [''])[0]

        path = os.path.join(os.path.dirname(__file__), 'data', 'lang.json')
        with open(path, "r") as json_file:
            lang_dict = json.load(json_file)

        return cls(
            id = None,
            label = None,
            description = None,
            entrytype = 'scholarly article' if data.get('document_type', {}).get('description') == 'journal article' else 'publication',
            language = lang_dict[data.get('language',{}).get('languages',[''])[3].lower()][0] if data.get('language',{}).get('languages') else None,
            title = data.get('title', {}).get('title', {}),
            date = f"{data.get('year','')}-01-01",
            volume = data.get('source', {}).get('series', [''])[0].get('volume'),
            issue = data.get('source', {}).get('series', [''])[0].get('issue'),
            page = data.get('source', {}).get('page'),
            journal = [Journal.from_zbmath(data.get('source'))] if 'source' in data else [],
            authors = [
                Author.from_zbmath(author)
                for author in data.get('contributors', {}).get('authors', [])
                if author
            ] if 'contributors' in data else [],
        )