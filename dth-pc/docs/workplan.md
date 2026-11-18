# Workplan: product catalogue handbook as an L2 DTH (dth-pc)

*Source:* Digital transformation handbook for health product catalogue, WHO 2025, ISBN 9789240116191 (L1 entry `litlfred/who-iris` `library/9789240116191-eng`).
*Target repo:* `litlfred/dth-pc` (empty today: one `.gitignore` commit). *Shared target:* `litlfred/smart-ra`.
*Depends on:* **dth-sc** (owner, 2026-10-31: "dth-pc and probably dth-sfp depends on dth-sc"). dth-pc mounts dth-sc as well as smart-ra and who-iris. See the SC workplan (project file sc-workplan.md).
*Builds on:* the five-DTH workplans (project file workplans.md) (split rule, S1–S4) and the agreed order A (dth-hrh pilot first: dth-hrh#47, smart-ra#133, smart-base#242).
*Governing skills:* folio-assistant-core `l1-document-ingestion`, `l1-coverage`, `glossary-terms`; cat-harness `term-disagreement`, `archimate-models`.
*Convention (owner, 2026-10-31):* a term that is a concept in the KG is written Capitalized (Product Master Data, Trade Item, Generic Product); a plain-English use stays lower case.
*Status:* approved by the owner 2026-10-31 (option A). Section 2e, PC-8 and Q6 added and approved 2026-10-31 (Q6 A).

## 1. What the L1 entry holds (review)

| item | finding |
|---|---|
| Size | 62 pages, 131 KB text; 62 page sections (124 files = .md + .jsonld), 63 blocks (62 prose + 1 figure), 15 vector figures |
| Segmentation | **page-granular, `toc_source: none`.** No chapter or step outline. The printed contents (p.4) gives 8 chapters + glossary + annexes, so an outline can be rebuilt. This must happen before seeding a folio. |
| Front matter | p.3 licence (CC BY-NC-SA 3.0 IGO), p.5 acknowledgements, p.6–7 abbreviations (52), p.8–9 glossary (17 terms) |
| Introduction | p.10–19: Product Master Data (Fig 1, 2), effect of inconsistent identifiers (Fig 3), DIIG phases (Fig 4), SMART Guidelines L1–L5 (Fig 5), ANC workflow touchpoints (Fig 6), DHSC architecture framework (Fig 7), how to use, target users table |
| Ch 1 Regulatory policies | p.20–23: 4 steps (identify, develop, review/approve, publish/enforce) |
| Ch 2 Data management and governance | p.24–33: 5 steps; Data Owner / Data Custodian / Data Steward roles; classification → Generic Product → Trade Item → Regulated Trade Item model with cardinalities (Fig 8, 9); Packaging Hierarchy (Fig 10–12); coding best practices; WHODrug |
| Ch 3 Technology | p.34–37: 4 steps (requirements, select tool, plan, design/build/deploy) |
| Ch 4 Change management | p.38–41: 2 steps; local identifier → GTIN transition (Fig 13) |
| Ch 5 Capacity | p.42–44: 3 steps; Catalogue Manager role |
| Ch 6 WHO-hosted PCMT | p.45–47: global vs country catalogues, access model (Fig 14) |
| Ch 7 Global good | p.48–50: sharing with WHO Global Catalogue (Fig 15) |
| Ch 8 Country experiences | p.51–54: Rwanda, Zambia, Nigeria tables |
| Annexes | p.56 Principles for Digital Development; p.57–61 roles (project manager, solution architect, business analyst, developer, DBA, infrastructure specialist, QA/test manager, test analyst, system admin, support engineer) |
| Normative markers | 55 hits of should/shall/must/recommend*, on 25 pages. Many are in the licence page (7) and glossary (6), so the real normative set is smaller. |

**L1 defects to fix in who-iris first** (litlfred/who-iris only):
1. Rebuild the outline (chapters, steps, figures) from p.4 so blocks are chapter- and step-scoped, not page-scoped.
2. p.50 carries the wrong running header (Chapter 1's title on a Chapter 7 page), which will mislabel the block.
3. Step tables (INPUTS / STEPS / RESOURCES / OUTPUTS / RISKS / MITIGATION) are flattened into running text. They need to be re-extracted as tables, or the step structure is lost.
4. Fig 9 and Fig 12 (FHIR mapping) are only partly text; check the vector figures carry them.
5. Abbreviation "AEFI" is expanded as "Adverse effects following immunisation"; the usual WHO expansion is "events". Record as a term disagreement, do not silently change the source.

## 2. The split: what goes where

### 2a. smart-ra (shared, done once)

**Glossary (SKOS scheme, task S1).** PC terms that are shared across DTHs go into smart-ra, with PC wording kept as a cited alternative (as in smart-base `findings/dth-terms.md`, which already compares PC with PHC, SC and the RA):

| term | why shared | note |
|---|---|---|
| Registry | identical sense in PHC, SC, PC, RA | 4 near-identical wordings; one concept |
| Trade Item | used by SC and PC | PC has 2 senses: glossary (GS1, "priced, ordered or invoiced") and body ("manufacturer-specific branded"). Keep both as alternatives; owner picks |
| Product Master Data | SC and PC | one concept (owner 2026-10-31: no homonym split needed) |
| Interoperability, Open source, Open standards, Digital transformation / digitization / digitalization, Functional / non-functional requirements, Features, End user, UAT, SMART Guidelines, Data element, Organogram | generic, in several DTHs | cited alternatives only; nothing chosen |

**ArchiMate (one model, `smart-ra/archimate/`).** smart-ra 0.2.0 (564 elements, 20 views) already has: Product Registry, Product Catalog Management System, Product Master Data Management (capability), Supplier registry, Facility registry, DPI-F Information Mediator, Terminology Service, Traceability, Recall, Product Traceability (service), Warehouse Management System, Procurement Management System, Health Facility Logistics Management System, Supplier role, Warehouse role, "Health Product Data?" (data object, name has a question mark). **No product catalogue view exists.**

Proposed additions (reuse first, mint only what is missing):
- **New view: "National Product Catalogue"** (drafted with the SC thread, which owns the DHSC framework view). Shows Product Registry realised by Product Catalog Management System; serving forecasting, procurement, warehouse, dispensing, recall and traceability; exchange through the Information Mediator; GTIN sourcing from an external data pool; the NRA as source of regulatory data.
- **New business objects:** Product Classification, Generic Product, Trade Item, Regulated Trade Item, Packaging Level. Rename or replace "Health Product Data?" once the owner decides.
- **New roles / stakeholders:** Data Owner, Data Custodian, Data Steward, Catalogue Manager, Master Data Governance Group, National regulatory authority (stakeholder), Manufacturer / distributor (source of truth).
- **Optional second view: "WHO-hosted PCMT, global and country catalogues"** (Ch 6–7). Only if the owner wants WHO-hosted services in the RA; see open question Q3.
- Shared with SC (agreed 2026-10-31 with the "Plan supply chain handbook KG" thread, see sc-workplan.md section 5): SC drafts the DHSC framework view, PC drafts the National Product Catalogue view; PC owns Product Registry, Product Catalog Management System, Product Master Data Management and Supplier registry, and SC reuses those IDs; PC proposes the new product / Trade Item objects and data roles and SC reuses them; one combined smart-ra PR for both views.

### 2b. dth-pc (its own content)

- **Declaration and wiring** copied from dth-hrh once S4 lands: `dth-pc.json`, `index.config.json` mounting who-iris, smart-ra and dth-sc, `extends` the L2 DTH kind from smart-base#242.
- **Narrative folio** `folio/dth-pc/`, seeded from the re-segmented L1: one chapter per handbook chapter, one section per step. Prose blocks quote or paraphrase with a source link to the L1 block.
- **Domain glossary** `dth-pc.glossary.json`, PC-only terms, each linked to the smart-ra concept it narrows or matches: Generic Product (National Product Code), Trade Item (narrows shared Trade Item), Regulated Trade Item, Country Trade Item Identifier, Product Classification, Packaging Hierarchy, Quantity of Eaches, Unit of Use, catalogue (global / country), Catalogue Manager, Data Owner / Data Custodian / Data Steward, Master Data Governance Group, National Product Catalogue (NPC), PCMT, master data guideline.
- **Conceptual information model** (Fig 8–9): classification → Generic Product → Trade Item → Regulated Trade Item, with the cardinalities printed on p.29, as a `table` + `diagram` block. It is a structural model taken from the text, not an empirical claim. Its elements link to the smart-ra business objects above. The FHIR mapping (InventoryItem, Fig 12) is recorded as a link to the future L3 IG, not modelled here.
- **Step structure** (Ch 1–5): each step's inputs, outputs, resources, risks and mitigations as a `table` block per step, so the output chain (e.g. "standardized master data coding schemes" made in Ch 2 step 2, used in Ch 3 step 1 and Ch 4 step 1) is traceable. See Q2 on whether these also become ArchiMate work packages.
- **Best practices** (p.29 coding rules, p.39 local-identifier → GTIN rule, p.41 minimum attribute set) captured as normative statements, using the `normative-statements` skill, with source links.
- **Links from narrative to architecture:** every block that names a component (NPC, Product Registry, mediator, WMS, eLMIS, GDSN, PCMT) links to the smart-ra element or view. The platform QA check from S3 enforces it.

### 2d. What changes because dth-pc depends on dth-sc

- **Mounts:** dth-pc's `index.config.json` mounts who-iris, smart-ra **and dth-sc**. dth-pc is wired after dth-sc, so PC-4 waits on SC's wiring step too.
- **Terms resolve through dth-sc first:** supply chain terms that SC defines (traceability, track and trace, product verification, the foundational components, the SCISMM levels) are not redefined in dth-pc. A dth-pc term that narrows one of them links to the dth-sc term, which links on to smart-ra. Only terms the PC handbook introduces itself stay in `dth-pc.glossary.json`.
- **Views:** PC's "National Product Catalogue" view is drawn as a refinement of the Product Registry box in SC's DHSC framework view, and links back to it.
- **Definition conflicts go to smart-ra as issues.** Where PC wording disagrees with a smart-ra or dth-sc definition (known now: Trade Item has two PC senses; Registry has four near-identical wordings; Open Standards differs between the PC glossary and the full-STAC paper; AEFI expansion), they are raised on litlfred/smart-ra in one combined issue (as SC did in #140 and SF in #139), using the `term-disagreement` outcomes (change-prose, local-term, vocabulary-wrong). Nothing is chosen in dth-pc while an issue is open. Check litlfred/smart-ra#140 (SC's conflict issue, traceability) first and comment there instead of opening a duplicate where a term overlaps.

### 2c. Kept as cited L1 source blocks only (never formal)

These are empirical or time-bound and stay out of glossary definitions and the model:
- Ch 8 country figures (Rwanda 7134 products / 2611 with GTINs; Zambia 7414 / 551; Nigeria 6517 / 794; dates 2019–2024; "29 mandatory attributes").
- "WHODrug … from nearly 150 countries", "DH&I WG … over 250 individuals", "WHO-hosted PCMT will be available in 2026".
- Acknowledgements, funding statement, licence text.
- The Fig 4 DIIG phase figure: per `dth-terms.md`, it has one source (the DIIG); dth-pc cites the DIIG rendering, does not re-draw it.

### 2e. Business processes, roles and decision tables (owner, 2026-10-31: every DTH workplan)

*Status: approved by the owner 2026-10-31 (Q6 option A).*

Every process the handbook describes gets a BPMN 2.0 diagram. The lanes are roles, every role is a structured record, and every decision rule the handbook states is extracted as a DMN decision table. Rules for all three:

- **Only what the source says.** A lane, task, gateway or rule cites its L1 page. Where the handbook names no performer for a step, the task goes in an `unassigned` lane and is flagged for the owner; it is not guessed.
- **No empirical content.** Counts, dates and country figures never become a task, a condition or a role.
- **Process ids** are `PC-BP-nn`, **decision ids** `PC-DT-nn`, **role ids** `PC-R-nn`. They are this handbook's, and they link to the smart-ra ArchiMate business process, role and object they realise (PC-3).

**Processes found (10).** Chapters 1–5 are written as numbered steps with INPUTS / STEPS / RESOURCES / OUTPUTS / RISKS / MITIGATION tables. Each chapter becomes one process, with one task per step; inputs and outputs become data objects, so the output chain across chapters is a set of message and data flows.

| id | process | source | lanes (roles) | where |
|---|---|---|---|---|
| PC-BP-01 | Establish regulatory policies for Product Master Data (4 steps: identify, develop, review and approve, publish and enforce) | Ch 1, p.21–23 | National Regulatory Authority, Ministry of Health, Manufacturer / Distributor, Master Data Governance Group | dth-pc |
| PC-BP-02 | Establish master data management and governance (5 steps) | Ch 2, p.25–33 | Data Owner, Data Custodian, Data Steward, Master Data Governance Group | dth-pc |
| PC-BP-03 | Add or update a product record, with approval | p.26 (Data Owner "approves changes"), p.40 ("data approval workflows within the NPC") | Data Steward (submits), Data Owner (approves), Data Custodian (applies) | dth-pc |
| PC-BP-04 | Assign a Country Trade Item Identifier and move to GTIN | p.39, Fig 13 | Catalogue Manager, Manufacturer | dth-pc (decision PC-DT-01) |
| PC-BP-05 | Distribute Product Master Data to downstream systems on add or update | p.39 ("event triggers such as data additions and updates") | Catalogue Manager; consuming systems as participants (eLMIS, WMS, procurement) | dth-pc, linked to dth-sc's supply chain processes |
| PC-BP-06 | Select, plan and deploy the National Product Catalogue tool (4 steps) | Ch 3, p.35–37 | unassigned (flagged: the chapter names no performer) | dth-pc |
| PC-BP-07 | Institutionalise use of the National Product Catalogue: change plan and SOPs (2 steps) | Ch 4, p.39–41 | unassigned (flagged) | dth-pc |
| PC-BP-08 | Build human resource capacity (3 steps) | Ch 5, p.43–44 | Catalogue Manager; others unassigned | dth-pc |
| PC-BP-09 | Derive a country catalogue from the Global Catalogue (associate or copy a product) | p.46–47, Fig 14 | Country user group, WHO user group | tool-neutral BPMN in dth-pc; the PCMT access model in smart-pcmt (Q3) |
| PC-BP-10 | Share country Product Master Data with the WHO Global Catalogue | p.49–50, Fig 15 | Country (WHO-hosted or in-country tool), WHO | dth-pc |

**Roles (structured).** Each role is one record with an id, a label, its responsibilities quoted from the source, the processes it acts in, and its smart-ra ArchiMate business role.

| id | role | source | goes to |
|---|---|---|---|
| PC-R-01 | Data Owner | p.26 | dth-pc glossary + record; ArchiMate role in smart-ra |
| PC-R-02 | Data Custodian | p.26 | same |
| PC-R-03 | Data Steward | p.26 | same |
| PC-R-04 | Master Data Governance Group | p.25 | same |
| PC-R-05 | Catalogue Manager | p.43 | same |
| PC-R-06 | National Regulatory Authority | p.21 | stakeholder; reuse dth-sc / smart-ra if present |
| PC-R-07 | Manufacturer / Distributor ("source of truth for product master data") | p.21 | stakeholder; reuse dth-sc if present |
| PC-R-08 | Ministry of Health | p.21–22 | stakeholder; reuse smart-ra |
| PC-R-09 | WHO user group, country user group | p.47 | smart-pcmt (PCMT-specific) |
| PC-R-10 … 19 | Annex project roles: project manager, solution architect, business analyst, developer, DBA, infrastructure specialist, QA / test manager, test analyst, system admin, support engineer | p.57–61 | smart-ra (shared with other DTHs); dth-pc cites them |

**Decision tables.** Only rules the handbook states as conditions become DMN.

| id | decision | inputs → output | source | where |
|---|---|---|---|---|
| PC-DT-01 | Trade Item identifier | GTIN assigned? → Country Trade Item Identifier = the GTIN, or a generated local identifier, replaced by the GTIN once assigned | p.39, Fig 13 | dth-pc |
| PC-DT-02 | Attribute catalogue | attribute group → Global Catalogue (global identifier, Unit of Use, pharmaceutical information, Trade Item information, manufacturer, country of origin, shelf life) or country catalogue (country identifiers, registration number) | Fig 14, p.46 | dth-pc |
| PC-DT-03 | Catalogue access | user group × catalogue → view / edit / own | p.47 | smart-pcmt (PCMT-specific) |

Not decision tables: the coding rules on p.29 (sequential code, uniform length, characteristics as attributes) are constraints on a code, so they stay normative statements and become validation rules on the information model. The change approval in PC-BP-03 has no stated conditions in the source, so it stays a single approval task with no DMN.

**Schema gaps this exposes (Q6).** The `document` kind allows `diagram` and `table` but not the DAK block kinds smart-base already has: `persona`, `actor-definition`, `business-process` (with a `.bpmn` companion) and `decision-logic` (with a `.dmn` companion). There is also no schema for the step table that Ch 1–5 repeat (INPUTS / STEPS / RESOURCES / OUTPUTS / RISKS / MITIGATION), so today that structure can only be extracted by an agent. With a step schema, PC-BP-01, 02 and 06–08 can be generated from the tables mechanically.

## 3. Coverage

Run `l1-coverage` on the re-segmented entry. Expect most of the 55 markers to be accounted for as: captured (best practices, step obligations), `editorial` (licence page), or `background-fact` (glossary, case studies). Exclusions are proposed by the agent and signed off by the owner only. Target 100 % accounted-for.

## 4. Work items, in order

| # | where | item | depends on |
|---|---|---|---|
| PC-1 | who-iris | Rebuild outline (34 chapter/step sections), re-extract 18 step tables + reference tables, fix p.50 running header, verify Figs. 8–12 & HL7 FHIR R5 mappings (**DONE** on `litlfred/who-iris#7`, mounted at `f98ec83a5`) | — |
| PC-2 | smart-ra | Add shared PC terms to the SKOS scheme as alternatives (**DONE** on `smart-ra#147`) | S1 (smart-ra#133) |
| PC-3 | smart-ra | Add business objects and roles; "National Product Catalogue" (`id-02175c6feb9155618981ff120f954420`) and "Product Master Data Information Model" (`id-053fa0e33f6b5b0bb218195486c05160`) views (**DONE** on `smart-ra#147`) | S2, SC thread |
| PC-0 | smart-ra | Definition conflicts issue (Trade Item, Registry wording, Open Standards, AEFI) (**DONE** on `smart-ra#142`) | — |
| PC-4 | dth-pc | Wire repo from the dth-hrh template, mounting `dpi-h-ra` (`smart-ra@2c01ca033`), `dth-sc` (`dth-sc@f291f3642`), and `who-iris` (`who-iris@f98ec83a5`) (**DONE** on #1) | S4 (dth-hrh#47), smart-base#242, dth-sc wiring |
| PC-5 | dth-pc | Seed folio from PC-1, domain glossary (16 terms), information model & HL7 FHIR R5 resource attribute mappings (`t-ch02-fig-8-linkage`, `t-ch02-fig-9-information-model`, `t-ch02-fig-11-packaging-variations`, `t-ch02-fig-12-fhir-packaging`), 18 step tables (`t-ch01-step-1`..`t-ch05-step-3`), reference/country tables (33 `t-*` tables total), 15 vector figure blocks (`f-*`, `fig:1`..`fig:15` + `media/vfig-p*.png`), and best practices (**DONE** on #1) | PC-1, PC-4 |
| PC-6 | dth-pc | Link narrative, tables, figures, roles, processes, and decisions to glossary and ArchiMate; run glossary validator (`bun run check:dth-glossary`) and link QA (**DONE** on #1: 16 terms matched across `dpi-h-ra` and `dth-sc`; 126 blocks with 624 glossary links, 818 ArchiMate 0.3.0-draft.1 links, and 18 figure-view mappings) | PC-2, PC-3, PC-5, S3 |
| PC-7 | dth-pc | `l1-coverage` (`bun run check:l1-coverage`, `folio/dth-pc/l1-coverage.json`, `docs/l1-coverage.md`) to **100 % accounted-for** across all 34 L1 sections / 47 normative sentences (57 marker hits: 34 captured in folio blocks, 8 `editorial`, 5 `background-fact` signed off by `litlfred`, 0 unaccounted) (**DONE** on #1) | PC-5 |
| PC-8 | dth-pc (+ smart-pcmt for BP-09 access, DT-03) | Draft the 10 BPMN diagrams (`processes/PC-BP-01.bpmn`..`PC-BP-10.bpmn` + `bp:pc-bp-01`..`10` + rendered `folio/dth-pc/media/bp-pc-bp-01.svg`..`10.svg`), the 19 role records (`PC-R-01`..`19` as `pers:pc-r-01`..`19`) and the 2 dth-pc DMN tables (`decisions/PC-DT-01.dmn`, `PC-DT-02.dmn` + `dt:pc-dt-01`, `dt:pc-dt-02`) of section 2e; flag every unassigned lane (`PC-BP-06`, `PC-BP-07`, `PC-BP-08`) for the owner (**DONE** on #1; `PC-DT-03` is smart-pcmt scope per Q3) | PC-1 (step tables), PC-3 (ArchiMate roles), Q6 |

PC-0 and PC-1 can start now. PC-2 to PC-7 wait for the dth-hrh pilot (order A) and for dth-sc's glossary and view (SC2, SC3).

## 5. Open questions for the owner

- **Q1 Trade Item sense: DECIDED (owner, 2026-10-31).** Trade Item is the WHO concept with the narrow sense (manufacturer-specific branded health products, p.28). The GS1 trade item is a separate external concept, linked as `broadMatch`. The glossary's GS1 sentence (p.9) is recorded as a note citing GS1.
- **Q2 Step tables: DECIDED (owner, 2026-10-31): A.** Tables in dth-pc only; no ArchiMate work packages.
- **Q3 WHO-hosted PCMT: DECIDED (owner, 2026-10-31): A.** Modelled in smart-pcmt (downstream of dth-pc) as a KG derived from the published FHIR IGs (e.g. smart.who.int/pcmt-vaxprequal); proprietary sources recorded as referenced sources, never copied. No RA view. Plan: litlfred/smart-ra#145.
- **Q4 Medical devices: DECIDED (owner, 2026-10-31): A.** Scope note on the National Product Catalogue view and the dth-pc glossary.
- **Q6 Block kinds for processes, roles and decisions: DECIDED (owner, 2026-10-31): A.** A: the L2 DTH kind (smart-base#242) admits smart-base's DAK kinds `persona`, `actor-definition`, `business-process` (.bpmn) and `decision-logic` (.dmn), plus a new shared step-table schema (recommended: one schema for every DTH, and the step tables become mechanical). B: draw them as `diagram` and `table` blocks with the .bpmn and .dmn files beside them, no new schema. C: keep processes, roles and decisions out of the DTH, in a DAK-shaped repo.
- **Q5 Workplan issue: DONE.** litlfred/dth-pc#2, moved from smart-ra#141 (on smart-ra: conflicts #142, full-STAC proposal #143, smart-pcmt plan #145).
