# Literature Logic Chain output schema

The canonical internal representation is a JSON object with these top-level fields:

- `title`: paper title
- `subtitle`: short framing line
- `summary`: one-sentence causal summary
- `nodes`: ordered logic-chain nodes
- `edges`: causal links between nodes
- `experiments`: evidence records
- `limitations`: limitation records

Each node should answer four questions:

1. Why does this step exist?
2. What does it do?
3. What becomes weaker/ambiguous/wrong if it is removed or changed?
4. What evidence supports that explanation?

Recommended stage vocabulary:

`problem`, `gap`, `hypothesis`, `data`, `model`, `training`, `downstream`, `evidence`, `limitation`.

The visualization should preserve the node order and edge structure so the HTML is an alternate view of the textual reasoning rather than an independent summary.
