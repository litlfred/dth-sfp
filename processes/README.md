# Business Processes (BPMN 2.0) — `dth-sfp`

Six BPMN 2.0 business processes drafted from the WHO *Digital Transformation Handbook for Substandard and Falsified Medical Product Reporting Systems* (`who-iris/library/9789240120747-eng`, `litlfred/dth-sfp#1` §2.4 Step P6b):

| Process Code | File | Title | L1 Source | Swimlanes |
|---|---|---|---|---|
| `SF-REP-001` | [`SF-REP-001.bpmn`](SF-REP-001.bpmn) | Detect and report suspected SF medical product | Table 10 (p. 29), Fig. 4 (p. 30, redrawn with F5 fixes), Table 9 (pp. 27–28) | `pers:sfp-r-01`..`12`/`14`, `pers:sfp-r-13` |
| `SF-REP-002` | [`SF-REP-002.bpmn`](SF-REP-002.bpmn) | Receive, acknowledge and track SF report | Table 9 stages 5–6 (pp. 27–28), Table 12 (`SFR.FXNREQ.001`–`007`, p. 31) | `pers:sfp-r-13`, `pers:sfp-r-01` |
| `SF-REP-003` | [`SF-REP-003.bpmn`](SF-REP-003.bpmn) | Investigate SF report and follow up with reporter | Intro (p. 1), Table 9 stage 6 (pp. 27–28), Ch. 7 (p. 47) | `pers:sfp-r-13`, `pers:sfp-r-01`, `pers:sfp-r-05` |
| `SF-REP-004` | [`SF-REP-004.bpmn`](SF-REP-004.bpmn) | Take regulatory action on confirmed SF product | Intro (p. 1), §2.1 (p. 15), §2.2 (p. 16) | `pers:sfp-r-13`, `pers:sfp-r-14`, `pers:sfp-r-15` |
| `SF-REP-005` | [`SF-REP-005.bpmn`](SF-REP-005.bpmn) | Report confirmed SF case to WHO GSMS | Intro (p. 1), Table 4 (p. 12) | `pers:sfp-r-13`, `pers:sfp-r-15` |
| `SF-REP-006` | [`SF-REP-006.bpmn`](SF-REP-006.bpmn) | Submit SF report offline and synchronise | Table 9 (Paramedic, p. 28), Table 13 NFRs (pp. 32–35), Ch. 7 (p. 47) | `pers:sfp-r-09`, `pers:sfp-r-13` |
