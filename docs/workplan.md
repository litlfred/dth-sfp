<!-- claude-projects-attribution: {"github_login":"litlfred"} -->
_Requested by **litlfred** · [project thread](https://claude.ai/code/project/chan_017WNUkNK8kdDziPK58Pv6G9?thread=cmsg_017WNUkNK8kdDziPK58Pv6G94iS5AL2CvRnmbf3WBK8tir)_

Workplan (moved from litlfred/smart-ra#136). Updated 2026-10-31 01:55Z: section 2.4 (BPMN for each business process, roles in DAK schemas, DMN tables) approved by the owner. Term placement is open in litlfred/smart-ra#146. Related: litlfred/smart-ra#133, #139 (glossary conflicts), #147 (NMRA role), litlfred/smart-base#242, litlfred/dth-hrh#47. Session: https://claude.ai/code/session_01Qmmkt8KMUSeoNpVrULjNpy

# Workplan: dth-sfp as an L2 DTH on smart-ra (draft for approval, 2026-10-31)

Handbook: *Digital transformation handbook for reporting substandard and falsified medical products* (WHO 2026, ISBN 9789240120747, IRIS 187cabc7).
L1 source: `litlfred/who-iris` `library/9789240120747-eng` (72 PDF pages, 144 page sections, 72 prose blocks, 6 vector figures).
Target: `litlfred/dth-sfp` (fork, today holds only `.gitignore`). Shared content: `litlfred/smart-ra`.
Builds on `workplans.md` in this folder (split rule, S1 to S4). Depends on smart-ra#133, smart-base#242, the dth-hrh#47 pilot and **dth-sc** (owner, 2026-10-31: dth-pc and probably dth-sfp depend on dth-sc). Tracking issue: this repo (moved from litlfred/smart-ra#136).
Status: **plan only.** No code, no issue and no PR until the owner approves.

Page numbers below are the handbook's printed page numbers (PDF page = printed page + 12).

---

## 1. What the L1 entry holds

### 1.1 Shape of the handbook

| part | printed pp. | content | DIIG phase |
|---|---|---|---|
| Front matter | i–ix | title, licence, contents, acknowledgements, abbreviations (19), **glossary (35 terms)** | – |
| Introduction | 1–6 | SF definitions (WHA70), reporting rationale, audience (Table 1), use scenarios, SMART L1–L5 (Fig. 2), DIIG (Fig. 1) | – |
| Ch 1 Assess current state | 7–13 | stakeholders (Table 2), digital readiness (Table 3), current practice and data tools (Table 4), barriers (Table 5) | 1 |
| Ch 2 Shared understanding and governance | 14–17 | regulatory policy review, multisector alignment, governance bodies and roles, SMART goals, risk | 2 |
| Ch 3 Future state | 18–22 | investment roadmap (Table 6), enterprise architecture link (Fig. 3, DIIG EA framework) | 3, 4 |
| Ch 4 Determine requirements | 23–35 | personas (Tables 7, 8), scenarios (Table 9), process matrix (Table 10), workflow (Fig. 4), data elements (Table 11), functional reqs (Table 12), non-functional reqs (Table 13) | 5 |
| Ch 5 Plan implementation | 36–38 | planning steps (Table 14), software options (Table 15) | 7 |
| Ch 6 Monitor, evaluate, scale | 39–45 | M&E maturity (Figs 5, 6), evaluation questions (Table 16), M&E plan steps (Table 17), measures (Table 18), operations plan | 6 |
| Ch 7 Share experiences | 46–47 | Indonesia / Tanzania pilot case study | – |
| References, resources | 48–50 | 37 refs; resources incl. DIIG, PHC, SC and PC handbooks | – |
| Annexes 1–7 | 51–59 | digital principles, persona template, BPMN symbols, RACI, software landscape template, barriers map, risk template | – |

The handbook says it covers SMART L1 and L2 (p. 5). Chapter 4 is in effect a small DAK: personas, scenarios, a business process, a data dictionary and requirements. That is the content worth formalizing.

### 1.2 State of the L1 ingest

- **Page-granular, no outline** (`structure.json`: `toc_source: none`), though the handbook has a two-page contents list. The folio has to be re-sectioned by chapter and section (step P1).
- **The PDF is missing** from `uploads/9789240120747-eng/` (agy prompt in the parent thread). Re-sectioning and table extraction need it; the page text alone loses table structure (Tables 9, 11–13 are flattened).
- Figures: 6 vector figures (Figs 1, 2, 3, 4, 5/6). Fig. 4 (the workflow) is the one that becomes formal content.
- `keywords.json` and `summaries.json` exist (draft summaries, 2026-10-28).

---

## 2. Where each piece goes

### 2.0 Dependency on dth-sc (added 2026-10-31)

dth-sfp declares `needs: [smart-ra, dth-sc]` and mounts dth-sc as well as who-iris. What it takes from dth-sc instead of defining:

- SC's domain terms: product verification, track and trace, the traceability models, the traceability event (product id, batch, serial; receive, ship, dispense, discard).
- SC's "Digital health supply chain architecture" view: the SF reporting app and NMRA back end are linked into it rather than drawn again.
- SFP data elements DE3 (product ID), DE6 (batch number) and DE7 (expiry date) link to the matching SC/PC data elements, so a report names a product the same way the supply chain does.

Open point: the "search for the product" requirement and the "standardized master data" NFR point at the product catalogue, so dth-sfp may also need dth-pc (which itself needs dth-sc). Decided when P4 starts.

Definition conflicts with smart-ra are raised as issues on smart-ra (owner, 2026-10-31), not settled in dth-sfp. First batch: see section 3, F10.

The split rule from `workplans.md`: shared glossary concepts and **every** ArchiMate element and view go in smart-ra; the narrative, its own domain terms (each linked to the smart-ra concept it narrows) and the block-to-ArchiMate links go in dth-sfp.

### 2.1 Glossary

The handbook's 35 glossary terms split three ways.

**A. Already in smart-ra (link, record the handbook's wording as an alternative, choose nothing):**
enterprise architecture, interoperability, registry, SMART Guidelines, point-of-service applications (used in §3.2), SNOMED GPS (§4.4).

**B. New in smart-ra (shared beyond this handbook).** Two clusters:

- *DIIG / requirements vocabulary* that every DTH uses: business process, workflow, data element, persona, end user, features, functional requirements, non-functional requirements, enabling environment, digitization, digitalization, digital transformation, monitoring, evaluation, open source, open standards, organogram, user acceptance testing. PHC, SC and PC define many of the same; they go in with sources, as alternatives (S1 rule).
- *Medical product quality and safety vocabulary* (new smart-ra collection). PC and SC also touch recall, traceability and product quality, so these should not live in one handbook: medical product (generic product / product information), trade item, substandard medical product, falsified medical product, unregistered medical product, pharmacovigilance, active pharmacovigilance, passive pharmacovigilance, adverse drug reaction, post-market surveillance, risk-based post-market surveillance, national medicines regulatory authority (NMRA), health care professional, Member State Mechanism, GSMS.

**C. dth-sfp's own terms** (each `skos:broader` or `closeMatch` to a smart-ra concept): SF report, report type, suspect product, reporter, anonymous report, therapeutic failure / lack of efficacy, tracking number, reporter feedback loop, detection-to-notification time, polypharmacy (as a reporting barrier), the persona specializations from Tables 7–9.

### 2.2 ArchiMate (all in smart-ra)

smart-ra 0.2.0 has nothing for SF reporting, pharmacovigilance or regulation. What it already has that SF reporting reuses: *Product Registry*, *Facility registry*, *DPI-H Health Workforce Registry* (reporter credentials), *Terminology Service*, *Interoperability Component*, *Identity Management Service*, *Update Subscription/Notification*, *DPI-F Security & Consent Module*, capabilities *Recall*, *Traceability*, *Product Master Data Management*, stakeholders *Ministry of Health*, *Health Workers*, *Patients*, *Licensing Bodies*.

New elements (names follow the handbook's wording):

*Reuse, not new:* **National Regulatory Authority** (BusinessRole, altLabel "Regulator; NMRA") is added by the SC thread in draft litlfred/smart-ra#147 (`archimate/0.3.0-draft.1`). SF reuses it by id (EXISTING in a `tools/archimate-dth/add_views.py` spec) and does not define its own NMRA.

| layer | elements |
|---|---|
| Motivation | stakeholders NMRA, law enforcement and customs, health financing and procurement agencies, ICT ministry, regional/global regulators, medical product industry, professional associations; drivers and goals from §2.4 (patient safety, regulatory action, supply chain transparency); the barrier categories of Table 5 as assessments |
| Strategy | capabilities post-market surveillance, pharmacovigilance, SF case reporting, SF case investigation, regulatory enforcement (links to existing *Recall*) |
| Business | roles health care professional (reporter), NMRA reviewer, steering committee, technical working group, advisory council, project champion, digital health coordinator; processes *Report suspected SF product* (SF-REP-001), *Investigate SF report*, *Take regulatory action*, *Give feedback to reporter*, *Report to GSMS*; objects SF report, medical product alert |
| Application | SF reporting application (point-of-service, per Fig. 3), NMRA case management back end, pharmacovigilance system; external: WHO GSMS, VigiFlow/VigiBase, WHO Medical Product Alert |
| Data | SF report data object (core data elements, like CDE-HWR) |

**Shared with SC** (agreed with the dth-sc workplan, `sc-workplan.md` §5): SF defines the regulatory and pharmacovigilance elements above; SC defines the traceability data services (product verification, track and trace, traceability event data object). Both reuse the same smart-ra element IDs, so SC's "Regulatory systems" and "Quality systems" boxes point at the elements defined here.

New views, drafted together with the PC and SC views because they share the product elements:

1. **SF reporting in the DIIG EA** (layered view placing the app in Fig. 3's POS layer, with registries and the interoperability layer).
2. **SF reporting business view** (roles, processes SF-REP-001 to GSMS, information flows; replaces nothing, adds the to-be process).
3. **SF reporting application cooperation view** (app, back end, PV system, registries, external WHO systems).
4. **Regulatory governance view** (steering committee, TWG, advisory council and their relations, from §2.3).

### 2.3 dth-sfp KG (its own content)

| item | from | becomes |
|---|---|---|
| Narrative folio | all chapters | re-sectioned folio (Intro, Ch 1–7, Annexes), blocks citing L1 pages; each block linked to glossary terms and ArchiMate elements |
| DIIG phase map | Fig. 1, chapter heads | each chapter linked to its DIIG phase (table in 1.1) |
| Audience | Table 1 | chapter-to-role links (roles in smart-ra) |
| Personas | §4.1, Tables 7, 8, Annex 2 | persona instances with ISCO-08 codes; links to dth-hrh's occupation terms |
| User scenarios | Table 9 | 9 scenarios × 6 stages (discovery → follow-up) |
| Business processes | Table 10, Fig. 4, Table 9, Intro | six processes SF-REP-001 to 006, each with a BPMN 2.0 diagram (section 2.4) |
| Decision logic | Fig. 4, Tables 6, 12 | four DMN tables SFR.DT.01–04 (section 2.4) |
| Data dictionary | Table 11 | SFR.A1.DE1–DE10 as data elements; FHIR/terminology bindings left open |
| Functional requirements | Table 12 | 7 requirements (2 with IDs, 5 get IDs we assign, marked as assigned) |
| Non-functional requirements | Table 13 | about 100 rows in 11 categories (2 with IDs, rest get assigned IDs) |
| Indicators | Table 18 | measures as indicator definitions, **no targets or numbers** |
| Governance, RACI, risk | §2.3, Annex 4, Annex 7 | RACI and risk templates as structured templates |
| Barriers | Table 5, Annex 6 | barrier → candidate solution map |
| Implementation steps | Tables 14, 15, 17 | step lists linked to the narrative |

**Stays as cited L1 only (never formal content):** front matter and acknowledgements; empirical statements (the 2017 "one in ten" estimate, GSMS observations on who reports, pilot counts such as 36 reports of 27 products, the example goal "14 days to 2 days", Table 3's metrics); the Ch 7 case study; references (cross-linked to who-iris library items where held: DIIG, PHC, SC, PC handbooks).


### 2.4 BPMN, roles and DMN (owner rule, 2026-10-31)

Every DTH ingest drafts a BPMN diagram for each business process found, puts every role into a structured schema, and extracts DMN decision tables. For SFP, the smart-base DAK logical models already cover most of this, so most of it is a mechanical table-to-schema mapping rather than agentic extraction.

**Rule (owner, 2026-10-31): a DTH uses the DAK kinds** for user personas, user scenarios, business processes, data elements, requirements, indicators and decision logic. dth-sfp authors those components as DAK components, not as DTH-only structures. Enabling DAK kinds inside the DTH document kind is smart-base#242 (DTH parent thread).

**Schemas used (smart-base `input/fsh/models`)** and how mechanical each mapping is:

| handbook source | smart-base model | mapping |
|---|---|---|
| Tables 7, 8 (personas, ISCO codes); §4.1 list | `GenericPersona` / `Persona` (actor `DAK.Persona.HealthcareProvider` as parent) | mechanical: one row → one persona, ISCO code kept |
| Table 9 (9 professions × 6 stages) | `UserScenario` | mechanical: one row → one scenario, columns → stages |
| Table 10 (SF-REP-001) | `BusinessProcessWorkflow` | mechanical: columns map to name, ID, personas, objective, task set |
| Fig. 4 workflow | BPMN 2.0 XML (smart-base `bpmn_import` / `bpmn_author` skills) | redraw (F5 defects mean it cannot be traced as is) |
| Table 11 (SFR.A1.DE1–10) | `CoreDataElement` | mechanical |
| Tables 12, 13 | `FunctionalRequirement`, `NonFunctionalRequirement` | mechanical (Table 12 already uses "As a / I want / So that") |
| Table 18 | `ProgramIndicator` | mechanical, no targets |
| Decision tables below | `DecisionSupportLogic` (DMN) | mechanical where the table is given, see list |

**Schemas missing** (nothing in smart-base fits; proposed to the platform as S3 follow-ups, not built in dth-sfp): organisational role and governance body (steering committee, TWG, advisory council, project champion: these are not DAK personas); RACI matrix (Annex 4); risk register (Annex 7); barrier → solution map (Table 5, Annex 6); stakeholder analysis (Table 2); implementation step list (Tables 14, 17). Until those exist they stay as structured narrative blocks.

**Roles.** Every BPMN lane and pool binds to a role IRI, never free text: a persona from the dth-sfp persona set (which narrows a smart-base DAK persona) or a smart-ra business role (NMRA reviewer, supplier/manufacturer, law enforcement). The same role IRI is the one the ArchiMate business view uses, so the lane, the persona and the ArchiMate role are one thing.

**Business processes found and BPMN to draft:**

| ID | process | source | pools / lanes | status in source |
|---|---|---|---|---|
| SF-REP-001 | Detect and report suspected SF product | Table 10, Fig. 4, Table 9 | health care professional (one lane per persona variant where steps differ), patient, supplier/manufacturer; message flow to NMRA | given (Fig. 4, defective) |
| SF-REP-002 | Receive, acknowledge and track report (tracking number, confirmation, status updates) | Table 9 last two columns, Table 12 | NMRA, reporter | steps named, no diagram |
| SF-REP-003 | Investigate report and follow up with reporter | Intro p. 1, Table 9, Ch 7 | NMRA reviewer, reporter, laboratory | steps named, no diagram |
| SF-REP-004 | Take regulatory action (remove from supply chain, recall or withdraw, sanction, refer to law enforcement) | Intro p. 1, §2.1, §2.2 | NMRA, law enforcement/customs, supply chain (links to dth-sc recall) | steps named, no diagram |
| SF-REP-005 | Report confirmed case to WHO GSMS | Intro p. 1, Table 4 | NMRA, WHO GSMS | one sentence |
| SF-REP-006 | Submit offline and synchronise | Table 9 (paramedic), Table 13 NFRs, Ch 7 outbox | reporter, app | subprocess of SF-REP-001 |

Only SF-REP-001 has a diagram in the source. The others are drafted from the named steps only; any step the handbook does not state is marked as a gap, not filled in.

**DMN decision tables:**

| ID | decision | source | extractable? |
|---|---|---|---|
| SFR.DT.01 | Report type → path (substandard / falsified) | Fig. 4 gateways, DE8 | yes; F2 (unregistered missing) noted on the table |
| SFR.DT.02 | Product selected → product type | Table 12 ("system assigns applicable type") | yes as a lookup against the product catalogue (dth-pc) |
| SFR.DT.03 | Reporter profile → region | Table 12 SFR.FXNREQ.001 | yes as a derivation |
| SFR.DT.04 | Capability → roadmap horizon (short / medium / long) | Table 6 | yes, the table is already a decision table |
| — | Adverse reaction reported → also route to pharmacovigilance | §1.3, §2.1, DE9 | **no**: the handbook urges PV integration but gives no rule; recorded as a named decision point without logic |
| — | Risk impact × probability → priority | Annex 7 | **no**: one example row only, no rule |

Logic is only extracted where the handbook states it. Nothing is inferred.

---

## 3. Findings in the source (to record, not to fix silently)

These are recorded on the folio as review notes. None is resolved by choosing a reading.

- **F1. Two definitions of "substandard".** Glossary (ref 9, QA terminology database): "authorized by national regulatory authorities but fail to meet either national or international quality standards or specifications". Introduction (ref 23, WHA70/A70/23): "fail to meet either their quality standards or their specifications, or both". Both go in as alternatives.
- **F2. Report type omits "unregistered".** The glossary defines *unregistered* (the third WHO SF category), but the workflow and DE8 offer only substandard / falsified.
- **F3. Persona lists disagree.** §4.1 names 6 professions; Table 7 names doctor, nurse, individual; Table 8 names CHW, lab technician, pharmacist; Table 9 has 9 scenarios (adds midwife, paramedic); Annex 2 adds veterinarians.
- **F4. Missing IDs and definitions.** Only 2 of 7 functional and 2 of about 100 non-functional requirements carry IDs; DE2 (type of report) and DE5 (type of product) have no definition or value set.
- **F5. Fig. 4 is not valid BPMN.** Step 2 repeats gateway 1; gateway 1 has an unlabelled bypass to the end event; gateway 5 is labelled "Select type of report" rather than a question; step numbers 6–8 repeat on both paths. It also breaks the handbook's own Annex 3 rules. The redrawn BPMN keeps the figure as the L1 source and lists each change.
- **F6. Glossary "Registry" is truncated** ("…canonical minimum data etc.").
- **F7. Copy-paste in end-of-chapter checklists**: chapters 2–4 all say "comprehensive current state analysis".
- **F8. Undefined reference**: Table 13 cites "workstream 3 content (CQL + FHIR resources)".
- **F10. Conflicts with the smart-ra glossary** (raised as litlfred/smart-ra#139): *enterprise architecture* (SFP uses the DIIG "blueprint" wording, smart-ra the "organising logic" wording); *interoperability* (different wording and scope); *product* (smart-ra means an ArchiMate product, an offering; SFP means a health product: a homonym); *SMART Guidelines* (SFP adds "aligned with normative recommendations" and "software- and context-agnostic"). *Registry* matches smart-ra but is truncated in the handbook (F6).
- **F9.** The term comparison against the RA (`smart-base/findings/dth-terms.md`) does not cover SFP yet; step P2 runs it.

---

## 4. Steps

| step | what | where | needs |
|---|---|---|---|
| P0 | PDF into who-iris uploads (agy) | who-iris | owner/agy |
| P1 | Re-ingest by outline (chapters, sections, tables as structured blocks) | who-iris | P0 |
| P2 | Term comparison SFP vs RA and PHC/SC/PC; add clusters B to smart-ra glossary | smart-ra | S1 (smart-ra#133) |
| P3 | ArchiMate elements and 4 views, drafted with PC/SC views; link into SC's supply chain view | smart-ra | S1, S2, SC's view |
| P4 | Wire dth-sfp from the dth-hrh template (`needs: smart-ra, dth-sc`, mount who-iris) | dth-sfp | S3, S4 (smart-base#242, dth-hrh#47), dth-sc scaffold |
| P5 | Seed folio from P1 sections; domain glossary (cluster C) with links | dth-sfp | P1, P2, P4 |
| P6a | Mechanical mapping of tables to smart-base models: personas, scenarios, process matrix, data elements, requirements, indicators | dth-sfp | P1, P5 |
| P6b | BPMN for SF-REP-001 to 006, every lane bound to a role IRI | dth-sfp | P6a, P3 (roles) |
| P6c | DMN tables SFR.DT.01–04 | dth-sfp | P6a |
| P6d | Propose missing schemas (governance role, RACI, risk, barrier map, stakeholder analysis, step list) | smart-base | – |
| P7 | Link every block to glossary terms and ArchiMate elements; glossary and ArchiMate-link checks green; l1-coverage at 100 % accounted | dth-sfp | P3, P6 |

Order: SF goes last, after dth-sc (which it depends on) and dth-pc.

## 5. Rules carried

- No empirical claims in formal content: figures, statistics and country examples stay as cited L1 blocks.
- No pushes or PRs on WorldHealthOrganization repos; work only in `litlfred/dth-sfp` and `litlfred/smart-ra`.
- Ask the owner before any PR. Issues are turned off on the `litlfred/dth-*` forks, so the workplan was first filed as litlfred/smart-ra#136; it now lives on dth-sfp.
- Definition conflicts with smart-ra go to smart-ra as issues.


---
_Generated by [Claude Code](https://claude.ai/code)_
