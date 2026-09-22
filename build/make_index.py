"""Regenerate docs/index.html.

The previews are real geometry, not screenshots: the Petersen graph from its
standard pentagon/pentagram coordinates, the coastlines from the same TopoJSON the
atlas uses, the observatory positions from the INTERMAGNET station list. Edit
INSTRUMENTS below for copy, then re-run:

    python3 build/make_index.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
LAND = os.path.abspath(os.path.join(ROOT, "..", "literary-atlas", "docs", "data", "land.json"))
WORLD_CACHE = os.path.join(HERE, "world_mini.txt")

# ---------------------------------------------------------------- previews

def world_path():
    """Coastlines, heavily simplified, in a 200x100 equirectangular box.

    Cached next to this script so the page can be rebuilt without the atlas
    repository checked out alongside.
    """
    if not os.path.exists(LAND):
        if os.path.exists(WORLD_CACHE):
            return open(WORLD_CACHE).read()
        raise SystemExit(f"need {LAND} or the cached {WORLD_CACHE}")

    rings = json.load(open(LAND))
    keep = [r for r in rings if len(r) > 28][:14]
    out = []
    for ring in keep:
        pts = ring[::4]
        if pts[-1] != ring[-1]:
            pts.append(ring[-1])
        out.append("M" + "L".join(
            f"{(lon + 180) / 360 * 200:.1f},{(90 - lat) / 180 * 100:.1f}" for lon, lat in pts) + "Z")
    d = "".join(out)
    open(WORLD_CACHE, "w").write(d)
    return d


def proj(lon, lat):
    return ((lon + 180) / 360 * 200, (90 - lat) / 180 * 100)


def petersen():
    """Outer pentagon, inner pentagram, five spokes — the standard drawing."""
    outer = [(50 + 34 * math.sin(2 * math.pi * i / 5), 50 - 34 * math.cos(2 * math.pi * i / 5)) for i in range(5)]
    inner = [(50 + 16 * math.sin(2 * math.pi * i / 5), 50 - 16 * math.cos(2 * math.pi * i / 5)) for i in range(5)]
    edges = ([(outer[i], outer[(i + 1) % 5]) for i in range(5)]
             + [(outer[i], inner[i]) for i in range(5)]
             + [(inner[i], inner[(i + 2) % 5]) for i in range(5)])
    lines = "".join(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>' for a, b in edges)
    dots = "".join(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="4"/>' for p in outer + inner)
    return f'<svg viewBox="0 0 100 100" class="pet">{lines}{dots}</svg>'


def sparsity(n=14, seed=4):
    """A small pattern with its columns grouped into colour classes."""
    import random
    rng = random.Random(seed)
    cols = [(j * 5) % 7 for j in range(n)]
    cells = "".join(
        f'<rect x="{j * 7}" y="{i * 7}" width="6" height="6" class="c{cols[j]}"/>'
        for i in range(n) for j in range(n) if i == j or rng.random() < 0.13)
    bar = "".join(f'<rect x="{j * 7}" y="-9" width="6" height="6" class="c{cols[j]}"/>' for j in range(n))
    return f'<svg viewBox="-2 -12 102 112" class="spars">{bar}{cells}</svg>'


def agreement_grid():
    """Five implementations against five, all agreeing — the harness result."""
    cells = "".join(
        f'<rect x="{c * 19}" y="{r * 19}" width="17" height="17" class="{"self" if r == c else "ok"}"/>'
        for r in range(5) for c in range(5))
    return f'<svg viewBox="-1 -1 97 97" class="agree">{cells}</svg>'


BOOK_SETTINGS = [
    (139.7, 35.7), (-0.1, 51.5), (30.3, 59.9), (-74.0, 40.7), (2.3, 48.9), (51.4, 35.7),
    (2.2, 41.4), (12.5, 41.9), (13.4, 52.5), (-58.4, -34.6), (-99.1, 19.4), (126.98, 37.6),
    (72.9, 19.1), (-9.1, 38.7), (28.98, 41.0), (-122.4, 37.8), (37.6, 55.8), (4.9, 52.4),
    (-79.4, 43.7), (18.4, -33.9), (151.2, -33.9), (-3.7, 40.4), (79.9, 6.9), (3.4, 6.5),
]

# INTERMAGNET observatories that survive the 2010-2022 coverage cut.
OBSERVATORIES = [
    (-4.5, 50.9), (2.3, 48.0), (0.3, 41.0), (5.7, 50.3), (23.9, 38.1), (14.3, 41.4),
    (38.8, 9.0), (27.7, -25.9), (19.2, -34.4), (72.9, 18.6), (78.6, 17.4),
    (104.5, 52.2), (83.2, 54.9), (126.9, 36.4), (130.9, 31.4), (87.7, 43.8),
    (-89.6, 30.4), (-43.7, -22.4),
]


def atlas_map(world):
    dots = "".join(
        f'<circle cx="{proj(a, b)[0]:.1f}" cy="{proj(a, b)[1]:.1f}" r="{2.6 if i % 4 == 0 else 1.8}"/>'
        for i, (a, b) in enumerate(BOOK_SETTINGS))
    return (f'<svg viewBox="0 0 200 100" class="world"><path class="land" d="{world}"/>'
            f'<g class="dots">{dots}</g></svg>')


def network_map(world):
    pts = [proj(a, b) for a, b in OBSERVATORIES]
    lines = "".join(
        f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}"/>'
        for i in range(len(pts)) for j in range(i + 1, len(pts)) if (i * 7 + j) % 3 == 0)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9"/>' for x, y in pts)
    return (f'<svg viewBox="0 0 200 100" class="world"><path class="land" d="{world}"/>'
            f'<g class="net">{lines}{dots}</g></svg>')


# ---------------------------------------------------------------- content

def instruments(world):
    return [
        dict(
            slug="graph-conjectures", accent="#1C56D6", title="Conjecture Engine",
            preview=petersen(),
            body="""Mines inequalities between graph invariants from every connected graph up to eight
        vertices, then attacks the survivors with graphs it never saw. It rediscovers Wilf's
        theorem. It also proposes &chi; &le; &omega; + 1, which is false &mdash; and finds the Gr&ouml;tzsch
        graph that kills it.""",
            meta="21,139 graphs &middot; 33 exact invariants"),
        dict(
            slug="precol-playground", accent="#7A3CB8", title="PreCol Playground",
            preview=sparsity(),
            body="""Colour a sparse matrix's bipartite graph and watch the number of matrix&ndash;vector
        products fall. On a 183&times;183 Jacobian: 183 products uncompressed, 72 one-sided,
        20 with star bicolouring, 11 if you only need the band. Every count is verified
        against the definition before it is shown.""",
            meta="Ten SuiteSparse matrices, or drop your own"),
        dict(
            slug="literary-atlas", accent="#0F766E", title="Literary Atlas",
            preview=atlas_map(world),
            body="""191 book reviews placed where the books are <em>set</em> rather than where they were
        published, as a map and as a timeline of how far back each author reached. Median
        reach is 14 years; <em>The Name of the Rose</em> reaches back 653.""",
            meta="147 placed, the rest honestly unplaceable"),
        dict(
            slug="gtea-rosetta", accent="#B02A6E", title="GTea Rosetta",
            preview=agreement_grid(),
            body="""The same graph algorithms in Python, JavaScript, C++, Rust and Java, run against one
        contract pinned tightly enough that any disagreement is a bug. 1,100 comparisons, zero
        disagreements &mdash; except the spectral radius, which differs by 3.6 &times; 10<sup>&minus;15</sup> and always will.""",
            meta="Five graph libraries in this account; nothing checked they still agreed"),
        dict(
            slug="geomagnetic-graph", accent="#00786B", title="Geomagnetic Network",
            preview=network_map(world),
            body="""Twenty magnetic observatories as one correlation graph, rewired every day for
        thirteen years. On a quiet day the network splits into geographic communities; during
        the March 2015 storm the communities stop existing and modularity hits zero.""",
            meta="12&nbsp;GB of minute data &middot; 4,748 daily graphs"),
    ]


def row(it):
    url = f"https://rostam.github.io/{it['slug']}/"
    return f'''    <li class="row" style="--sig:{it['accent']}">
      <a class="plate" href="{url}" aria-hidden="true" tabindex="-1">
        {it['preview']}
      </a>
      <div class="text">
        <h2><a href="{url}">{it['title']}</a></h2>
        <p>{it['body']}</p>
        <p class="meta">{it['meta']} &middot; <a href="https://github.com/rostam/{it['slug']}">source</a></p>
      </div>
    </li>
'''


def build():
    world = world_path()
    rows = "\n".join(row(it) for it in instruments(world))
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Five Instruments</title>
<meta name="description" content="Five things built out of the research already sitting in this account: graph conjectures, sparse-matrix colouring, a literary atlas, a five-language conformance harness, and geomagnetic storms as graph dynamics.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect x='1' y='1' width='6' height='6' fill='%231C56D6'/><rect x='9' y='1' width='6' height='6' fill='%237A3CB8'/><rect x='1' y='9' width='6' height='6' fill='%230F766E'/><rect x='9' y='9' width='6' height='6' fill='%23B02A6E'/></svg>">
<link rel="stylesheet" href="css/plate.css">
<link rel="stylesheet" href="css/app.css">
</head>
<body>
<header class="top">
  <h1>Five Instruments</h1>
  <a href="https://github.com/rostam">github.com/rostam</a>
</header>

<main>
  <section class="intro">
    <p class="lede">Five working tools, each built out of research that was already
    sitting in this account as a paper, a C++ build or a folder of CSVs &mdash; and was
    therefore impossible to look at without checking something out and compiling it.
    Everything below opens in a browser.</p>
  </section>

  <ol class="rack">

{rows}
  </ol>

  <footer>
    <p>Each one reuses something that was already here &mdash; a dissertation's colouring
    heuristics, a Persian book blog, five ports of the same graph library, a folder of
    INTERMAGNET CSVs. The work was done; it just had no front door.</p>
  </footer>
</main>
</body>
</html>
'''
    dest = os.path.join(ROOT, "docs", "index.html")
    open(dest, "w").write(html)
    print(f"wrote {dest}: {len(html) / 1024:.0f} KB, {len(instruments(world))} instruments")


if __name__ == "__main__":
    build()
