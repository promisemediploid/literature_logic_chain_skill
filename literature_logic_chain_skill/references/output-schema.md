# Literature Logic Chain output schema

The canonical internal representation is a JSON object with these top-level fields:

- `title`: paper title
- `subtitle`: short framing line
- `opening_explanation`: one full paragraph (roughly 250–500 Chinese characters) that explains the whole paper's causal chain. This replaces the older "one-sentence logic" opening; do not compress it into a slogan.
- `prerequisites`: `{ "required": [], "recommended": [], "nice_to_know": [] }`. Terms only — no cards, no teaching, no large footprint.
- `nodes`: ordered logic-chain nodes
- `edges`: causal links between nodes, as `{"from": "<node-id>", "to": "<node-id>"}`
- `experiments`: evidence records, ideally `{"claim": ..., "method": ..., "supports": ["<node-id>"]}`
- `limitations`: limitation records, as plain strings or objects

`summary` is still accepted for backward compatibility, but `opening_explanation` is what the page renders.

## Node fields

Required by `scripts/generate_logic_html.py`:

| Field | Meaning |
| --- | --- |
| `id` | unique node id, referenced by `edges` and `depends_on` |
| `stage` | one of the stage vocabulary below |
| `title` | a full question or causal judgement used for navigation |
| `explanation` | 2–5 complete sentences; this is the main body text and is always visible |
| `why` | why the reader must be brought to this step |
| `function` | what this step contributes to the whole method |
| `if_omitted` | what breaks, gets ambiguous, or becomes a shortcut if this step is removed or changed |
| `evidence` | list of experiments, figures, ablations, or paper references supporting the explanation |

Optional:

- `source`: page/section/figure pointers
- `depends_on`: upstream node ids
- `short`: brief navigation hint (legacy)

## Stage vocabulary

`problem`, `gap`, `hypothesis`, `data`, `model`, `training`, `downstream`, `evidence`, `limitation`.

## Validation

`scripts/generate_logic_html.py` checks that all required top-level and node fields exist, that every `stage` is valid, that node ids are unique, and that every edge points to an existing node. Run the generator first to fail fast on malformed input.

## Rendering rule

The visualization preserves node order and edge structure so the HTML is an alternate view of the textual reasoning, never an independent summary. Explanations are displayed by default; interactions only help locate and compare them.
