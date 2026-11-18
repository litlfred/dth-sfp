# dth-sfp ArchiMate overlay

A DTH builds an **overlay** on the smart-ra (DPI-H RA) ArchiMate model and does not add to that model (owner, 2026-11-01, card Q-RA1 A; [dth-sfp#7](https://github.com/litlfred/dth-sfp/issues/7)). The one exception is a real conflict between a DTH and smart-ra terms or models: then an issue goes to smart-ra and to the DTH.

| Version | File | Overlays smart-ra | Draws from dth-phc |
|---|---|---|---|
| 0.1.0-draft.1 | [`0.1.0-draft.1/dth-sfp-overlay.archimate`](0.1.0-draft.1/dth-sfp-overlay.archimate) | 0.3.0-draft.1 | 0.1.0-draft.1 |

It holds the four substandard and falsified (SF) reporting views: SF Reporting in the DIIG Enterprise Architecture (Fig. 3), SF Reporting Business Process View (Fig. 4 and SF-REP-001..006), SF Reporting Application Cooperation View, and SF Reporting Regulatory Governance View (§2.3).

Each element carries one of three tags:

- `overlay:owner` = `dth-sfp`: an element this DTH adds (41 elements, 131 relationships, 4 views). The folio links it with a `https://litlfred.github.io/dth-sfp/archimate/<version>/…` IRI.
- `overlay:base`: a reference copy of a smart-ra element, under the same id, with its smart-ra IRI as the value. It is there only so the overlay's views can draw it.
- `overlay:dth`: a reference copy of an element another DTH's overlay owns, with that overlay's IRI as the value. Only dth-phc so far: *Point-of-service application* (which the SF Reporting Application specializes, Fig. 3), *Health worker* (a candidate match of Health Care Professional (Reporter)), and two Serving relationships into the Interoperability Component.

`bun run check:dth-glossary` fails when a reference copy names something smart-ra does not hold, when an owned element is already in smart-ra, or when a folio link does not resolve in the pinned model or this overlay. It does not open the dth-phc overlay, which is not mounted here. `scripts/archimate/extract_overlay.py` built 0.1.0-draft.1 from the SFP work that was once in smart-ra#182 (`tools/archimate-dth/dth_sfp.py` on branch `feat/133-phc-pcposs-archimate-view`, c984026).
