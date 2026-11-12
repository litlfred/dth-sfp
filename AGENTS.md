# AGENTS.md — Digital Transformation Handbook for Substandard and Falsified Medical Product Reporting Systems

This is a **folio**: the L2 content repository for the WHO *Digital Transformation Handbook for Substandard and Falsified Medical Product Reporting Systems* (Geneva: World Health Organization; 2026; ISBN 978-92-4-012074-7; IRIS handle [`10665/384624`](https://iris.who.int/handle/10665/384624)).

The authoring platform (`folio-assistant`), reference architecture (`dpi-h-ra`), sibling DTH glossaries (`dth-sc`, `dth-pc`, `dth-hrh`), DAK schemas (`smart-base`), and L1 source (`who-iris`) are **remote-mounted** at the repository root from the SHAs pinned in `index.lock.json` (all gitignored). The session-start hook mounts them; by hand: `bun run cat-harness-tools/scripts/remote-mount.ts` or `bun run cat-harness-tools/scripts/mount-from-lock.ts`.

This file is the **agent-generic** source of truth, read natively by Claude Code, Gemini CLI, Antigravity, Cursor and Copilot. `CLAUDE.md` and `GEMINI.md` are thin stubs pointing here.

## Instance graph and dependencies

`dth-sfp.json` declares `needs: ["dpi-h-ra", "dth-sc", "dth-pc", "dth-hrh", "smart-base", "who-iris"]`:

- **`dpi-h-ra`** (`litlfred/smart-ra`, mounted with `glossary/` and `archimate/`): WHO/ITU DPI-H Reference Architecture glossary (`dpi-h-ra` and `full-stac`) and ArchiMate 0.3.0-draft.1 views and elements.
- **`dth-sc`** (`litlfred/dth-sc`, mounted with `glossary/`): supply chain architecture and traceability concepts (`batch-number`, `expiry-date`, `product-master-data`, `pharmaceutical-supply-chain`, `track-and-trace`, `traceability`, `recall`, `verification`, `dispense`, `gs1`, `global-trade-item-number`, `serial-number`, `national-regulatory-authority`, `authorized-trading-partners`, `logistics-management-information-system`, `electronic-health-record`, `visibility-and-analytics-network`).
- **`dth-pc`** (`litlfred/dth-pc`, mounted with `glossary/`): product catalogue and regulatory concepts (`medical-product`, `substandard-medical-product`, `falsified-medical-product`, `unregistered-unlicensed-medical-product`, `adverse-drug-reaction`, `pharmacovigilance`, `stringent-regulatory-authority`, `regulatory-authority`, `marketing-authorization-holder`, `national-product-catalogue`, `manufacturer`, `product-identifier`).
- **`dth-hrh`** (`litlfred/dth-hrh`, mounted with `glossary/`): health workforce and occupation concepts (`occupation`, `international-standard-classification-of-occupations`, `health-professional`, `health-workforce`, `community-health-workers`, `human-resources-for-health-information-system`, `health-worker-registry`).
- **`smart-base`** (`litlfred/smart-base`): DAK artefact schemas (`persona`, `user-scenario`, `business-process`, `data-element`, `decision-table`, `indicator`, `functional-requirement`, `non-functional-requirement`) and DTH skills (`dth-authoring`, `dth-l1-to-l2-ingest`, `dth-archimate-patterns`, `dth-workplan`).
- **`who-iris`** (`litlfred/who-iris`): frozen L1 source at `who-iris/library/9789240120747-eng/` (72 PDF page sections and 6 extracted vector figures).

## What goes where (the split rule)

| goes in | what |
|---|---|
| **`smart-ra` (`dpi-h-ra`)** | shared digital health & enterprise architecture glossary (`dpi-h-ra` / `full-stac`); the shared ArchiMate model, which a DTH never adds to |
| **`dth-sc` / `dth-pc` / `dth-hrh`** | supply chain & traceability terms (`dth-sc`), medical product quality/safety & product catalogue terms (`dth-pc`), and health workforce / ISCO-08 occupation terms (`dth-hrh`) |
| **here (`dth-sfp`)** | the L2 narrative folio (`folio/dth-sfp/`); SF reporting domain terms (`glossary/dth-sfp.glossary.json`); DAK personas, user scenarios, data elements (`SFR.A1.DE1`–`DE10`), functional & non-functional requirements (`SFR.FXNREQ.001`–`007`, `SFR.NFXNREQ.*`), indicators, 6 BPMN 2.0 processes (`processes/SF-REP-001.bpmn`..`SF-REP-006.bpmn`), 4 DMN 1.3 decision tables (`decisions/SFR-DT-01.dmn`..`SFR-DT-04.dmn`), and 100% L1 normative coverage (`folio/dth-sfp/l1-coverage.json`); the SF reporting ArchiMate overlay on smart-ra (`archimate/`) |

**No empirical claims in formal content.** Country pilot vignettes (Chapter 7: Indonesia and United Republic of Tanzania) stay as cited L1 source text (`meta.sourceOnly: true`) and never become formal requirements, decision rules, or indicator targets.

**ArchiMate overlay, not model additions (`archimate/`).** dth-sfp builds an overlay on smart-ra's ArchiMate model and never adds elements to smart-ra (owner, 2026-11-01, Q-RA1 A). Its own elements are tagged `overlay:owner=dth-sfp` and are linked with `https://litlfred.github.io/dth-sfp/archimate/<version>/…` IRIs. A smart-ra element the overlay draws is a reference copy tagged `overlay:base`; a dth-phc overlay element it draws is a reference copy tagged `overlay:dth`. A real conflict with a smart-ra term or model goes to an issue on smart-ra AND on dth-sfp. See [`archimate/README.md`](archimate/README.md).

**Never push to or open PRs on `WorldHealthOrganization/*`.** Work happens in `litlfred/dth-sfp`.

## Validation and build commands

```sh
bun run check:dth-glossary   # SKOS + cross-instance glossary & ArchiMate link validation
bun run check:l1-coverage    # 100% normative sentence coverage against who-iris/library/9789240120747-eng
bun run kg:blocks            # extract block KG
bun run check:kg-blocks      # validate block KG and DAK artefacts
bun run check:library-kg     # validate library citations
bun run site:glossary        # build glossary site
bun run site:document        # build standalone L2 document site
```
