# Decision Tables (DMN 1.3) — `dth-sfp`

Four DMN 1.3 decision tables extracted mechanically from the WHO *Digital Transformation Handbook for Substandard and Falsified Medical Product Reporting Systems* (`who-iris/library/9789240120747-eng`, `litlfred/dth-sfp#1` §2.4 Step P6c), titled as noun phrases naming the decision output (Silver, *DMN Method & Style*) with FEEL 1.3 input entries:

| Decision ID | File | Decision (Noun Phrase) | Source |
|---|---|---|---|
| `SFR.DT.01` | [`SFR-DT-01.dmn`](SFR-DT-01.dmn) | Suspected product report classification and workflow path | Fig. 4 gateways (p. 30), `SFR.A1.DE8` (Table 11, p. 31) |
| `SFR.DT.02` | [`SFR-DT-02.dmn`](SFR-DT-02.dmn) | Applicable medical product type | Table 12 `SFR.FXNREQ.006` (p. 31), National Product Catalogue (`dth-pc`) |
| `SFR.DT.03` | [`SFR-DT-03.dmn`](SFR-DT-03.dmn) | Assigned reporter geographic region | Table 12 `SFR.FXNREQ.001` (p. 31) |
| `SFR.DT.04` | [`SFR-DT-04.dmn`](SFR-DT-04.dmn) | Digital capability roadmap milestone | Table 6 (§3.1, p. 20) |

## Named Decision Points Without Rules in Source (Recorded, Not Inferred)

1. **Adverse reaction reported (`SFR.A1.DE9`) → Also route to pharmacovigilance (PV) system** (§1.3 p. 12, §2.1 p. 15, Table 11 p. 31): The handbook recommends coordination and interoperability between SF reporting and pharmacovigilance systems (`VigiFlow`/`VigiBase`), and collects adverse reaction details in `SFR.A1.DE9`, but specifies no decision rule for automatic PV co-routing.
2. **Risk impact × probability → Priority level** (Annex 7 *Risk management template*, p. 59 / PDF p. 71): Annex 7 provides a single illustrative row (`Impact: High`, `Probability: Medium`, `Priority: High`) with no scoring matrix or threshold rule.
