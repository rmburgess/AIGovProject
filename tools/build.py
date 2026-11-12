"""Build app/index.html from app/template.html and the library files in content/.

Usage: python3 tools/build.py
The library JSON is inlined into the page so the published page is one file.
"""
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
modules = {}
for name in ["iud", "cervical"]:
    modules[name] = json.loads((root / "content" / f"{name}.json").read_text())

# Every cited id must exist in the module's sources, and every card id must be unique.
seen = set()
for m in modules.values():
    for c in m["cards"]:
        assert c["id"] not in seen, f"duplicate card id {c['id']}"
        seen.add(c["id"])
        for s in c.get("cites", []) + [x for h in c.get("harder", []) for x in h[1]]:
            assert s in m["sources"], f"{c['id']} cites unknown source {s}"

demo = json.loads((root / "content" / "demo.json").read_text())
for name, d in demo.items():
    ids = {c["id"] for c in modules[name]["cards"]}
    for sec in d["plan"]["sections"]:
        for it in sec["items"]:
            for cid in it["cites"]:
                assert cid in ids, f"demo plan for {name} cites unknown card {cid}"
    # the trap plan is meant to contain bad citations and a dose; it must contain at least one of each
    bad = [cid for sec in d["trap"]["sections"] for it in sec["items"] for cid in it["cites"] if cid not in ids]
    assert bad, f"demo trap for {name} should contain an unknown card id"

scenarios = json.loads((root / "eval" / "scenarios.json").read_text())
ids = set()
for s in scenarios:
    assert s["id"] not in ids, f"duplicate scenario id {s['id']}"
    ids.add(s["id"])
    assert s["module"] in modules, f"scenario {s['id']} has unknown module"

template = (root / "app" / "template.html").read_text()
marker = "/*__DATA__*/null"
assert marker in template, "template is missing the data marker"
out = template.replace(marker, json.dumps({"modules": modules, "demo": demo, "scenarios": scenarios}, ensure_ascii=False))
(root / "app" / "index.html").write_text(out)
print("built app/index.html", len(out), "bytes")
