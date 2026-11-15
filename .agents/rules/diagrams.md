# Diagrams

A README diagram is read at a glance or not at all. It shows where things
happen in the code, so a reader knows which module to open.

## What is drawn

- **A node is something in the code**: a class, a module, a service, a
  file, named as the code names it. A short gloss may follow the name
  (`Holdout: last 205 cycles`); a sentence may not.
- **What travels goes on the arrow**, never in a node: a request type is a
  label, not a box.
- **A box is a boundary in the repository**: the package the README
  describes in a solid yellow frame, its folders in grey dashed boxes,
  another library of the workspace in a teal dashed node or box outside it.
- **One meaning per kind of link**, stated in one line under the diagram:

| Link | Meaning |
| --- | --- |
| solid arrow, labelled | happens on every request |
| dotted arrow | happens once, at start |
| dotted line, no head | imports the types of another library |

- **The flow goes one way.** No arrow back against it, no two crossing.

## How it is laid out

A Markdown page is a line of text. A preview scales every diagram to the
page width, so its natural width sets the size of its text: between 1100
and 1350 pixels it reads like the page, past 1350 the text shrinks past
reading, under 1100 a few boxes are blown up larger than the headings. Fill
the width while a row stays readable, then wrap to the next row.

- **A box's contents go across; the boxes stack down.** Two boxes in a
  chain stack, they do not sit side by side past the page.
- **Nothing narrow and tall**: a single column wastes the page as much as
  a long row overflows it.
- Something outside the package sits next to what uses it, not in a
  corner.

## How Mermaid places things

- A node sits one rank after whatever points to it. To lift a node to the
  first rank, declare its link from it: `runtime -.- classifier`.
- `direction LR` inside a subgraph holds only when none of its nodes links
  outside it. Link the boxes, not their nodes: `services --> core`.
- Unlinked nodes in a subgraph stack; chain them with `~~~` to lay them in
  a row.
- `A <--|label| B` does not parse.

## Before showing it

`just agent::diagrams <file>...` renders every diagram of the files into
`build/diagrams/` and prints each one's width against the page
([diagrams.sh](../checks/diagrams.sh)). Look at every image before
handing it over: the width is only the first check. It downloads
mermaid-cli, so it runs on demand, never in the gate.
