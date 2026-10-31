#!/usr/bin/env python3
"""Seed and materialize folio/dth-sfp/ from who-iris/library/9789240120747-eng and DAK specifications."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L1_DIR = ROOT / "who-iris" / "library" / "9789240120747-eng"
SEC_DIR = L1_DIR / "sections"
FOLIO_DIR = ROOT / "folio" / "dth-sfp"
MEDIA_DIR = FOLIO_DIR / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Copy 6 vector figures from L1 into folio/dth-sfp/media/
for fig_png in sorted((L1_DIR / "media" / "figures").glob("*.png")):
    shutil.copy2(fig_png, MEDIA_DIR / fig_png.name)

SFP_NS = "https://litlfred.github.io/dth-sfp/v0/ns#glossary/dth-sfp/"
RA_NS = "https://litlfred.github.io/smart-ra/v0/ns#glossary/dpi-h-ra/"
SC_NS = "https://litlfred.github.io/dth-sc/v0/ns#glossary/dth-sc/"
PC_NS = "https://litlfred.github.io/dth-pc/v0/ns#glossary/dth-pc/"
HRH_NS = "https://litlfred.github.io/dth-hrh/v0/ns#glossary/dth-hrh/"
ARCH_EL = "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.1/elements/"
ARCH_VW = "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.1/views/"

def g(ns: str, term: str) -> dict:
    return {"iri": f"{ns}{term}", "term": term}

def el(eid: str, name: str, etype: str) -> dict:
    return {"iri": f"{ARCH_EL}{eid}.jsonld", "name": name, "type": etype}

def vw(vid: str, name: str) -> dict:
    return {"iri": f"{ARCH_VW}{vid}.jsonld", "name": name}

EL_NMRA = el("id-8e67c8e9e1195cdc857b03a2c640e7fe", "National Regulatory Authority", "BusinessRole")
EL_REG_SYS = el("id-22eff58eae365a4f8d0e0368d8c3497e", "Regulatory Systems", "ApplicationComponent")
EL_QUAL_SYS = el("id-1555c26cfbcd57f49b6e63fed8491d80", "Quality Systems", "ApplicationComponent")
EL_GLOB_PLAT = el("id-e3c4f0ec36f35eccb0d4c50f887316e5", "Global Platforms", "ApplicationComponent")
EL_PROD_REG = el("id-59c26d672a4248e0bb83cf4d26cba10c", "Product Registry", "ApplicationComponent")
EL_NPC = el("id-ed45b0d35d7c5ccbbf4abe599a80be5c", "National Product Catalogue", "ApplicationComponent")
EL_PROD_VER = el("id-975c5567001151299672c0341a733111", "Product Verification", "ApplicationService")
EL_TRACK_TRACE = el("id-bc68171ed2615dad80e6f7d8199f4057", "Track and Trace", "ApplicationService")
EL_TRACEABILITY = el("id-e88f6d077d31407bb1af5f2ecfd3b48a", "Traceability", "Capability")
EL_RECALL = el("id-a9c92f8fa2924d4180e8f5512b0d0097", "Recall", "Capability")
EL_TRACE_EVT = el("id-5dc77dae1bce5d11b288830795b31bdf", "Traceability Event", "DataObject")
EL_HWR = el("id-350840520ae44f658b6ad3b3762e382e", "DPI-H Health Workforce Registry (HWR)", "ApplicationComponent")
EL_FAC_REG = el("id-4e0767822dcf46409554156a133fbc67", "DPI-H: Facility Registry", "ApplicationComponent")
EL_TERM_SVC = el("id-3f41de2b51c24041b08243bf72b140d1", "Terminology Service", "ApplicationComponent")
EL_INFO_MED = el("id-3c5d846710034c4595e206e748d65e36", "DPI-F Information Mediator", "ApplicationComponent")
EL_SEC_CONSENT = el("id-d79aa0eec0584b0792b44bca408afeb6", "DPI-F Security & Consent Module", "ApplicationComponent")
EL_NOTIF = el("id-6b78a242e71a428c87434e2fe5891ee2", "Update Subscription/Notification", "ApplicationComponent")
EL_REP_MOD = el("id-bbd18f65be45490fbbaf02346511ae5e", "Reporting Module", "ApplicationComponent")
EL_ANALYTICS = el("id-3fd92d497ca040c8a436f355c0b68770", "Analytics & Reporting Platform", "ApplicationComponent")
EL_HF = el("id-9cecae7a982548e1960a36ed41713a7c", "Health Facility", "BusinessRole")
EL_CH = el("id-2bdc635e575f5ec59bb5d6cbff12de78", "Community Health", "BusinessRole")
EL_IND = el("id-03e28af10b8f5b099e271461c8a99f21", "Individual", "BusinessRole")
EL_MFG = el("id-66d0f91175c154b48413d57e9f952a34", "Manufacturer / Distributor", "BusinessRole")
EL_SUP = el("id-895960beffc24849a375a9950ff551c7", "Supplier", "BusinessRole")

VW_DHSC = vw("id-92267636cc42566ca5d2cff0e81be8c9", "DHSC Architecture Framework (DTH SC Fig. 14)")
VW_TT = vw("id-bea56e01c8345fbc803dee47a17ccfd3", "Track and Trace through DHSC Components (DTH SC Fig. 24)")
VW_PARTNERS = vw("id-2d524cffba25509e82684f47d624cc42", "Health Supply Chain Partners and Processes (DTH SC Figs. 1-3)")
VW_PMD = vw("id-053fa0e33f6b5b0bb218195486c05160", "Product Master Data Information Model (DTH PC Figs. 8-9)")
VW_NPC = vw("id-02175c6feb9155618981ff120f954420", "National Product Catalogue (DTH PC Fig. 2, Ch. 2-3)")
VW_INTEROP = vw("id-8c5dd12b8d4e425184f6003d0513d569", "Interoperability Layer")
VW_COMP = vw("id-3ad41900b17d47f78129e16d32ed2f38", "Components")
VW_CAP = vw("id-4e6e25746e8d4398add06fcbc4fb5a4e", "Capabilities-Goals")
VW_HW = vw("id-19be800d18a34a618d6e1955cf58e956", "ALL High Level - Health Workforce")

CHAPTER_MAP = {
    "sec-front-matter": "00-front-matter",
    "sec-000": "00-front-matter",
    "sec-001": "00-front-matter",
    "sec-002": "00-front-matter",
    "sec-003": "00-introduction",
    "sec-004": "00-introduction",
    "sec-005": "00-introduction",
    "sec-006": "00-introduction",
    "sec-007": "00-introduction",
    "sec-008": "ch01-assess-current-state",
    "sec-009": "ch01-assess-current-state",
    "sec-010": "ch01-assess-current-state",
    "sec-011": "ch01-assess-current-state",
    "sec-012": "ch02-shared-understanding-governance",
    "sec-013": "ch02-shared-understanding-governance",
    "sec-014": "ch02-shared-understanding-governance",
    "sec-015": "ch02-shared-understanding-governance",
    "sec-016": "ch02-shared-understanding-governance",
    "sec-017": "ch02-shared-understanding-governance",
    "sec-018": "ch03-future-state",
    "sec-019": "ch03-future-state",
    "sec-020": "ch03-future-state",
    "sec-021": "ch04-determine-requirements",
    "sec-022": "ch04-determine-requirements",
    "sec-023": "ch04-determine-requirements",
    "sec-024": "ch04-determine-requirements",
    "sec-025": "ch04-determine-requirements",
    "sec-026": "ch04-determine-requirements",
    "sec-027": "ch05-plan-implementation",
    "sec-028": "ch06-monitor-evaluate-scale",
    "sec-029": "ch06-monitor-evaluate-scale",
    "sec-030": "ch06-monitor-evaluate-scale",
    "sec-031": "ch07-share-experiences",
    "sec-032": "references-resources",
    "sec-033": "references-resources",
    "sec-034": "annexes",
    "sec-035": "annexes",
    "sec-036": "annexes",
    "sec-037": "annexes",
    "sec-038": "annexes",
    "sec-039": "annexes",
    "sec-040": "annexes",
    "sec-041": "annexes",
}

FINDINGS_BY_SEC = {
    "sec-002": [
        "F1: Two definitions of 'substandard medical product' — Glossary (p. ix, citing ref 9) states 'authorized by national regulatory authorities, but fail to meet either national or international quality standards or specifications – or, in some cases, both', whereas Introduction (p. 1, citing ref 23 WHA70/A70/23) states 'fail to meet either their quality standards or their specifications, or both'. Both are preserved as alternatives.",
        "F3 (Polypharmacy orphan glossary entry): 'Polypharmacy' is defined on p. viii (citing ref 16) but never used in the handbook body text (pp. 1-59).",
        "F6: Glossary entry for 'Registry' (p. viii) is truncated mid-sentence ('...canonical minimum data etc.').",
        "F9 & F10: Term comparison with smart-ra (dpi-h-ra) recorded — 'enterprise architecture', 'interoperability', 'product' (ArchiMate business offering vs physical medical product homonym), and 'SMART Guidelines' carry distinct wordings across smart-ra and dth-sfp.",
    ],
    "sec-004": [
        "F1: Introduction (p. 1, citing WHA70/A70/23 ref 23) defines substandard medical products as 'authorized medical products that fail to meet either their quality standards or their specifications, or both' — preserved alongside the Glossary p. ix wording.",
    ],
    "sec-017": [
        "F7: End-of-chapter checklist copy-paste defect — Chapter 2's checklist (p. 17 / PDF p. 29) asks 'Has a comprehensive current state analysis been conducted?' (copied from Chapter 1).",
    ],
    "sec-020": [
        "F7: End-of-chapter checklist copy-paste defect — Chapter 3's checklist (p. 21 / PDF p. 33) repeats 'Has a comprehensive current state analysis been conducted?' from Chapter 1.",
    ],
    "sec-022": [
        "F3: Persona lists disagree across the handbook — §4.1 (p. 25) names 6 professions (doctor, nurse, pharmacist, pharmacy technician, dentist, public health worker); Table 7 (pp. 25-26) lists 3 (Doctor, Nurse, Individual/Patient); Table 8 (p. 26) lists 3 (CHW, Laboratory technician, Pharmacist); Table 9 (pp. 27-28) has 9 scenarios (adding Midwife and Paramedic); Annex 2 (p. 53) adds Veterinarians. All 12 reporting personas plus 3 regulatory/supply-chain/governance roles are unioned in SFP-R-01..SFP-R-15.",
    ],
    "sec-023": [
        "F3: Table 9 (pp. 27-28) includes 9 user scenarios (Doctor, Nurse, Individual/Patient, CHW, Lab Technician, Pharmacist, Dentist, Midwife, Paramedic), adding Midwife and Paramedic beyond §4.1 and Tables 7-8.",
    ],
    "sec-024": [
        "F2: Report type in Fig. 4 (p. 30) omits 'unregistered/unlicensed medical products' (the third WHO SF category defined on p. ix and p. 1), offering only substandard and falsified branches.",
        "F5: Fig. 4 (p. 30 / PDF p. 42) has 5 BPMN 2.0 defects: (1) step 2 repeats gateway 1 ('Is the product registered?'); (2) gateway 1 has an unlabelled bypass arrow to the end event; (3) gateway 5 is labelled 'Select type of report' (imperative task label) rather than a question; (4) step numbers 6, 7, 8 repeat on both parallel paths; (5) symbol usage violates Annex 3 rules. Redrawn cleanly in processes/SF-REP-001.bpmn while keeping Fig. 4 as the cited L1 figure.",
    ],
    "sec-025": [
        "F2: Data element SFR.A1.DE8 ('Type of report', Table 11, p. 31) describes substandard/falsified reporting channels and omits unregistered/unlicensed medical products.",
        "F4: Missing definitions in Table 11 (p. 31) — SFR.A1.DE2 ('Type of report') and SFR.A1.DE5 ('Type of product') have empty Description and Data type cells, and SFR.A1.DE8 duplicates the label 'Type of report'.",
    ],
    "sec-026": [
        "F4: Missing requirement IDs in Tables 12 and 13 (pp. 31-35) — only 2 of 7 functional requirements (SFR.FXNREQ.001, SFR.FXNREQ.002) and 2 of 78 non-functional requirements (SFR.NFXNREQ.001, SFR.NFXNREQ.010) carry IDs in the source; stable IDs are assigned and flagged as assigned in the L2 blocks.",
        "F7: End-of-chapter checklist copy-paste defect — Chapter 4's checklist (p. 35 / PDF p. 47) repeats 'Has a comprehensive current state analysis been conducted?' from Chapter 1.",
        "F8: Undefined reference in Table 13 Interoperability category (p. 32 / PDF p. 44) — row 5 cites 'workstream 3 content (CQL + FHIR resources)', which is never defined in the handbook.",
    ],
    "sec-036": [
        "F3: Annex 2 user persona template (p. 53 / PDF p. 65) adds 'veterinarians' to the health care worker list, which does not appear in §4.1 or Tables 7-9.",
    ],
}

def section_glossary_and_archimate(sec_id: str) -> tuple[list[dict], dict]:
    glos = [g(SFP_NS, "sf-report"), g(SFP_NS, "suspect-product")]
    els = [EL_NMRA, EL_REG_SYS]
    vws = [VW_DHSC, VW_COMP]

    if sec_id in ("sec-front-matter", "sec-000", "sec-001", "sec-002"):
        glos += [
            g(SFP_NS, "substandard-medical-product"),
            g(SFP_NS, "falsified-medical-product"),
            g(SFP_NS, "unregistered-or-unlicensed-medical-product"),
            g(SFP_NS, "medical-product"),
            g(SFP_NS, "pharmacovigilance"),
            g(SFP_NS, "active-pharmacovigilance"),
            g(SFP_NS, "passive-pharmacovigilance"),
            g(SFP_NS, "adverse-drug-reaction"),
            g(SFP_NS, "post-market-surveillance"),
            g(SFP_NS, "risk-based-post-market-surveillance"),
            g(SFP_NS, "global-surveillance-and-monitoring-system"),
            g(SFP_NS, "member-state-mechanism"),
            g(SFP_NS, "national-medicines-regulatory-authority"),
            g(SFP_NS, "polypharmacy"),
            g(RA_NS, "enterprise-architecture"),
            g(RA_NS, "interoperability"),
            g(RA_NS, "registry"),
            g(RA_NS, "smart-guidelines"),
            g(PC_NS, "product-master-data"),
            g(SC_NS, "traceability"),
        ]
        els += [EL_GLOB_PLAT, EL_NPC]
        vws += [VW_NPC, VW_INTEROP]
    elif sec_id in ("sec-003", "sec-004", "sec-005", "sec-006", "sec-007"):
        glos += [
            g(SFP_NS, "substandard-medical-product"),
            g(SFP_NS, "falsified-medical-product"),
            g(SFP_NS, "unregistered-or-unlicensed-medical-product"),
            g(SFP_NS, "therapeutic-failure"),
            g(SFP_NS, "medical-product-alert"),
            g(SFP_NS, "global-surveillance-and-monitoring-system"),
            g(RA_NS, "smart-guidelines"),
            g(RA_NS, "digital-transformation"),
            g(SC_NS, "recall" if False else "traceability"),
        ]
        els += [EL_RECALL, EL_GLOB_PLAT]
        vws += [VW_CAP]
    elif sec_id in ("sec-008", "sec-009", "sec-010", "sec-011"):
        glos += [
            g(SFP_NS, "enabling-environment"),
            g(SFP_NS, "pharmacovigilance"),
            g(SFP_NS, "reporter-feedback-loop"),
            g(SFP_NS, "anonymous-report"),
            g(RA_NS, "stakeholder"),
            g(RA_NS, "digital-infrastructure"),
            g(SC_NS, "health-supply-chain-information-system"),
        ]
        els += [EL_QUAL_SYS, EL_GLOB_PLAT]
        vws += [VW_PARTNERS]
    elif sec_id in ("sec-012", "sec-013", "sec-014", "sec-015", "sec-016", "sec-017"):
        glos += [
            g(SFP_NS, "national-medicines-regulatory-authority"),
            g(SFP_NS, "detection-to-notification-time"),
            g(RA_NS, "governance"),
            g(RA_NS, "goal"),
            g(SC_NS, "governance-health-supply-chain"),
            g(HRH_NS, "regulation"),
        ]
        els += [EL_RECALL, EL_TRACEABILITY]
        vws += [VW_CAP]
    elif sec_id in ("sec-018", "sec-019", "sec-020"):
        glos += [
            g(RA_NS, "enterprise-architecture"),
            g(RA_NS, "interoperability"),
            g(RA_NS, "point-of-service-applications"),
            g(RA_NS, "registry"),
            g(PC_NS, "national-product-catalogue"),
            g(SC_NS, "traceability"),
            g(HRH_NS, "health-workforce-registry"),
        ]
        els += [EL_NPC, EL_PROD_REG, EL_FAC_REG, EL_HWR, EL_TERM_SVC, EL_INFO_MED, EL_SEC_CONSENT]
        vws += [VW_INTEROP, VW_NPC, VW_TT]
    elif sec_id in ("sec-021", "sec-022", "sec-023", "sec-024", "sec-025", "sec-026"):
        glos += [
            g(SFP_NS, "reporter"),
            g(SFP_NS, "report-type"),
            g(SFP_NS, "tracking-number"),
            g(SFP_NS, "reporter-feedback-loop"),
            g(SFP_NS, "anonymous-report"),
            g(RA_NS, "user-persona"),
            g(RA_NS, "business-process"),
            g(RA_NS, "workflow"),
            g(RA_NS, "data-element"),
            g(RA_NS, "functional-requirements"),
            g(RA_NS, "non-functional-requirements"),
            g(RA_NS, "snomed-gps"),
            g(PC_NS, "product-master-data"),
            g(PC_NS, "transactional-data"),
            g(SC_NS, "traceability"),
            g(HRH_NS, "occupation"),
            g(HRH_NS, "international-standard-classification-of-occupations"),
        ]
        els += [EL_NPC, EL_PROD_VER, EL_TRACK_TRACE, EL_TRACE_EVT, EL_NOTIF, EL_SEC_CONSENT, EL_HF, EL_CH, EL_IND, EL_MFG]
        vws += [VW_PMD, VW_TT, VW_HW]
    elif sec_id in ("sec-027",):
        glos += [
            g(RA_NS, "open-source"),
            g(RA_NS, "open-standards"),
            g(RA_NS, "total-cost-of-ownership"),
            g(RA_NS, "deploy"),
        ]
        els += [EL_REP_MOD]
    elif sec_id in ("sec-028", "sec-029", "sec-030"):
        glos += [
            g(SFP_NS, "monitoring"),
            g(SFP_NS, "evaluation"),
            g(SFP_NS, "detection-to-notification-time"),
            g(RA_NS, "user-acceptance-testing"),
            g(RA_NS, "outcome"),
        ]
        els += [EL_ANALYTICS, EL_REP_MOD]
        vws += [VW_CAP]
    elif sec_id in ("sec-031",):
        glos += [
            g(SFP_NS, "reporter-feedback-loop"),
            g(SFP_NS, "global-surveillance-and-monitoring-system"),
        ]
        els += [EL_REP_MOD, EL_GLOB_PLAT]
    else:
        glos += [
            g(RA_NS, "business-process"),
            g(RA_NS, "user-persona"),
            g(RA_NS, "stakeholder"),
        ]

    # Deduplicate glossary by iri
    seen_g = set()
    dedup_g = []
    for item in glos:
        if item["iri"] not in seen_g:
            seen_g.add(item["iri"])
            dedup_g.append(item)

    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": els,
        "views": vws,
    }
    return dedup_g, arch

def write_block(chapter_dir: Path, filename: str, builder: str, builder_import: str, label: str, title: str, md_body: str, meta: dict, extra_ts_fields: str = "", uses: list[str] | None = None):
    if uses:
        dak_refs = [u for u in uses if u.startswith(("pers:", "bp:", "dt:", "scen:", "de:", "freq:", "nfreq:", "ind:"))]
        if dak_refs:
            meta = dict(meta)
            meta["relatedBlocks"] = dak_refs
        uses = [u for u in uses if not u.startswith(("pers:", "bp:", "dt:", "scen:", "de:", "freq:", "nfreq:", "ind:"))]
    chapter_dir.mkdir(parents=True, exist_ok=True)
    ts_path = chapter_dir / f"{filename}.ts"
    md_path = chapter_dir / f"{filename}.md"
    uses_line = f"  uses: {json.dumps(uses)},\n" if uses else ""
    meta_json = json.dumps(meta, ensure_ascii=False)
    ts_content = (
        f'import {{ {builder} }} from "../../schema/{builder_import}";\n\n'
        f"export default {builder}({{\n"
        f'  label: {json.dumps(label)},\n'
        f'  title: {json.dumps(title)},\n'
        f"{extra_ts_fields}"
        f"{uses_line}"
        f"  meta: {meta_json},\n"
        f"}});\n"
    )
    ts_path.write_text(ts_content)
    md_path.write_text(md_body.rstrip() + "\n")

# 1. Write all 43 L1 outline section prose blocks
for j_path in sorted(SEC_DIR.glob("*.jsonld")):
    sec_id = j_path.stem
    sec_meta = json.loads(j_path.read_text())
    md_files = sorted(SEC_DIR.glob(f"{sec_id}*.md"))
    md_file = md_files[0]
    raw_md = md_file.read_text()
    chapter = CHAPTER_MAP[sec_id]
    chapter_dir = FOLIO_DIR / chapter
    block_name = f"p-{sec_id}"
    label = f"prose:{sec_id}"
    title = f"{sec_meta.get('title', sec_id)} (PDF pp. {sec_meta.get('pageStart')}–{sec_meta.get('pageEnd')})"
    glos, arch = section_glossary_and_archimate(sec_id)
    findings = FINDINGS_BY_SEC.get(sec_id, [])

    md_out = raw_md
    if findings:
        callout = "\n\n> [!WARNING]\n> **Source Review Findings Recorded (`litlfred/dth-sfp#1` §3):**\n" + "\n".join(
            f"> - **{f}**" for f in findings
        ) + "\n"
        md_out = raw_md.rstrip() + callout

    meta = {
        "source": f"who-iris/library/9789240120747-eng/sections/{md_file.name}",
        "sectionId": sec_id,
        "pageStart": sec_meta.get("pageStart"),
        "pageEnd": sec_meta.get("pageEnd"),
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if findings:
        meta["reviewNotes"] = findings
    if sec_id == "sec-031":
        meta["sourceOnly"] = True

    write_block(chapter_dir, block_name, "prose", "builders", label, title, md_out, meta)

# 2. Write the 6 Figure blocks (f-fig-01 .. f-fig-06)
FIGURES = [
    ("00-introduction", "f-fig-01", "fig:fig-01", "Fig. 1. Planning and implementing a digital health enterprise: phases, steps and resources (p. 4 / PDF p. 16)", "media/diig-phases-sfp.svg", "sec-006", 16, "0.3.0-draft.1", "id-4e6e25746e8d4398add06fcbc4fb5a4e", "Capabilities-Goals", []),
    ("00-introduction", "f-fig-02", "fig:fig-02", "Fig. 2. WHO’s SMART Guidelines approach (p. 5 / PDF p. 17)", "media/fig-2-smart-guidelines-approach.svg", "sec-006", 17, "0.3.0-draft.1", "id-8c5dd12b8d4e425184f6003d0513d569", "Interoperability Layer", []),
    ("ch03-future-state", "f-fig-03", "fig:fig-03", "Fig. 3. Links to the enterprise architecture / DIIG national digital health architecture (p. 22 / PDF p. 34)", "vfig-p034.png", "sec-020", 34, "0.3.0-draft.1", "id-92267636cc42566ca5d2cff0e81be8c9", "DHSC Architecture Framework (DTH SC Fig. 14)", []),
    ("ch04-determine-requirements", "f-fig-04", "fig:fig-04", "Fig. 4. Workflow for reporting substandard and falsified medical products (L1 source diagram, p. 30 / PDF p. 42)", "vfig-p042.png", "sec-024", 42, "0.3.0-draft.1", "id-bea56e01c8345fbc803dee47a17ccfd3", "Track and Trace through DHSC Components (DTH SC Fig. 24)", [
        "F2: Fig. 4 omits the third WHO SF category ('unregistered/unlicensed medical products', p. ix & p. 1).",
        "F5: Fig. 4 contains 5 BPMN 2.0 defects (step 2 repeats gateway 1; gateway 1 has an unlabelled bypass to End; gateway 5 is labelled 'Select type of report' rather than a question; step numbers 6-8 repeat on both branches; symbols deviate from Annex 3). Preserved as the L1 source figure and redrawn cleanly in bp:sf-rep-001 (processes/SF-REP-001.bpmn).",
    ]),
    ("ch06-monitor-evaluate-scale", "f-fig-05", "fig:fig-05", "Fig. 5. Monitoring and evaluation across system maturity stages (p. 40 / PDF p. 52)", "vfig-p052.png", "sec-029", 52, "0.3.0-draft.1", "id-4e6e25746e8d4398add06fcbc4fb5a4e", "Capabilities-Goals", []),
    ("ch06-monitor-evaluate-scale", "f-fig-06", "fig:fig-06", "Fig. 6. Digital health maturity continuum and M&E focus (p. 41 / PDF p. 53)", "vfig-p053.png", "sec-029", 53, "0.3.0-draft.1", "id-4e6e25746e8d4398add06fcbc4fb5a4e", "Capabilities-Goals", []),
]

for ch, fname, flabel, ftitle, png_name, sec_id, pdf_p, model_id, view_id, view_name, rnotes in FIGURES:
    glos, arch = section_glossary_and_archimate(sec_id)
    arch = dict(arch)
    fig_rel = png_name if png_name.startswith("media/") else f"media/{png_name}"
    arch["figures"] = [{"figure": fig_rel, "model": model_id, "view": view_id, "viewName": view_name}]
    if fname == "f-fig-01":
        md = (
            f"![{ftitle}](media/diig-phases-sfp.svg)\n\n"
            f"*Source: adapted from WHO Digital transformation handbook for health product catalogue, 2025, Fig. 4, itself adapted from the 2020 WHO Digital implementation investment guide (DIIG), Fig. 1.1.1 (`who-iris/library/9789240120747-eng/figures/vfig-p016.png`, PDF page {pdf_p}). Generated by the `diig-phases-svg` tool from the who-iris data for the product catalogue figure and this handbook\x27s adaptation file (`figure-data/diig-phases-sfp.json`); this handbook is added in Phase 07 and marked \"(this document)\" in place of the product catalogue handbook. Mapped to `dpi-h-ra` ArchiMate view `{view_name}` (`{view_id}`).*\n"
        )
        source_val = {
            "library": "9789240120747-eng",
            "file": "who-iris/library/9789240120747-eng/figures/vfig-p016.png",
            "page": pdf_p,
            "method": "generated",
            "citation": "WHO. Digital transformation handbook for reporting substandard and falsified medical products. 2025. Fig. 1, adapted from WHO Digital transformation handbook for health product catalogue, 2025, Fig. 4, and WHO Digital implementation investment guide (DIIG), 2020, Fig. 1.1.1",
            "issue": "litlfred/dth-sfp#1",
            "generated": {
                "adaptation": "figure-data/diig-phases-sfp.json",
                "repo": "https://github.com/litlfred/who-iris",
                "commit": "5191f142a828bbe2f4d010dbe0d651513444da63",
                "data": "https://github.com/litlfred/who-iris/blob/5191f142a828bbe2f4d010dbe0d651513444da63/library/9789240116191-eng/figure-data/fig-4-diig-phases.json",
                "generator": "https://github.com/litlfred/folio-assistant-core/blob/4bfeb957292b6478bd54ba05b807a5b475ac3b93/scripts/diig-phases-svg.ts",
                "tool": "diig-phases-svg",
                "pr": [
                    "https://github.com/litlfred/who-iris/pull/149",
                    "https://github.com/litlfred/folio-assistant-core/pull/405"
                ],
                "output": "diig-phases-sfp.svg"
            }
        }
        extra_props = f'  file: {json.dumps(png_name)},\n  page: {pdf_p},\n'
    elif fname == "f-fig-02":
        md = (
            f"![{ftitle}](media/fig-2-smart-guidelines-approach.svg)\n\n"
            f"*Source: WHO, Digital transformation handbook for reporting substandard and falsified medical products, 2025, Fig. 2 (`who-iris/library/9789240120747-eng/figures/vfig-p017.png`, PDF page {pdf_p}), adapted from WHO SMART Guidelines (Mehl et al., 2021). Generated by the `smart-approach-svg` tool from the who-iris SMART Guidelines approach figure data (`who-iris/library/9789240116191-eng/figure-data/fig-5-smart-guidelines-approach.json`). Mapped to `dpi-h-ra` ArchiMate view `{view_name}` (`{view_id}`).*\n"
        )
        source_val = {
            "library": "9789240120747-eng",
            "file": "who-iris/library/9789240120747-eng/figures/vfig-p017.png",
            "page": pdf_p,
            "method": "generated",
            "citation": "WHO. Digital transformation handbook for reporting substandard and falsified medical products. 2025. Fig. 2, adapted from WHO SMART Guidelines (Mehl et al., 2021)",
            "issue": "litlfred/dth-sfp#1",
            "generated": {
                "repo": "https://github.com/litlfred/who-iris",
                "commit": "3ecd60367222d7cc8eb0960061bcc06eb7a985dd",
                "data": "https://github.com/litlfred/who-iris/blob/3ecd60367222d7cc8eb0960061bcc06eb7a985dd/library/9789240116191-eng/figure-data/fig-5-smart-guidelines-approach.json",
                "generator": "https://github.com/litlfred/folio-assistant-core/blob/aeef4ea569c25cff8649d7365e69554eadab6027/scripts/smart-approach-svg.ts",
                "tool": "smart-approach-svg",
                "pr": [
                    "https://github.com/litlfred/who-iris/pull/149",
                    "https://github.com/litlfred/folio-assistant-core/pull/405"
                ],
                "output": "fig-2-smart-guidelines-approach.svg"
            }
        }
        extra_props = f'  file: {json.dumps(png_name)},\n  page: {pdf_p},\n'
    else:
        md = f"![{ftitle}](../media/{png_name})\n\n*Source: `who-iris/library/9789240120747-eng/media/figures/{png_name}` (PDF page {pdf_p}). Mapped to `dpi-h-ra` ArchiMate view `{view_name}` (`{view_id}`).*\n"
        source_val = f"who-iris/library/9789240120747-eng/media/figures/{png_name}"
        extra_props = f'  file: {json.dumps(png_name)},\n'
    if rnotes:
        md += "\n> [!WARNING]\n> **Source Figure Review Findings (`litlfred/dth-sfp#1` §3):**\n" + "\n".join(f"> - **{n}**" for n in rnotes) + "\n"
    meta = {
        "source": source_val,
        "pdfPage": pdf_p,
        "figureFile": fig_rel,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    write_block(FOLIO_DIR / ch, fname, "figure", "builders", flabel, ftitle, md, meta, extra_props, uses=[f"prose:{sec_id}"])

# 3. Helper to extract markdown tables from a section file
def extract_tables(sec_prefix: str) -> list[str]:
    md_file = sorted(SEC_DIR.glob(f"{sec_prefix}*.md"))[0]
    txt = md_file.read_text()
    return re.findall(r"(?:^\|.*\|\n)+", txt, re.M)

TABLE_SPECS = [
    ("00-front-matter", "t-abbreviations", "tbl:abbreviations", "Abbreviations and acronyms (19 entries, p. vi / PDF p. 8)", "sec-001", 0, 8, []),
    ("00-front-matter", "t-glossary", "tbl:glossary", "Handbook Glossary (35 entries, pp. vii–ix / PDF pp. 9–11)", "sec-002", 0, 9, FINDINGS_BY_SEC["sec-002"]),
    ("00-introduction", "t-table-01", "tbl:table-01", "Table 1. Target audience and how to use this handbook (p. 2 / PDF p. 14)", "sec-005", 0, 14, []),
    ("ch01-assess-current-state", "t-table-02", "tbl:table-02", "Table 2. Stakeholder analysis for SF medical product reporting (p. 9 / PDF p. 21)", "sec-009", 0, 21, []),
    ("ch01-assess-current-state", "t-table-03", "tbl:table-03", "Table 3. Assessing digital readiness and enabling environment (p. 11 / PDF p. 23)", "sec-010", 0, 23, []),
    ("ch01-assess-current-state", "t-table-04", "tbl:table-04", "Table 4. Questions for assessing current SF and PV reporting practices (p. 12 / PDF p. 24)", "sec-011", 0, 24, []),
    ("ch01-assess-current-state", "t-table-05", "tbl:table-05", "Table 5. Common barriers to reporting SF medical products and potential digital solutions (pp. 12–13 / PDF pp. 24–25)", "sec-011", 1, 24, []),
    ("ch03-future-state", "t-table-06", "tbl:table-06", "Table 6. Short-, medium- and long-term milestones for an SF reporting system (p. 20 / PDF p. 32)", "sec-019", 0, 32, []),
    ("ch04-determine-requirements", "t-table-07", "tbl:table-07", "Table 7. Examples of user personas: Doctor, Nurse, and Individual (pp. 25–26 / PDF pp. 37–38)", "sec-022", 0, 37, FINDINGS_BY_SEC["sec-022"]),
    ("ch04-determine-requirements", "t-table-08", "tbl:table-08", "Table 8. Additional user personas: Community health worker, Laboratory technician, and Pharmacist (p. 26 / PDF p. 38)", "sec-022", 1, 38, FINDINGS_BY_SEC["sec-022"]),
    ("ch04-determine-requirements", "t-table-09", "tbl:table-09", "Table 9. User scenarios across 9 reporting personas and 6 workflow stages (pp. 27–28 / PDF pp. 39–40)", "sec-023", 0, 39, FINDINGS_BY_SEC["sec-023"]),
    ("ch04-determine-requirements", "t-table-10", "tbl:table-10", "Table 10. Business process matrix SF-REP-001 (p. 29 / PDF p. 41)", "sec-024", 0, 41, FINDINGS_BY_SEC["sec-024"]),
    ("ch04-determine-requirements", "t-table-11", "tbl:table-11", "Table 11. Core data dictionary for SF medical product reporting (SFR.A1.DE1–DE10, p. 31 / PDF p. 43)", "sec-025", 0, 43, FINDINGS_BY_SEC["sec-025"]),
    ("ch04-determine-requirements", "t-table-12", "tbl:table-12", "Table 12. Functional requirements for an SF reporting system (SFR.FXNREQ.001–007, p. 31 / PDF p. 43)", "sec-026", 0, 43, FINDINGS_BY_SEC["sec-026"]),
    ("ch04-determine-requirements", "t-table-13", "tbl:table-13", "Table 13. Non-functional requirements across 11 categories (pp. 32–35 / PDF pp. 44–47)", "sec-026", 1, 44, FINDINGS_BY_SEC["sec-026"]),
    ("ch05-plan-implementation", "t-table-14", "tbl:table-14", "Table 14. Key implementation planning steps and considerations (p. 37 / PDF p. 49)", "sec-027", 0, 49, []),
    ("ch05-plan-implementation", "t-table-15", "tbl:table-15", "Table 15. Software development and procurement options (p. 38 / PDF p. 50)", "sec-027", 1, 50, []),
    ("ch06-monitor-evaluate-scale", "t-table-16", "tbl:table-16", "Table 16. Illustrative evaluation questions for an SF reporting system (p. 42 / PDF p. 54)", "sec-029", 1, 54, []),
    ("ch06-monitor-evaluate-scale", "t-table-17", "tbl:table-17", "Table 17. Key steps for developing an M&E plan (p. 43 / PDF p. 55)", "sec-029", 2, 55, []),
    ("ch06-monitor-evaluate-scale", "t-table-18", "tbl:table-18", "Table 18. M&E measures across Quality, Fidelity, Stability, Functionality and Investment (p. 44 / PDF p. 56)", "sec-029", 3, 56, []),
    ("annexes", "t-annex-01", "tbl:annex-01", "Annex 1. Principles for Digital Development applied to SF reporting (p. 52 / PDF p. 64)", "sec-035", 0, 64, []),
    ("annexes", "t-annex-02", "tbl:annex-02", "Annex 2. User persona template (p. 53 / PDF p. 65)", "sec-036", 0, 65, FINDINGS_BY_SEC["sec-036"]),
    ("annexes", "t-annex-03", "tbl:annex-03", "Annex 3. Business Process Model and Notation (BPMN) symbols (pp. 54–55 / PDF pp. 66–67)", "sec-037", 0, 66, []),
    ("annexes", "t-annex-04", "tbl:annex-04", "Annex 4. Stakeholder RACI matrix template (p. 56 / PDF p. 68)", "sec-038", 0, 68, []),
    ("annexes", "t-annex-05", "tbl:annex-05", "Annex 5. Template for assessing current software applications (p. 57 / PDF p. 69)", "sec-039", 0, 69, []),
    ("annexes", "t-annex-06", "tbl:annex-06", "Annex 6. Barriers to reporting mapping template (p. 58 / PDF p. 70)", "sec-040", 0, 70, []),
    ("annexes", "t-annex-07", "tbl:annex-07", "Annex 7. Risk management template (p. 59 / PDF p. 71)", "sec-041", 0, 71, []),
]

for ch, tname, tlabel, ttitle, sec_id, tbl_idx, pdf_p, rnotes in TABLE_SPECS:
    tbls = extract_tables(sec_id)
    tbl_md = tbls[tbl_idx] if tbl_idx < len(tbls) else tbls[-1]
    glos, arch = section_glossary_and_archimate(sec_id)
    md = f"### {ttitle}\n\n{tbl_md}"
    if rnotes:
        md += "\n> [!NOTE]\n> **Source Table Review Notes (`litlfred/dth-sfp#1` §3):**\n" + "\n".join(f"> - {n}" for n in rnotes) + "\n"
    meta = {
        "source": f"who-iris/library/9789240120747-eng/sections/{sorted(SEC_DIR.glob(f'{sec_id}*.md'))[0].name}",
        "pdfPage": pdf_p,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    write_block(FOLIO_DIR / ch, tname, "table", "builders", tlabel, ttitle, md, meta, uses=[f"prose:{sec_id}"])

# 4. Step P6a: 15 DAK Persona blocks (pers-sfp-r-01 .. pers-sfp-r-15)
PERSONAS = [
    ("01", "Doctor", "2211, 2212", "doctor", "human", EL_HF, ["sec-022", "sec-023"], [37, 39], "Generalist or specialist medical practitioner (Table 7, p. 25; Table 9 scenario 1, p. 27) who diagnoses patients, prescribes or administers medical products, and reports suspected SF products when encountering unexpected adverse reactions or therapeutic failure.", []),
    ("02", "Nurse", "2221", "nurse", "human", EL_HF, ["sec-022", "sec-023"], [37, 39], "Nursing professional (Table 7, p. 25; Table 9 scenario 2, p. 27) who prepares and administers medicines at the point of care, monitors patient responses, and reports suspected SF products when observing physical defects or adverse events.", []),
    ("03", "Individual / Patient", "N/A", "individual-patient", "human", EL_IND, ["sec-022", "sec-023"], [38, 39], "Patient, caregiver, or member of the public (Table 7, p. 26; Table 9 scenario 3, p. 27) who purchases or consumes a medical product and reports abnormal appearance, packaging, taste, lack of effect, or adverse reactions.", []),
    ("04", "Community Health Worker", "3253 (Table 8 lists 3259)", "community-health-worker", "human", EL_CH, ["sec-022", "sec-023"], [38, 39], "Community health worker (Table 8, p. 26; Table 9 scenario 4, p. 27) delivering primary care and health commodities in community outreach settings who detects and reports suspected SF products.", []),
    ("05", "Laboratory Technician", "3212", "laboratory-technician", "human", EL_HF, ["sec-022", "sec-023"], [38, 39], "Medical or quality-control laboratory technician (Table 8, p. 26; Table 9 scenario 5, p. 27; SF-REP-003) who identifies suspect diagnostic reagents/kits or performs laboratory testing on reported SF samples.", []),
    ("06", "Pharmacist", "2262", "pharmacist", "human", EL_HF, ["sec-022", "sec-023"], [38, 40], "Community or hospital pharmacist (Table 8, p. 26; Table 9 scenario 6, p. 28) who inspects stock, verifies packaging/batch/expiry, dispenses medicines, and reports suspected SF medical products.", []),
    ("07", "Dentist", "2261", "dentist", "human", EL_HF, ["sec-022", "sec-023"], [37, 40], "Dental practitioner (§4.1, p. 25; Table 9 scenario 7, p. 28) who administers dental anaesthetics and medicines and reports suspected SF dental products.", ["F3: Listed in §4.1 and Table 9 scenario 7, omitted from Tables 7–8."]),
    ("08", "Midwife", "2222", "midwife", "human", EL_HF, ["sec-023"], [40], "Midwifery professional (Table 9 scenario 8, p. 28) providing maternal and newborn care who detects and reports suspected SF uterotonics, antibiotics, or maternal health commodities.", ["F3: Present in Table 9 scenario 8, omitted from §4.1 and Tables 7–8."]),
    ("09", "Paramedic", "2240, 3258", "paramedic", "human", EL_CH, ["sec-023"], [40], "Emergency paramedical responder (Table 9 scenario 9, p. 28; SF-REP-006) who administers emergency medical products in field settings and submits SF reports online or via the offline outbox.", ["F3: Present in Table 9 scenario 9, omitted from §4.1 and Tables 7–8."]),
    ("10", "Pharmacy Technician", "3213", "pharmacy-technician", "human", EL_HF, ["sec-022"], [37], "Pharmaceutical technician or assistant (§4.1, p. 25) who receives, shelves, and prepares medical products in pharmacies/stores and reports suspected SF packaging or batch anomalies.", ["F3: Named in §4.1 (p. 25), omitted from Tables 7–9."]),
    ("11", "Public Health Worker", "2269", "public-health-worker", "human", EL_CH, ["sec-022"], [37], "Public health officer / programme worker (§4.1, p. 25) engaged in immunization, disease control, or field surveillance who detects and reports suspected SF medical products.", ["F3: Named in §4.1 (p. 25), omitted from Tables 7–9."]),
    ("12", "Veterinarian", "2250", "veterinarian", "human", EL_HF, ["sec-036"], [65], "Veterinary practitioner (Annex 2 user persona template, p. 53 / PDF p. 65) who prescribes or administers veterinary medicines and reports suspected SF veterinary products.", ["F3: Appears in Annex 2 template (p. 53), omitted from §4.1 and Tables 7–9."]),
    ("13", "NMRA Reviewer, Inspectorate & Case System", "2269 / Regulatory Authority", "national-medicines-regulatory-authority", "organisation-and-system", EL_NMRA, ["sec-015", "sec-024", "sec-026"], [28, 41, 43], "National medicines regulatory authority (NMRA) focal point, inspectorate, and SF case management system (Intro p. 1, §2.3 p. 16, Table 10 p. 29, Table 12 p. 31) responsible for receiving, acknowledging, investigating, and acting on SF reports.", []),
    ("14", "Pharmaceutical Manufacturer, Importer & Supply Chain Actor", "1321 / 3322", "suspect-product", "organisation", EL_MFG, ["sec-009", "sec-025"], [21, 43], "Authorized manufacturer, marketing authorization holder, importer, wholesaler, or distributor (Table 2 p. 9, SFR.A1.DE4 & DE8 Table 11 p. 31, SF-REP-004) who reports suspected counterfeit/falsified products or executes batch recalls.", []),
    ("15", "Governance, Law Enforcement, Customs & WHO GSMS Actor", "1112", "global-surveillance-and-monitoring-system", "organisation", EL_GLOB_PLAT, ["sec-014", "sec-015"], [28], "National steering committee, technical working group (TWG), advisory council, law enforcement/customs authorities, and WHO Global Surveillance and Monitoring System (GSMS) (§2.2–2.3 p. 16, SF-REP-004, SF-REP-005).", []),
]

BPMN_LANES_BY_NUM = {'01': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_HCP',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_Reporter',
         'processId': 'SF-REP-002'},
        {'bpmnFile': 'processes/SF-REP-003.bpmn',
         'laneId': 'Lane_SF_REP_003_Reporter',
         'processId': 'SF-REP-003'}],
 '02': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R02',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R02',
         'processId': 'SF-REP-002'},
        {'bpmnFile': 'processes/SF-REP-003.bpmn',
         'laneId': 'Lane_SF_REP_003_R02',
         'processId': 'SF-REP-003'}],
 '03': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R03',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R03',
         'processId': 'SF-REP-002'},
        {'bpmnFile': 'processes/SF-REP-003.bpmn',
         'laneId': 'Lane_SF_REP_003_R03',
         'processId': 'SF-REP-003'}],
 '04': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R04',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R04',
         'processId': 'SF-REP-002'},
        {'bpmnFile': 'processes/SF-REP-006.bpmn',
         'laneId': 'Lane_SF_REP_006_R04',
         'processId': 'SF-REP-006'}],
 '05': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R05',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-003.bpmn',
         'laneId': 'Lane_SF_REP_003_Lab',
         'processId': 'SF-REP-003'}],
 '06': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R06',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-004.bpmn',
         'laneId': 'Lane_SF_REP_004_R06',
         'processId': 'SF-REP-004'}],
 '07': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R07',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R07',
         'processId': 'SF-REP-002'}],
 '08': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R08',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R08',
         'processId': 'SF-REP-002'}],
 '09': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R09',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-006.bpmn',
         'laneId': 'Lane_SF_REP_006_Reporter',
         'processId': 'SF-REP-006'}],
 '10': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R10',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-004.bpmn',
         'laneId': 'Lane_SF_REP_004_R10',
         'processId': 'SF-REP-004'}],
 '11': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R11',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R11',
         'processId': 'SF-REP-002'}],
 '12': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R12',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_R12',
         'processId': 'SF-REP-002'}],
 '13': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_NMRA',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-002.bpmn',
         'laneId': 'Lane_SF_REP_002_NMRA',
         'processId': 'SF-REP-002'},
        {'bpmnFile': 'processes/SF-REP-003.bpmn',
         'laneId': 'Lane_SF_REP_003_NMRA',
         'processId': 'SF-REP-003'},
        {'bpmnFile': 'processes/SF-REP-004.bpmn',
         'laneId': 'Lane_SF_REP_004_NMRA',
         'processId': 'SF-REP-004'},
        {'bpmnFile': 'processes/SF-REP-005.bpmn',
         'laneId': 'Lane_SF_REP_005_NMRA',
         'processId': 'SF-REP-005'},
        {'bpmnFile': 'processes/SF-REP-006.bpmn',
         'laneId': 'Lane_SF_REP_006_App',
         'processId': 'SF-REP-006'}],
 '14': [{'bpmnFile': 'processes/SF-REP-001.bpmn',
         'laneId': 'Lane_SF_REP_001_R14',
         'processId': 'SF-REP-001'},
        {'bpmnFile': 'processes/SF-REP-004.bpmn',
         'laneId': 'Lane_SF_REP_004_SupplyChain',
         'processId': 'SF-REP-004'}],
 '15': [{'bpmnFile': 'processes/SF-REP-004.bpmn',
         'laneId': 'Lane_SF_REP_004_LawEnforcement',
         'processId': 'SF-REP-004'},
        {'bpmnFile': 'processes/SF-REP-005.bpmn',
         'laneId': 'Lane_SF_REP_005_GSMS',
         'processId': 'SF-REP-005'}]}

for num, pname, isco, gterm, ptype, arch_el, secs, pages, desc, rnotes in PERSONAS:
    pid = f"sfp-r-{num}"
    role_code = f"SFP-R-{num}"
    fname = f"pers-{pid}"
    label = f"pers:{pid}"
    title = f"{role_code} — {pname} (ISCO-08: {isco})"
    glos = [
        g(SFP_NS, gterm),
        g(SFP_NS, "reporter"),
        g(SFP_NS, "sf-report"),
        g(RA_NS, "user-persona"),
        g(HRH_NS, "occupation"),
        g(HRH_NS, "international-standard-classification-of-occupations"),
    ]
    if gterm == "community-health-worker":
        glos.append(g(HRH_NS, "community-health-workers"))
    elif ptype == "human" and isco != "N/A":
        glos.append(g(HRH_NS, "health-professional"))
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [arch_el, EL_NMRA],
        "views": [VW_HW, VW_PARTNERS],
    }
    md = (
        f"### {title}\n\n"
        f"- **Role ID:** `{role_code}` (`{label}`)\n"
        f"- **ISCO-08 Code(s):** `{isco}`\n"
        f"- **BPMN Resource ID:** `{label}`\n"
        f"- **ArchiMate Role / Actor:** `{arch_el['name']}` (`{arch_el['iri']}`)\n"
        f"- **L1 Source Sections:** `{', '.join(secs)}` (PDF pp. {', '.join(str(p) for p in pages)})\n\n"
        f"{desc}\n"
    )
    if rnotes:
        md += "\n> [!NOTE]\n> **Persona Coverage Note (`litlfred/dth-sfp#1` Finding F3):**\n" + "\n".join(f"> - {n}" for n in rnotes) + "\n"
    meta = {
        "roleId": role_code,
        "title": title,
        "isco08": isco,
        "personaType": ptype,
        "bpmnRoleId": label,
        "bpmnLanes": BPMN_LANES_BY_NUM[num],
        "source": f"who-iris/library/9789240120747-eng/sections/{sorted(SEC_DIR.glob(f'{secs[0]}*.md'))[0].name}",
        "sections": secs,
        "pdfPages": pages,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    write_block(FOLIO_DIR / "ch04-determine-requirements", fname, "persona", "dak", label, title, md, meta, uses=[f"prose:{s}" for s in secs] + ["tbl:table-07", "tbl:table-08"])

# 5. Step P6a: 9 DAK UserScenario blocks (us-sfp-scen-01 .. us-sfp-scen-09) from Table 9
SCENARIOS = [
    ("01", "Doctor", "pers:sfp-r-01", "doctor", 39, "Observes lack of therapeutic effect or unexpected adverse reaction in a treated patient.", "Opens the digital SF reporting app on clinic computer or mobile phone.", "Selects the medicine from the product catalogue or enters product name, batch number, and expiry date.", "Uploads photos of the medicine packaging, vial/blister, and label.", "Receives immediate confirmation message and unique report tracking number.", "Receives investigation updates from the NMRA and clinical guidance on affected batches."),
    ("02", "Nurse", "pers:sfp-r-02", "nurse", 39, "Notices discoloration, particulate matter, or defective seal while preparing an injectable or oral medication.", "Initiates an SF report on the ward tablet or mobile reporting application.", "Scans the barcode or enters product name, batch number, and expiry date.", "Takes and attaches photographs of the defective vial/ampoule and outer carton.", "Receives submission confirmation and tracking number.", "Receives alert feedback from pharmacy/NMRA on whether to quarantine remaining ward stock."),
    ("03", "Individual / Patient", "pers:sfp-r-03", "individual-patient", 39, "Purchases medicine with unusual smell, taste, crumbling tablets, or spelling errors on packaging, or experiences unexpected side effects.", "Accesses public web portal, mobile app, or USSD/hotline interface (with option for anonymous reporting).", "Enters medicine name, where purchased, batch number, and expiry date if visible.", "Uploads smartphone photos of the pills and packaging.", "Receives confirmation receipt and tracking reference.", "Receives plain-language advice to consult a health professional and status confirmation when reviewed."),
    ("04", "Community Health Worker", "pers:sfp-r-04", "community-health-worker", 39, "During community outreach, identifies damaged or suspicious antimalarial/ORS/vaccine supplies or hears patient complaints of treatment failure.", "Opens mobile SF reporting app (using offline mode if in a low-connectivity village).", "Selects product from simplified list and records batch number and expiry date.", "Captures photos of the suspect pack and lot details.", "Receives local queue confirmation and tracking number upon network sync.", "Receives supervisor/NMRA notification on replacement stock and community guidance."),
    ("05", "Laboratory Technician", "pers:sfp-r-05", "laboratory-technician", 39, "Detects erratic control results or physical defects in diagnostic test kits or laboratory reagents.", "Logs into the SF reporting system (with option to report anonymously if concerned about reprisal).", "Enters diagnostic kit/reagent identifier, manufacturer, lot/batch number, and expiry date.", "Uploads photos of the reagent lot certificate, cassette/strip defect, and packaging.", "Receives confirmation and tracking number.", "Receives regulatory follow-up regarding lot quarantine and laboratory quality alert."),
    ("06", "Pharmacist", "pers:sfp-r-06", "pharmacist", 40, "Identifies suspicious packaging, missing security seal, inconsistent batch/expiry printing, or patient return of ineffective medicine during dispensing.", "Submits structured SF report via pharmacy management system or dedicated NMRA reporting portal.", "Scans GS1 barcode / GTIN or enters product ID (DE3), manufacturer (DE4), batch (DE6), and expiry (DE7).", "Uploads high-resolution photos of primary/secondary packaging and supplier invoice details.", "Receives tracking number and quarantine guidance.", "Receives formal NMRA disposition (recall, quarantine release, or counterfeit alert)."),
    ("07", "Dentist", "pers:sfp-r-07", "dentist", 40, "Observes failure of local dental anaesthetic or abnormal consistency/packaging of dental medicine or material.", "Accesses digital SF reporting form via clinic workstation or smartphone.", "Enters dental product name, manufacturer, batch number, and expiry date.", "Uploads photos of the dental cartridge/vial and packaging.", "Receives confirmation message and tracking number.", "Receives NMRA follow-up on batch quality assessment."),
    ("08", "Midwife", "pers:sfp-r-08", "midwife", 40, "Observes lack of uterine contraction after administering oxytocin/uterotonic or notices compromised cold-chain/packaging integrity.", "Submits priority SF report via maternity ward mobile device.", "Enters product name, strength, batch number, expiry date, and clinical observation (therapeutic failure).", "Uploads photos of the ampoule and box.", "Receives immediate confirmation and tracking number.", "Receives urgent regulatory feedback and batch replacement instructions."),
    ("09", "Paramedic", "pers:sfp-r-09", "paramedic", 40, "Encounters defective emergency medicine or airway/infusion supply in an ambulance or field emergency with intermittent connectivity.", "Records SF report in the mobile app offline outbox (subprocess SF-REP-006).", "Scans barcode or enters product name, batch number, and expiry date offline.", "Attaches photos stored locally until connectivity is restored.", "App automatically syncs when online and delivers confirmation and tracking number.", "Receives fleet/emergency medical services safety notice and NMRA follow-up."),
]

for num, srole, pers_ref, gterm, pdf_p, st1, st2, st3, st4, st5, st6 in SCENARIOS:
    fname = f"us-sfp-scen-{num}"
    label = f"scen:sfp-scen-{num}"
    title = f"Scenario {int(num)}: {srole} reporting a suspected SF medical product (Table 9, PDF p. {pdf_p})"
    glos = [
        g(SFP_NS, gterm),
        g(SFP_NS, "reporter"),
        g(SFP_NS, "sf-report"),
        g(SFP_NS, "tracking-number"),
        g(SFP_NS, "reporter-feedback-loop"),
        g(RA_NS, "use-case"),
    ]
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [EL_NMRA, EL_REG_SYS, EL_NOTIF],
        "views": [VW_DHSC, VW_PARTNERS],
    }
    md = (
        f"### {title}\n\n"
        f"- **Actor / Persona:** `{pers_ref}` ({srole})\n"
        f"- **Workflow:** `bp:sf-rep-001` (`SF-REP-001`), `bp:sf-rep-002` (`SF-REP-002`)\n\n"
        f"| Stage | Activity |\n"
        f"|---|---|\n"
        f"| **1. Initial discovery of a suspect medical product** | {st1} |\n"
        f"| **2. Reporting the suspect product** | {st2} |\n"
        f"| **3. Providing product details** | {st3} |\n"
        f"| **4. Uploading photos** | {st4} |\n"
        f"| **5. Receiving confirmation and a tracking number** | {st5} |\n"
        f"| **6. Follow-up and feedback** | {st6} |\n"
    )
    meta = {
        "scenarioId": f"SFP-SCEN-{num}",
        "persona": pers_ref,
        "source": "who-iris/library/9789240120747-eng/sections/sec-023-42-define-user-scenarios.md",
        "pdfPage": pdf_p,
        "stages": {
            "discovery": st1,
            "reporting": st2,
            "productDetails": st3,
            "uploadingPhotos": st4,
            "confirmationAndTracking": st5,
            "followUpAndFeedback": st6,
        },
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    write_block(FOLIO_DIR / "ch04-determine-requirements", fname, "userScenario", "dak", label, title, md, meta, f'  personas: [{json.dumps(pers_ref)}, "pers:sfp-r-13"],\n', uses=["prose:sec-023", "tbl:table-09", pers_ref])

# 6. Step P6b: 6 DAK BusinessProcess blocks (bp-sf-rep-001 .. bp-sf-rep-006) + companion .bpmn files
BP_SPECS = [
    ("SF-REP-001", "bp-sf-rep-001", "bp:sf-rep-001", "Process_SF_REP_001", "SF-REP-001 — Detect and report suspected SF medical product (Table 10, Fig. 4)", ["prose:sec-024", "tbl:table-10", "fig:fig-04", "pers:sfp-r-01", "pers:sfp-r-13"], 41, FINDINGS_BY_SEC["sec-024"]),
    ("SF-REP-002", "bp-sf-rep-002", "bp:sf-rep-002", "Process_SF_REP_002", "SF-REP-002 — Receive, acknowledge and track SF report (Table 9, Table 12)", ["prose:sec-023", "prose:sec-026", "tbl:table-12", "pers:sfp-r-01", "pers:sfp-r-13"], 43, []),
    ("SF-REP-003", "bp-sf-rep-003", "bp:sf-rep-003", "Process_SF_REP_003", "SF-REP-003 — Investigate SF report and follow up with reporter (Intro, Table 9, Ch. 7)", ["prose:sec-004", "prose:sec-023", "pers:sfp-r-13", "pers:sfp-r-01", "pers:sfp-r-05"], 41, []),
    ("SF-REP-004", "bp-sf-rep-004", "bp:sf-rep-004", "Process_SF_REP_004", "SF-REP-004 — Take regulatory action on confirmed SF product (Intro, §2.1, §2.2)", ["prose:sec-004", "prose:sec-013", "prose:sec-014", "pers:sfp-r-13", "pers:sfp-r-14", "pers:sfp-r-15"], 27, []),
    ("SF-REP-005", "bp-sf-rep-005", "bp:sf-rep-005", "Process_SF_REP_005", "SF-REP-005 — Report confirmed SF case to WHO GSMS (Intro, Table 4)", ["prose:sec-004", "prose:sec-011", "tbl:table-04", "pers:sfp-r-13", "pers:sfp-r-15"], 24, []),
    ("SF-REP-006", "bp-sf-rep-006", "bp:sf-rep-006", "Process_SF_REP_006", "SF-REP-006 — Submit SF report offline and synchronise (Table 9 Paramedic, Table 13, Ch. 7)", ["prose:sec-023", "prose:sec-026", "pers:sfp-r-09", "pers:sfp-r-13"], 44, []),
]

for code, fname, blabel, pid, btitle, uses, pdf_p, rnotes in BP_SPECS:
    ch_dir = FOLIO_DIR / "ch04-determine-requirements"
    shutil.copy2(ROOT / "processes" / f"{code}.bpmn", ch_dir / f"{fname}.bpmn")
    checklist_txt = (ROOT / "processes" / f"{code}.checklist.md").read_text()
    md = f"![{btitle}](../media/{code}.svg)\n\n{checklist_txt}"
    if rnotes:
        md += "\n> [!WARNING]\n> **BPMN Redraw & Source Review Notes (`litlfred/dth-sfp#1` §3):**\n" + "\n".join(f"> - {n}" for n in rnotes) + "\n"
    glos = [
        g(SFP_NS, "sf-report"),
        g(SFP_NS, "reporter-feedback-loop"),
        g(SFP_NS, "tracking-number"),
        g(RA_NS, "business-process"),
        g(RA_NS, "workflow"),
        g(SC_NS, "traceability"),
    ]
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [EL_NMRA, EL_REG_SYS, EL_RECALL, EL_TRACEABILITY, EL_GLOB_PLAT],
        "views": [VW_DHSC, VW_TT, VW_PARTNERS],
    }
    meta = {
        "code": code,
        "processId": pid,
        "title": btitle,
        "canonicalBpmn": f"processes/{code}.bpmn",
        "canonicalSvg": f"processes/{code}.svg",
        "bpmnFile": f"{fname}.bpmn",
        "svgFile": f"media/{code}.svg",
        "source": "who-iris/library/9789240120747-eng/sections/sec-024-43-develop-business-processes-and-workflows.md",
        "pdfPage": pdf_p,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    extra = f'  processId: {json.dumps(pid)},\n  companions: {{ bpmn: {json.dumps(fname + ".bpmn")} }},\n'
    write_block(ch_dir, fname, "businessProcess", "dak", blabel, btitle, md, meta, extra, uses=uses)

# 7. Step P6c: 4 DAK DecisionTable blocks (dt-sfr-dt-01 .. dt-sfr-dt-04) + companion .dmn files + prose note
DT_SPECS = [
    ("SFR.DT.01", "SFR-DT-01.dmn", "dt-sfr-dt-01", "dt:sfr-dt-01", "Decision_SFR_DT_01", "SFR.DT.01 — Suspected product report classification and workflow path (Fig. 4, DE8)", ["prose:sec-024", "prose:sec-025", "bp:sf-rep-001", "tbl:table-11"], 42, [
        "F2: The handbook glossary (p. ix) and Introduction (p. 1) define 'unregistered/unlicensed medical products' as the third WHO SF category, but Fig. 4 and SFR.A1.DE8 only offer substandard and falsified paths.",
    ]),
    ("SFR.DT.02", "SFR-DT-02.dmn", "dt-sfr-dt-02", "dt:sfr-dt-02", "Decision_SFR_DT_02", "SFR.DT.02 — Applicable medical product type (Table 12 SFR.FXNREQ.006, DE5)", ["prose:sec-025", "prose:sec-026", "tbl:table-11", "tbl:table-12"], 43, [
        "F4: SFR.A1.DE5 ('Type of product') has an empty Description and Data type cell in Table 11 (p. 31); product categories are resolved against the National Product Catalogue (dth-pc) and the glossary definition of 'Medical product' (p. viii).",
    ]),
    ("SFR.DT.03", "SFR-DT-03.dmn", "dt-sfr-dt-03", "dt:sfr-dt-03", "Decision_SFR_DT_03", "SFR.DT.03 — Assigned reporter geographic region (Table 12 SFR.FXNREQ.001)", ["prose:sec-026", "tbl:table-12", "pers:sfp-r-01"], 43, []),
    ("SFR.DT.04", "SFR-DT-04.dmn", "dt-sfr-dt-04", "dt:sfr-dt-04", "Decision_SFR_DT_04", "SFR.DT.04 — Digital capability roadmap milestone (Table 6)", ["prose:sec-019", "tbl:table-06"], 32, []),
]

for code, dmn_file, fname, dlabel, did, dtitle, uses, pdf_p, rnotes in DT_SPECS:
    ch_dir = FOLIO_DIR / "ch04-determine-requirements"
    shutil.copy2(ROOT / "decisions" / dmn_file, ch_dir / f"{fname}.dmn")
    md = (
        f"### {dtitle}\n\n"
        f"- **Decision ID:** `{did}` (`{code}`)\n"
        f"- **Canonical DMN 1.3 File:** [`decisions/{dmn_file}`](../../../decisions/{dmn_file})\n"
        f"- **Companion DMN File:** `{fname}.dmn`\n"
    )
    if rnotes:
        md += "\n> [!WARNING]\n> **Decision Logic Review Notes (`litlfred/dth-sfp#1` §2.4 & §3):**\n" + "\n".join(f"> - {n}" for n in rnotes) + "\n"
    glos = [
        g(SFP_NS, "sf-report"),
        g(SFP_NS, "report-type"),
        g(PC_NS, "national-product-catalogue"),
        g(RA_NS, "data-element"),
    ]
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [EL_NMRA, EL_NPC, EL_FAC_REG],
        "views": [VW_NPC, VW_DHSC],
    }
    meta = {
        "code": code,
        "decisionId": did,
        "title": dtitle,
        "canonicalDmn": f"decisions/{dmn_file}",
        "dmnFile": f"{fname}.dmn",
        "source": "who-iris/library/9789240120747-eng/sections/sec-025-44-outline-data-requirements.md",
        "pdfPage": pdf_p,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    extra = f'  decisionId: {json.dumps(did)},\n  companions: {{ dmn: {json.dumps(fname + ".dmn")} }},\n'
    write_block(ch_dir, fname, "decisionTable", "dak", dlabel, dtitle, md, meta, extra, uses=uses)

# Named decision points without rules in source
write_block(
    FOLIO_DIR / "ch04-determine-requirements",
    "p-decision-points-without-rules",
    "prose",
    "builders",
    "prose:decision-points-without-rules",
    "Named Decision Points Without Rules in the Handbook (PV Routing & Annex 7 Risk Scoring)",
    """### Named Decision Points Without Rules in the Handbook (`litlfred/dth-sfp#1` §2.4)

Per owner rule (`litlfred/dth-sfp#1` §2.4), decision logic is extracted into DMN tables **only where the handbook states the rule**; nothing is inferred. Two decision points named in the handbook state no rule and are recorded here as explicit source gaps:

1. **Adverse drug reaction reported (`SFR.A1.DE9`) → Co-routing to Pharmacovigilance (PV) system** (§1.3 p. 12, §2.1 p. 15, Table 11 p. 31): The handbook emphasises aligning SF reporting with national pharmacovigilance systems (`VigiFlow` / `VigiBase`) and captures `SFR.A1.DE9` (*Adverse reaction details: Details of any adverse reaction that the patient experienced after using the product*), but gives no threshold or routing rule for when an SF report must automatically generate or forward an Individual Case Safety Report (ICSR) to the PV system.
2. **Risk impact × probability → Priority level** (Annex 7 *Risk management template*, p. 59 / PDF p. 71): Annex 7 illustrates a risk register table with columns `Risk description`, `Category`, `Impact`, `Probability`, `Priority`, `Risk mitigation`, `Action`, and `Status`, containing a single example row (`Impact: High`, `Probability: Medium`, `Priority: High`), without defining the impact × probability scoring matrix.
""",
    {
        "source": "who-iris/library/9789240120747-eng/sections/sec-025-44-outline-data-requirements.md",
        "pdfPage": 43,
        "reviewNotes": [
            "Named decision point without rule 1: Adverse reaction (SFR.A1.DE9) -> Pharmacovigilance co-routing (§1.3, §2.1, DE9).",
            "Named decision point without rule 2: Risk impact x probability -> priority matrix (Annex 7, p. 59).",
        ],
        "glossary": [g(SFP_NS, "adverse-drug-reaction"), g(SFP_NS, "pharmacovigilance"), g(SFP_NS, "sf-report")],
        "glossaryTerms": [f"{SFP_NS}adverse-drug-reaction", f"{SFP_NS}pharmacovigilance", f"{SFP_NS}sf-report"],
        "archimate": {"model": "0.3.0-draft.1", "basis": "agent-proposed", "elements": [EL_NMRA, EL_QUAL_SYS], "views": [VW_DHSC]},
    },
    uses=["prose:sec-011", "prose:sec-013", "prose:sec-025", "prose:sec-041"],
)

# 8. Step P6a: 10 DAK DataElement blocks (de-sfr-a1-de01 .. de-sfr-a1-de10) from Table 11
DATA_ELEMENTS = [
    ("01", "SFR.A1.DE1", "Product name", "The brand or generic name of the medical product being reported.", "String", [g(SFP_NS, "suspect-product"), g(SFP_NS, "medical-product"), g(PC_NS, "generic-product"), g(PC_NS, "trade-item")], [EL_NPC, EL_PROD_REG], []),
    ("02", "SFR.A1.DE2", "Type of report", "(Empty in source Table 11 — see Finding F4 and SFR.A1.DE8).", "Unspecified in source (F4)", [g(SFP_NS, "report-type"), g(SFP_NS, "sf-report"), g(RA_NS, "data-element")], [EL_REG_SYS], ["F4: SFR.A1.DE2 ('Type of report') has empty Description and Data type cells in Table 11 (p. 31), and its label is duplicated by SFR.A1.DE8."]),
    ("03", "SFR.A1.DE3", "Product ID", "A unique number or code assigned to the product, used to identify it in the system.", "String / Identifier", [g(SFP_NS, "suspect-product"), g(PC_NS, "country-trade-item-identifier"), g(PC_NS, "product-master-data"), g(SC_NS, "traceability")], [EL_NPC, EL_PROD_VER, EL_TRACE_EVT], []),
    ("04", "SFR.A1.DE4", "Manufacturer", "The name of the company that manufactured the product.", "String", [g(SFP_NS, "suspect-product"), g(PC_NS, "product-master-data"), g(PC_NS, "trade-item")], [EL_MFG, EL_NPC], []),
    ("05", "SFR.A1.DE5", "Type of product", "(Empty in source Table 11 — see Finding F4 and SFR.DT.02).", "Unspecified in source (F4; resolved via SFR.DT.02)", [g(SFP_NS, "medical-product"), g(PC_NS, "product-classification"), g(RA_NS, "data-element")], [EL_NPC, EL_TERM_SVC], ["F4: SFR.A1.DE5 ('Type of product') has empty Description and Data type cells in Table 11 (p. 31); Table 12 row 6 (SFR.FXNREQ.006 / SFR.DT.02) requires the system to auto-assign it when a user selects a specific product."]),
    ("06", "SFR.A1.DE6", "Batch number", "The number assigned to a specific batch of the product, used to trace its production history.", "String", [g(SFP_NS, "suspect-product"), g(PC_NS, "transactional-data"), g(SC_NS, "traceability")], [EL_TRACK_TRACE, EL_TRACE_EVT, EL_RECALL], []),
    ("07", "SFR.A1.DE7", "Expiry date", "The date after which the product should not be used.", "Date", [g(SFP_NS, "suspect-product"), g(PC_NS, "transactional-data"), g(SC_NS, "traceability")], [EL_TRACK_TRACE, EL_TRACE_EVT], []),
    ("08", "SFR.A1.DE8", "Type of report", "Indicates whether the report is from a health care professional, the public or the pharmaceutical industry (e.g. manufacturer, importer).", "Coding (HCP | Public | Pharmaceutical industry)", [g(SFP_NS, "report-type"), g(SFP_NS, "substandard-medical-product"), g(SFP_NS, "falsified-medical-product"), g(SFP_NS, "unregistered-or-unlicensed-medical-product")], [EL_REG_SYS, EL_NMRA], [
        "F2: SFR.A1.DE8 and Fig. 4 omit 'unregistered/unlicensed medical products' (defined on p. ix and p. 1).",
        "F4: SFR.A1.DE8 repeats the data element name 'Type of report' already used by SFR.A1.DE2.",
    ]),
    ("09", "SFR.A1.DE9", "Adverse reaction details", "Details of any adverse reaction that the patient experienced after using the product.", "Text", [g(SFP_NS, "adverse-drug-reaction"), g(SFP_NS, "therapeutic-failure"), g(SFP_NS, "pharmacovigilance")], [EL_QUAL_SYS, EL_REG_SYS], []),
    ("10", "SFR.A1.DE10", "Contact information", "The reporter's contact details (such as phone number or email address) for follow-up if needed.", "String", [g(SFP_NS, "reporter"), g(SFP_NS, "anonymous-report"), g(SFP_NS, "reporter-feedback-loop")], [EL_SEC_CONSENT, EL_HWR], []),
]

for num, de_id, de_name, de_desc, de_type, glos, els, rnotes in DATA_ELEMENTS:
    fname = f"de-sfr-a1-de{num}"
    label = f"de:sfr-a1-de{num}"
    title = f"{de_id} — {de_name} (Table 11, p. 31 / PDF p. 43)"
    md = (
        f"### {title}\n\n"
        f"- **Data Element ID:** `{de_id}`\n"
        f"- **Data Element Name:** {de_name}\n"
        f"- **Description (Table 11):** {de_desc}\n"
        f"- **Data Type:** `{de_type}`\n"
        f"- **FHIR / Terminology Binding:** Open (to be bound in L3 FHIR IG per `litlfred/dth-sfp#1` §2.3)\n"
    )
    if rnotes:
        md += "\n> [!WARNING]\n> **Data Dictionary Review Notes (`litlfred/dth-sfp#1` §3):**\n" + "\n".join(f"> - {n}" for n in rnotes) + "\n"
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": els,
        "views": [VW_PMD, VW_NPC, VW_TT],
    }
    meta = {
        "elementId": de_id,
        "name": de_name,
        "dataType": de_type,
        "description": de_desc,
        "source": "who-iris/library/9789240120747-eng/sections/sec-025-44-outline-data-requirements.md",
        "pdfPage": 43,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    write_block(FOLIO_DIR / "ch04-determine-requirements", fname, "dataElement", "dak", label, title, md, meta, f'  elementId: {json.dumps(de_id)},\n  dataType: {json.dumps(de_type)},\n', uses=["prose:sec-025", "tbl:table-11"])

# 9. Step P6a: 7 DAK FunctionalRequirement blocks (fxnreq-sfr-001 .. fxnreq-sfr-007) from Table 12
FXN_REQS = [
    ("001", "SFR.FXNREQ.001", False, "pers:sfp-r-13", "Public health agency", "know the region where the reporter is located based on the user's profile", "I do not have to ask the user to enter that information in the report"),
    ("002", "SFR.FXNREQ.002", False, "pers:sfp-r-13", "Public health agency", "know the user's profession based on their user profile", "I can understand which professions are reporting the most and target training accordingly"),
    ("003", "SFR.FXNREQ.003", True, "pers:sfp-r-01", "User", "have the system generate a unique tracking number for each report", "I can easily reference and monitor the progress of my report"),
    ("004", "SFR.FXNREQ.004", True, "pers:sfp-r-01", "User", "receive a confirmation message after submitting a report", "I am assured that my report has been successfully received"),
    ("005", "SFR.FXNREQ.005", True, "pers:sfp-r-13", "Regulatory authority", "receive real-time alerts when a new report is submitted", "I can review and act on critical reports promptly"),
    ("006", "SFR.FXNREQ.006", True, "pers:sfp-r-13", "Public health agency", "have the system assign the applicable type of product after a user selects a specific product", "I can minimize reporting errors"),
    ("007", "SFR.FXNREQ.007", True, "pers:sfp-r-13", "Public health agency", "ensure that all mandatory fields are completed before a report can be submitted", "I have all the necessary information to investigate the report"),
]

for num, req_id, is_assigned, actor_ref, as_a, i_want, so_that in FXN_REQS:
    fname = f"fxnreq-sfr-{num}"
    label = f"freq:sfr-{num}"
    assigned_tag = " [assigned ID — F4]" if is_assigned else ""
    title = f"{req_id}{assigned_tag} — As a {as_a}, I want to {i_want[:48]}... (Table 12, p. 31)"
    rnotes = ["F4: Requirement ID omitted in source Table 12 (p. 31 / PDF p. 43); assigned ID " + req_id + " in L2."] if is_assigned else []
    md = (
        f"### {req_id}{assigned_tag}\n\n"
        f"- **Requirement ID:** `{req_id}` ({'Assigned in L2 per Finding F4 — blank in source Table 12' if is_assigned else 'Printed in source Table 12'})\n"
        f"- **Actor / Persona:** `{actor_ref}` ({as_a})\n"
        f"- **As a:** {as_a}\n"
        f"- **I want:** {i_want}\n"
        f"- **So that:** {so_that}\n"
    )
    glos = [
        g(RA_NS, "functional-requirements"),
        g(RA_NS, "user-story"),
        g(SFP_NS, "sf-report"),
        g(SFP_NS, "tracking-number"),
    ]
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [EL_REG_SYS, EL_NMRA, EL_NOTIF],
        "views": [VW_DHSC, VW_COMP],
    }
    meta = {
        "requirementId": req_id,
        "idAssignedInL2": is_assigned,
        "actor": actor_ref,
        "asA": as_a,
        "iWant": i_want,
        "soThat": so_that,
        "source": "who-iris/library/9789240120747-eng/sections/sec-026-45-gather-requirements.md",
        "pdfPage": 43,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    if rnotes:
        meta["reviewNotes"] = rnotes
    write_block(FOLIO_DIR / "ch04-determine-requirements", fname, "functionalRequirement", "dak", label, title, md, meta, f'  requirementId: {json.dumps(req_id)},\n  actor: {json.dumps(actor_ref)},\n', uses=["prose:sec-026", "tbl:table-12", actor_ref])

# 10. Step P6a: 11 DAK NonFunctionalRequirement category blocks (nfxnreq-sfr-01 .. nfxnreq-sfr-11) from Table 13
NFR_CATEGORIES = [
    ("01", "SFR.NFXNREQ.CAT.01", "Security and confidentiality", "security", 44, [
        "SFR.NFXNREQ.001 (source ID): Ensure role-based access control (RBAC), authentication, and protection of confidential reporter and patient data.",
        "SFR.NFXNREQ.002–009 (assigned IDs, F4): Encrypt data in transit and at rest, support anonymous reporting (DE10), enforce password complexity and session timeouts, and protect against unauthorized access.",
    ], ["F4: Only row 1 (SFR.NFXNREQ.001) in Security and confidentiality carries a printed ID in Table 13; remaining rows assigned sequential IDs."]),
    ("02", "SFR.NFXNREQ.CAT.02", "Interoperability", "interoperability", 44, [
        "SFR.NFXNREQ.010 (source ID): Support standards-based data exchange with national and global systems (National Product Catalogue, Facility Registry, VigiFlow/PV, WHO GSMS).",
        "SFR.NFXNREQ.011–017 (assigned IDs, F4): Provide open APIs (HL7 FHIR), terminology bindings (SNOMED GPS, ICD), and compatibility with 'workstream 3 content (CQL + FHIR resources)' (Finding F8).",
    ], [
        "F4: Only the first row (SFR.NFXNREQ.010) in Interoperability carries a printed ID in Table 13; remaining rows assigned sequential IDs.",
        "F8: Row 5 of Interoperability in Table 13 (p. 32 / PDF p. 44) references 'workstream 3 content (CQL + FHIR resources)', which is undefined in the handbook.",
    ]),
    ("03", "SFR.NFXNREQ.CAT.03", "System performance and availability", "performance", 45, [
        "SFR.NFXNREQ.018–025 (assigned IDs, F4): Ensure fast response times for form loading, product search, photo upload, and report submission under concurrent load, with high system uptime.",
    ], ["F4: All rows in System performance and availability have blank ID cells in Table 13; assigned SFR.NFXNREQ.018–025."]),
    ("04", "SFR.NFXNREQ.CAT.04", "Usability and accessibility", "usability", 45, [
        "SFR.NFXNREQ.026–034 (assigned IDs, F4): Provide intuitive mobile- and web-responsive interfaces suitable for diverse health workers and public reporters, minimizing required typing via dropdowns and barcode scanning.",
    ], ["F4: All rows in Usability and accessibility have blank ID cells in Table 13; assigned SFR.NFXNREQ.026–034."]),
    ("05", "SFR.NFXNREQ.CAT.05", "Scalability", "scalability", 45, [
        "SFR.NFXNREQ.035–040 (assigned IDs, F4): Scale horizontally and vertically to accommodate growing numbers of users, facilities, product catalogue entries, and image attachments during national roll-out.",
    ], ["F4: All rows in Scalability have blank ID cells in Table 13; assigned SFR.NFXNREQ.035–040."]),
    ("06", "SFR.NFXNREQ.CAT.06", "Maintainability and support", "maintainability", 46, [
        "SFR.NFXNREQ.041–047 (assigned IDs, F4): Support modular configuration, automated software updates, clear system documentation, and local helpdesk/technical maintenance.",
    ], ["F4: All rows in Maintainability and support have blank ID cells in Table 13; assigned SFR.NFXNREQ.041–047."]),
    ("07", "SFR.NFXNREQ.CAT.07", "Data backup and recovery", "reliability", 46, [
        "SFR.NFXNREQ.048–054 (assigned IDs, F4): Perform automated regular backups of SF reports and attachments, support disaster recovery, and prevent data loss during power or network failures.",
    ], ["F4: All rows in Data backup and recovery have blank ID cells in Table 13; assigned SFR.NFXNREQ.048–054."]),
    ("08", "SFR.NFXNREQ.CAT.08", "Offline capability", "offline", 46, [
        "SFR.NFXNREQ.055–061 (assigned IDs, F4): Allow reporters in low-connectivity settings to capture SF reports and photos offline, store them in a local outbox, and synchronise automatically when connectivity resumes (subprocess SF-REP-006).",
    ], ["F4: All rows in Offline capability have blank ID cells in Table 13; assigned SFR.NFXNREQ.055–061."]),
    ("09", "SFR.NFXNREQ.CAT.09", "Compliance and legal", "compliance", 46, [
        "SFR.NFXNREQ.062–067 (assigned IDs, F4): Comply with national data protection, privacy, cybersecurity, and pharmaceutical regulatory laws.",
    ], ["F4: All rows in Compliance and legal have blank ID cells in Table 13; assigned SFR.NFXNREQ.062–067."]),
    ("10", "SFR.NFXNREQ.CAT.10", "Localization and language support", "localization", 47, [
        "SFR.NFXNREQ.068–072 (assigned IDs, F4): Support multiple national and local languages, local date/time formats, and culturally appropriate terminology.",
    ], ["F4: All rows in Localization and language support have blank ID cells in Table 13; assigned SFR.NFXNREQ.068–072."]),
    ("11", "SFR.NFXNREQ.CAT.11", "Audit trail and logging", "audit", 47, [
        "SFR.NFXNREQ.073–078 (assigned IDs, F4): Record tamper-evident audit logs of all report creations, edits, status transitions, user logins, and regulatory actions.",
    ], ["F4: All rows in Audit trail and logging have blank ID cells in Table 13; assigned SFR.NFXNREQ.073–078."]),
]

for num, req_id, cat_name, cat_slug, pdf_p, items, rnotes in NFR_CATEGORIES:
    fname = f"nfxnreq-sfr-{num}"
    label = f"nfreq:sfr-{num}"
    title = f"{req_id} — Non-functional requirements: {cat_name} (Table 13, PDF p. {pdf_p})"
    md = (
        f"### {title}\n\n"
        f"- **Category:** {cat_name} (`{cat_slug}`)\n"
        f"- **Table 13 Source Page:** PDF p. {pdf_p} (`sec-026`)\n\n"
        + "\n".join(f"- {it}" for it in items)
        + "\n\n> [!NOTE]\n> **Table 13 Review Notes (`litlfred/dth-sfp#1` §3):**\n"
        + "\n".join(f"> - {n}" for n in rnotes)
        + "\n"
    )
    glos = [
        g(RA_NS, "non-functional-requirements"),
        g(RA_NS, "interoperability"),
        g(SFP_NS, "sf-report"),
    ]
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [EL_REG_SYS, EL_SEC_CONSENT, EL_INFO_MED],
        "views": [VW_INTEROP, VW_COMP],
    }
    meta = {
        "requirementId": req_id,
        "category": cat_name,
        "categoryCode": cat_slug,
        "items": items,
        "source": "who-iris/library/9789240120747-eng/sections/sec-026-45-gather-requirements.md",
        "pdfPage": pdf_p,
        "reviewNotes": rnotes,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    write_block(FOLIO_DIR / "ch04-determine-requirements", fname, "nonFunctionalRequirement", "dak", label, title, md, meta, f'  requirementId: {json.dumps(req_id)},\n  category: {json.dumps(cat_slug)},\n', uses=["prose:sec-026", "tbl:table-13"])

# 11. Step P6a: 5 DAK Indicator blocks (ind-sfp-01 .. ind-sfp-05) from Table 18 (NO empirical targets)
INDICATORS = [
    ("01", "SFP.IND.01", "Quality measures (completeness, accuracy and timeliness of SF reports)", "Proportion of submitted SF reports with all mandatory core data elements (SFR.A1.DE1–DE10) completed accurately, and user satisfaction with reporting ease and clarity (Table 18, p. 44 / PDF p. 56). No empirical target values are asserted.", "Number of submitted SF reports with complete and validated core data elements (DE1–DE10)", "Total number of SF reports submitted in the reporting period"),
    ("02", "SFP.IND.02", "Fidelity measures (adherence to reporting workflows and detection-to-notification time)", "Adherence of system implementation to defined workflows (SF-REP-001–006), including elapsed detection-to-notification time and proportion of reports receiving acknowledgement and follow-up feedback (Table 18, p. 44 / PDF p. 56). No empirical target values are asserted.", "Elapsed time from detection/submission to NMRA notification and count of reports completing the feedback loop", "Total submitted SF reports requiring regulatory screening and feedback"),
    ("03", "SFP.IND.03", "Stability measures (system uptime, crash rate and offline sync reliability)", "Technical stability of the SF reporting platform, measured by system availability/uptime rate, error/crash frequency, and successful synchronisation rate of offline outbox reports (Table 18, p. 44 / PDF p. 56). No empirical target values are asserted.", "System operational uptime hours and successfully synchronised reports", "Total scheduled operational hours and total queued reports"),
    ("04", "SFP.IND.04", "Functionality measures (feature utilization and interoperability performance)", "Extent to which core functional features (barcode/product lookup SFR.DT.02, auto-region SFR.DT.03, photo upload, tracking number generation, registry/GSMS exchange) perform as specified (Table 18, p. 44 / PDF p. 56). No empirical target values are asserted.", "Number of functional features and interoperability exchanges operating without error", "Total deployed functional and interoperability capabilities"),
    ("05", "SFP.IND.05", "Investment and sustainability measures (cost efficiency and scale-up coverage)", "Alignment of implementation expenditure, workforce training coverage, and maintenance resources with the digital investment roadmap (Table 6, Table 18, p. 44 / PDF p. 56). No empirical target values are asserted.", "Facilities/regions actively using the digital SF reporting system within planned operational budget", "Total target facilities/regions in the phased implementation plan"),
]

for num, ind_id, ind_name, ind_desc, numer, denom in INDICATORS:
    fname = f"ind-sfp-{num}"
    label = f"ind:sfp-{num}"
    title = f"{ind_id} — {ind_name} (Table 18, p. 44 / PDF p. 56)"
    md = (
        f"### {title}\n\n"
        f"- **Indicator ID:** `{ind_id}`\n"
        f"- **Description:** {ind_desc}\n"
        f"- **Numerator:** {numer}\n"
        f"- **Denominator:** {denom}\n"
        f"- **Empirical Targets:** None (per `litlfred/dth-sfp#1` §2.3 & §5 rule: indicator definitions carry no empirical targets or numbers).\n"
    )
    glos = [
        g(SFP_NS, "monitoring"),
        g(SFP_NS, "evaluation"),
        g(SFP_NS, "detection-to-notification-time"),
        g(SFP_NS, "sf-report"),
        g(RA_NS, "outcome"),
    ]
    arch = {
        "model": "0.3.0-draft.1",
        "basis": "agent-proposed by name, for working-group review (litlfred/dth-sfp#1)",
        "elements": [EL_ANALYTICS, EL_REP_MOD, EL_NMRA],
        "views": [VW_CAP, VW_DHSC],
    }
    meta = {
        "indicatorId": ind_id,
        "name": ind_name,
        "description": ind_desc,
        "numerator": numer,
        "denominator": denom,
        "source": "who-iris/library/9789240120747-eng/sections/sec-029-61-develop-a-monitoring-and-evaluation-plan.md",
        "pdfPage": 56,
        "glossary": glos,
        "glossaryTerms": [x["iri"] for x in glos],
        "archimate": arch,
    }
    write_block(FOLIO_DIR / "ch06-monitor-evaluate-scale", fname, "indicator", "dak", label, title, md, meta, f'  indicatorId: {json.dumps(ind_id)},\n  numerator: {json.dumps(numer)},\n  denominator: {json.dumps(denom)},\n', uses=["prose:sec-029", "tbl:table-18"])

print("Seeded folio/dth-sfp/ across all 11 chapter directories.")

# 12. Write chapter manifests (<chapter>/<chapter>.ts) and root document manifest (folio/dth-sfp/dth-sfp.ts)
CHAPTER_TITLES = [
    ("00-front-matter", "Front matter (Imprint, Acknowledgements, Abbreviations and Glossary)"),
    ("00-introduction", "Introduction"),
    ("ch01-assess-current-state", "1. Assess the current state and enabling environment"),
    ("ch02-shared-understanding-governance", "2. Establish a shared understanding and governance framework"),
    ("ch03-future-state", "3. Define the future state"),
    ("ch04-determine-requirements", "4. Determine the requirements"),
    ("ch05-plan-implementation", "5. Plan the implementation"),
    ("ch06-monitor-evaluate-scale", "6. Monitor, evaluate and scale"),
    ("ch07-share-experiences", "7. Share implementation experiences"),
    ("references-resources", "References and resources"),
    ("annexes", "Annexes 1–7"),
]

for ch_slug, ch_title in CHAPTER_TITLES:
    ch_dir = FOLIO_DIR / ch_slug
    block_stems = sorted(
        p.stem
        for p in ch_dir.glob("*.ts")
        if p.stem != ch_slug
    )
    ch_ts = (
        'import { chapter, section } from "../../schema/builders";\n\n'
        "export default chapter({\n"
        f"  title: {json.dumps(ch_title)},\n"
        f"  label: {json.dumps('chap:' + ch_slug)},\n"
        "  sections: [\n"
        "    section({\n"
        f"      title: {json.dumps(ch_title)},\n"
        f"      label: {json.dumps('sec:' + ch_slug)},\n"
        f"      blocks: {json.dumps(block_stems)},\n"
        "    }),\n"
        "  ],\n"
        "});\n"
    )
    (ch_dir / f"{ch_slug}.ts").write_text(ch_ts)

doc_ts = """import { paper, chapterRef } from "../schema/builders";

export default paper({
  title: "Digital transformation handbook for reporting substandard and falsified medical products",
  authors: ["World Health Organization"],
  date: "2026",
  meta: {
    documentKind: "smart-base:dth",
    level: "L2",
    targetLevel: "L2",
    isbn: "9789240120747",
    iris: "10665/384624",
    source: { library: "9789240120747-eng", repository: "litlfred/who-iris" },
    licence: "CC BY-NC-SA 3.0 IGO",
    status: "complete L2 DTH folio (litlfred/dth-sfp#1 Steps P4–P7): 43 outline sections, 27 structured tables, 6 figures, 15 personas (SFP-R-01..15), 9 user scenarios, 6 BPMN 2.0 processes (SF-REP-001..006), 4 DMN 1.3 decision tables (SFR.DT.01..04), 10 data elements (SFR.A1.DE1..10), 7 functional requirements, 11 non-functional requirement categories, 5 indicators, and 100% L1 normative coverage",
    figureViews: [
      { figure: "Fig. 1", block: "folio/dth-sfp/00-introduction/f-fig-01.md", model: "0.3.0-draft.1", view: "id-4e6e25746e8d4398add06fcbc4fb5a4e", viewName: "Capabilities-Goals" },
      { figure: "Fig. 2", block: "folio/dth-sfp/00-introduction/f-fig-02.md", model: "0.3.0-draft.1", view: "id-8c5dd12b8d4e425184f6003d0513d569", viewName: "Interoperability Layer" },
      { figure: "Fig. 3", block: "folio/dth-sfp/ch03-future-state/f-fig-03.md", model: "0.3.0-draft.1", view: "id-92267636cc42566ca5d2cff0e81be8c9", viewName: "DHSC Architecture Framework (DTH SC Fig. 14)" },
      { figure: "Fig. 4", block: "folio/dth-sfp/ch04-determine-requirements/f-fig-04.md", model: "0.3.0-draft.1", view: "id-bea56e01c8345fbc803dee47a17ccfd3", viewName: "Track and Trace through DHSC Components (DTH SC Fig. 24)" },
      { figure: "Fig. 5", block: "folio/dth-sfp/ch06-monitor-evaluate-scale/f-fig-05.md", model: "0.3.0-draft.1", view: "id-4e6e25746e8d4398add06fcbc4fb5a4e", viewName: "Capabilities-Goals" },
      { figure: "Fig. 6", block: "folio/dth-sfp/ch06-monitor-evaluate-scale/f-fig-06.md", model: "0.3.0-draft.1", view: "id-4e6e25746e8d4398add06fcbc4fb5a4e", viewName: "Capabilities-Goals" },
    ],
  },
  chapters: [
    chapterRef({ dir: "00-front-matter" }),
    chapterRef({ dir: "00-introduction" }),
    chapterRef({ dir: "ch01-assess-current-state" }),
    chapterRef({ dir: "ch02-shared-understanding-governance" }),
    chapterRef({ dir: "ch03-future-state" }),
    chapterRef({ dir: "ch04-determine-requirements" }),
    chapterRef({ dir: "ch05-plan-implementation" }),
    chapterRef({ dir: "ch06-monitor-evaluate-scale" }),
    chapterRef({ dir: "ch07-share-experiences" }),
    chapterRef({ dir: "references-resources" }),
    chapterRef({ dir: "annexes" }),
  ],
});
"""
(FOLIO_DIR / "dth-sfp.ts").write_text(doc_ts)
print("Wrote folio/dth-sfp/dth-sfp.ts and 11 chapter manifests.")
