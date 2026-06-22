# How to Register a Question in MaRDMO

MaRDMO reads answers from the RDMO interview by looking up each question's URI and
extracting the value according to a set of configuration flags.  Registering a new
question means adding an entry to the relevant `<submodule>/data/questions.json`
file so that MaRDMO knows where to find the answer and how to store it.

---

## Step 1 — Locate the questions.json file

Each submodule has its own registry:

| Submodule | File |
|---|---|
| Model | `model/data/questions.json` |
| Algorithm | `algorithm/data/questions.json` |
| Workflow | `workflow/data/questions.json` |
| Publication | `publication/data/questions.json` |
| Search | `search/data/questions.json` |

Open the file for the submodule the new question belongs to.

---

## Step 2 — Add the entry

Add a new key under the appropriate entity group.  The minimum required fields are
`key1`, `key2`, and `uri`:

```json
"My New Question": {
    "key1": "model",
    "key2": "myfield",
    "uri": "domain/model/myfield"
}
```

Fill in the remaining fields according to steps 3 and 4 below.

---

## Step 3 — Set key1, key2, key3, and uri

**`key1`** is the entity class the answer belongs to (e.g. `"model"`, `"quantity"`,
`"software"`).  It becomes the top-level key in the answers dict.

**`key2`** is the specific question name within that entity (e.g. `"Name"`,
`"Description"`, `"reference"`).  It becomes the second-level key.

**`key3`** is only needed for deeply nested questions where the same entity block
holds multiple sub-fields under one key2 (e.g. `"author"` → `"ID"`, `"Name"`,
`"orcid"`).  Leave it out if not needed.

**`uri`** is the RDMO attribute URI fragment — the part after
`https://rdmo.mardi4nfdi.de/terms/`.  Check the RDMO admin interface under
*Domain → Attributes* for the exact value.

---

## Step 4 — Set the five boolean flags

The five flags determine how the answer is extracted and where it is stored.
Set only the ones that apply; all others default to `false`.

### set_prefix

Set to `true` when the question lives inside a **nested question set** (a question
set that is itself inside a collection page).  This inserts the entity instance
index into the path so that answers for different instances do not overwrite each
other.

### set_index

Set to `true` when the question lives inside a **question set** (not a top-level
page question).  This inserts the question set instance index into the path.

### collection_index

Set to `true` when the RDMO question is a **collection** (the user can provide
multiple answers for a single question).  This appends the answer index to the
path.

### external_id

Set to `true` when the question links to another entity via RDMO's external ID
mechanism (e.g. a relatant question that stores a reference to another portal
item).  The answer is stored as an `{ID, Name, Description}` dict or as a raw
external ID string depending on the path shape — see the
[Question Configuration Reference](../../reference/questions.md).

### option_text

Set to `true` when the question uses an **optionset combined with a free-text
field** — for example, a reference question where the option identifies the
reference type (DOI, URL) and the text holds the actual value.  The answer is
stored as a `[option_uri, text]` pair.

---

## Step 5 — Look up the correct flag combination

Once you have determined which flags apply, consult the
[Question Configuration Reference](../../reference/questions.md) to confirm the
resulting path and entry type.  Make sure the path and type match what the
downstream handler code expects for this entity.

---

## Example

A quantity reference question that lives in a nested question set (`set_prefix`),
is a collection (`collection_index`), and captures both a reference type option
and a URL (`option_text`):

```json
"Reference": {
    "key1": "quantity",
    "key2": "reference",
    "uri": "domain/quantity/reference",
    "set_prefix": true,
    "collection_index": true,
    "option_text": true
}
```

This matches flag combo `(✓ ✗ ✓ ✗ ✓)` → rule 17 → path
`[quantity, prefix_idx, reference, coll_index]` → list entry `[option_uri, text]`.
