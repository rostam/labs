# Five Instruments

Landing page for five browser-based research tools.

**[rostam.github.io/labs →](https://rostam.github.io/labs/)**

| | |
| --- | --- |
| [Conjecture Engine](https://github.com/rostam/graph-conjectures) | Mines bounds between graph invariants from every connected graph up to 8 vertices, then tries to break them |
| [PreCol Playground](https://github.com/rostam/precol-playground) | Sparse-matrix colouring for Jacobian compression, with live verification |
| [Literary Atlas](https://github.com/rostam/literary-atlas) | 191 book reviews placed where the books are set |
| [GTea Rosetta](https://github.com/rostam/gtea-rosetta) | The same graph algorithms in five languages, compared against one contract |
| [Geomagnetic Network](https://github.com/rostam/geomagnetic-graph) | 20 observatories as a correlation graph, rewired daily for 13 years |

The previews are real geometry rather than screenshots — the Petersen graph is drawn
from its actual coordinates, the coastlines from the same TopoJSON the atlas uses, the
agreement grid from the actual harness result. `build/` holds the generator.

## Rebuilding the page

```bash
python3 build/make_index.py     # regenerates docs/index.html
python3 -m http.server -d docs 8806
```
