#!/usr/bin/env python3
"""Build the dth-sfp ArchiMate overlay from the SFP work once held in smart-ra#182.

Owner rule (2026-11-01 08:13Z, card Q-RA1 A): a DTH builds an overlay on the
smart-ra model and does not add to it. This script copies the four SFP views,
every element and relationship they draw, and every other relationship the SFP
spec (smart-ra#182 tools/archimate-dth/dth_sfp.py) added, out of a source model
(the #182 branch file). Each item becomes one of:

- `overlay:base`: smart-ra already holds it; a reference copy under the same id
  whose value is its smart-ra IRI;
- `overlay:dth`: another DTH's overlay owns it (only dth-phc so far); a
  reference copy whose value is that overlay's IRI;
- `overlay:owner` = `dth-sfp`: this DTH adds it.

usage: extract_overlay.py <source model.xml> <smart-ra base model.xml> <smart-ra version>
                          <dth-phc overlay model.xml> <dth-phc version> <out .archimate>
"""
import copy, re, sys, zipfile
import xml.etree.ElementTree as ET

XSI = "http://www.w3.org/2001/XMLSchema-instance"
ARC = "http://www.archimatetool.com/archimate"
ET.register_namespace("xsi", XSI)
ET.register_namespace("archimate", ARC)
T = f"{{{XSI}}}type"
VIEW_FOLDER = "Substandard and Falsified Products (DTH SFP)"

src_path, base_path, base_ver, phc_path, phc_ver, out_path = sys.argv[1:7]
src = ET.parse(src_path).getroot()
base_ids = set(re.findall(r'\bid="([^"]+)"', open(base_path, encoding="utf-8").read()))
phc = ET.parse(phc_path).getroot()
phc_owned = {e.get("id") for e in phc.iter("element")
             if any(p.get("key") == "overlay:owner" and p.get("value") == "dth-phc" for p in e.findall("property"))}

top_type, by_id = {}, {}
for top in src.findall("folder"):
    for el in top.iter("element"):
        by_id[el.get("id")] = el
        top_type[el.get("id")] = top.get("type")

vf = next(f for f in src.iter("folder") if f.get("name") == VIEW_FOLDER)
views = [v for v in vf.iter("element") if v.get(T) == "archimate:ArchimateDiagramModel"]
assert len(views) == 4, [v.get("name") for v in views]

want = set()
for v in views:
    want.add(v.get("id"))
    for n in v.iter():
        for a in ("archimateElement", "archimateRelationship"):
            if n.get(a):
                want.add(n.get(a))
owned = lambda i: i not in base_ids and i not in phc_owned
# relationships the SFP spec added but no view draws (e.g. capability -> goal realizations)
for i, e in by_id.items():
    if e.get("source") and owned(i) and (owned(e.get("source")) and e.get("source") in want
                                         or owned(e.get("target")) and e.get("target") in want):
        want.add(i)
for i in list(want):  # a relationship needs both ends
    e = by_id.get(i)
    if e is not None and e.get("source"):
        want |= {e.get("source"), e.get("target")}
missing = sorted(i for i in want if i not in by_id)
assert not missing, missing

model = ET.Element(f"{{{ARC}}}model", {"name": "DTH-SFP overlay on the DPI-H reference architecture",
                                       "id": "id-dthsfp-overlay-0-1-0-draft-1", "version": "5.0.0"})
doc = ET.SubElement(model, "purpose")
doc.text = (f"Overlay of dth-sfp on smart-ra ArchiMate {base_ver}. Elements tagged overlay:base are reference "
            "copies of smart-ra elements (the IRI names the original); elements tagged overlay:dth are reference "
            f"copies of another DTH overlay's elements (dth-phc {phc_ver}); elements tagged overlay:owner=dth-sfp are "
            "added by this DTH and are not part of smart-ra. Built by scripts/archimate/extract_overlay.py.")
folders = {}
for top in src.findall("folder"):
    f = ET.SubElement(model, "folder", {"name": top.get("name"), "id": top.get("id"), "type": top.get("type")})
    folders[top.get("type")] = (f, ET.SubElement(f, "folder", {"name": "smart-ra (base, reference copies)",
                                                               "id": top.get("id") + "-base"}),
                                ET.SubElement(f, "folder", {"name": "dth-phc (overlay, reference copies)",
                                                            "id": top.get("id") + "-dth-phc"}))
iri = lambda repo, ver, e: (f"https://litlfred.github.io/{repo}/archimate/{ver}/"
                            f"{'views' if e.get(T).endswith('DiagramModel') else 'elements'}/{e.get('id')}.jsonld")
counts = {"owned": 0, "base": 0, "dth": 0}
for i in sorted(want, key=lambda i: (by_id[i].get(T), by_id[i].get("name") or "", i)):
    e = copy.deepcopy(by_id[i])
    owned_f, base_f, dth_f = folders[top_type[i]]
    if i in base_ids:
        prop, dest, k = ("overlay:base", iri("smart-ra", base_ver, e)), base_f, "base"
    elif i in phc_owned:
        prop, dest, k = ("overlay:dth", iri("dth-phc", phc_ver, e)), dth_f, "dth"
    else:
        prop, dest, k = ("overlay:owner", "dth-sfp"), owned_f, "owned"
    pos = next((n for n, c in enumerate(list(e)) if c.tag == "property"), len(list(e)))
    e.insert(pos, ET.Element("property", {"key": prop[0], "value": prop[1]}))
    dest.append(e)
    counts[k] += 1
for group in folders.values():
    for sub in group[1:]:
        if len(sub) == 0:
            group[0].remove(sub)
ET.indent(model)
xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(model, encoding="utf-8")
with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
    zi = zipfile.ZipInfo("model.xml", date_time=(1980, 1, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(zi, xml)
print(f"{out_path}: {counts['owned']} owned, {counts['base']} smart-ra reference copies, "
      f"{counts['dth']} dth-phc reference copies, views {[v.get('name') for v in views]}")
