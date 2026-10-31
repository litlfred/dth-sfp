# Decision Tables (DMN 1.3) — `dth-sfp`

Four DMN 1.3 decision tables extracted mechanically from the WHO *Digital Transformation Handbook for Substandard and Falsified Medical Product Reporting Systems* (`who-iris/library/9789240120747-eng`, `litlfred/dth-sfp#1` §2.4 Step P6c):

| Decision ID | File | Decision | Source |
|---|---|---|---|
| `SFR.DT.01` | [`SFR-DT-01.dmn`](SFR-DT-01.dmn) | Report type and registration status → Workflow path (substandard / falsified / unregistered F2 note) | Fig. 4 gateways (p. 30), `SFR.A1.DE8` (Table 11, p. 31) |
| `SFR.DT.02` | [`SFR-DT-02.dmn`](SFR-DT-02.dmn) | Product selected → Applicable product type (`SFR.A1.DE5`) | Table 12 `SFR.FXNREQ.006` (p. 31), National Product Catalogue (`dth-pc`) |
| `SFR.DT.03` | [`SFR-DT-03.dmn`](SFR-DT-03.dmn) | Reporter profile → Assigned geographic region | Table 12 `SFR.FXNREQ.001` (p. 31) |
| `SFR.DT.04` | [`SFR-DT-04.dmn`](SFR-DT-04.dmn) | Capability area × horizon → Investment roadmap milestone | Table 6 (§3.1, p. 20) |

## Named Decision Points Without Rules in Source (Recorded, Not Inferred)

1. **Adverse reaction reported (`SFR.A1.DE9`) → Also route to pharmacovigilance (PV) system** (§1.3 p. 12, §2.1 p. 15, Table 11 p. 31): The handbook recommends coordination and interoperability between SF reporting and pharmacovigilance systems (`VigiFlow`/`VigiBase`), and collects adverse reaction details in `SFR.A1.DE9`, but specifies no decision rule for automatic PV co-routing.
2. **Risk impact × probability → Priority level** (Annex 7 *Risk management template*, p. 59 / PDF p. 71): Annex 7 provides a single illustrative row (`Impact: High`, `Probability: Medium`, `Priority: High`) with no scoring matrix or threshold rule.
