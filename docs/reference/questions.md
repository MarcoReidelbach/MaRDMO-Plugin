# Question Configuration Reference

MaRDMO extracts interview answers from RDMO by reading each registered question's
configuration from `<submodule>/data/questions.json` and routing the value through
a rule function determined by five boolean flags.  This page documents the
configuration fields and the complete flag-to-rule mapping.

---

## Configuration fields

Each question entry inside `questions.json` has the following fields:

| Field | Required | Description |
|---|---|---|
| `uri` | yes | RDMO attribute URI fragment (without the base URI `https://rdmo.mardi4nfdi.de/terms/`) |
| `key1` | yes | Top-level key in the answers dict — the entity class name (e.g. `"field"`, `"model"`) |
| `key2` | yes | Second-level key — the specific question name within the entity (e.g. `"ID"`, `"Name"`) |
| `key3` | no | Optional third-level key for deeply nested structures |
| `set_prefix` | no | `true` when the question belongs to a nested (collection) question set — the entity instance index is inserted into the path |
| `set_index` | no | `true` when the question belongs to a question set — the question set instance index is inserted into the path |
| `collection_index` | no | `true` when the question is a collection (multiple answers) — the answer index is appended to the path |
| `external_id` | no | `true` to extract the entity reference stored for this question as `{ID, Name, Description}` or a raw external ID |
| `option_text` | no | `true` to extract both the selected option's URI and the entered text as a `[option_uri, text]` pair — used when a question captures both a relation type (option) and a related entity name (text) |

Omitted boolean fields default to `false`.

---

## Flag combinations and resulting paths

The five boolean flags `(set_prefix, set_index, collection_index, external_id, option_text)`
are read from the question config at runtime and used to look up the correct extraction
rule in `flag_dict` (defined in `constants.py`).

The **entry type** column describes what is stored at the resulting path:

- **raw** — `value.option_uri` if an option was selected, otherwise `value.text`
- **list** — a `[option_uri, text]` pair from `basic_list(value)`
- **dict** — an entity reference dict `{ID, Name, Description}` from `basic_dict(value)`
- **ext_id** — `value.external_id`

### Raw entries

| set_prefix | set_index | coll_index | ext_id | opt_text | Rule | Resulting path |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| ✗ | ✗ | ✗ | ✗ | ✗ | 0 | `[key1, key2]` |
| ✓ | ✗ | ✗ | ✗ | ✗ | 1 | `[key1, prefix_idx, key2]` |
| ✗ | ✓ | ✗ | ✗ | ✗ | 2 | `[key1, set_index, key2]` |
| ✗ | ✗ | ✓ | ✗ | ✗ | 10 | `[key1, key2, coll_index]` |
| ✓ | ✓ | ✗ | ✗ | ✗ | 3 | `[key1, prefix_idx, key2, set_index]` (+ `key3`) |
| ✗ | ✓ | ✓ | ✗ | ✗ | 4 | `[key1, set_index, key2, coll_index]` (+ `key3`) |
| ✓ | ✗ | ✓ | ✗ | ✗ | 5 | `[key1, prefix_idx, key2, coll_index]` |
| ✓ | ✓ | ✓ | ✗ | ✗ | 19 | `[key1, prefix_idx, key2, set_index, coll_index]` |

### External ID entries

| set_prefix | set_index | coll_index | ext_id | opt_text | Rule | Resulting path |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| ✗ | ✓ | ✗ | ✓ | ✗ | 12 | `[key1, set_index, key2]` |

### Dict entries (`{ID, Name, Description}`)

| set_prefix | set_index | coll_index | ext_id | opt_text | Rule | Resulting path |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| ✗ | ✗ | ✗ | ✓ | ✗ | 9 | `[key1]` |
| ✗ | ✗ | ✓ | ✓ | ✗ | 11 | `[key1, key2, coll_index]` |
| ✓ | ✓ | ✗ | ✓ | ✗ | 13 | `[key1, prefix_idx, key2, set_index]` (+ `key3`) |
| ✓ | ✗ | ✓ | ✓ | ✗ | 14 | `[key1, prefix_idx, key2, coll_index]` |
| ✓ | ✓ | ✓ | ✓ | ✗ | 15 | `[key1, prefix_idx, key2, set_index, coll_index]` |

### List entries (`[option_uri, text]`)

| set_prefix | set_index | coll_index | ext_id | opt_text | Rule | Resulting path |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| ✓ | ✗ | ✗ | ✗ | ✓ | 7 | `[key1, prefix_idx, key2]` |
| ✗ | ✓ | ✗ | ✗ | ✓ | 8 | `[key1, set_index, key2]` |
| ✓ | ✓ | ✗ | ✗ | ✓ | 16 | `[key1, prefix_idx, key2, set_index]` (+ `key3`) |
| ✓ | ✗ | ✓ | ✗ | ✓ | 17 | `[key1, prefix_idx, key2, coll_index]` |
| ✗ | ✓ | ✓ | ✗ | ✓ | 18 | `[key1, set_index, key2, coll_index]` (+ `key3`) |
| ✓ | ✓ | ✓ | ✗ | ✓ | 6 | `[key1, prefix_idx, key2, set_index, coll_index]` |
