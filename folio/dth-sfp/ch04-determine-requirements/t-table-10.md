### Table 10. Business process matrix SF-REP-001 (p. 29 / PDF p. 41)

| Process name | Process ID | Personas | Objectives | Task set |
| --- | --- | --- | --- | --- |
| *Title* | *ID used to reference this process* | *Individuals interacting to complete the process* | *A concrete statement describing what the process seeks to achieve* | *The general set of activities performed within the process* |
| Suspect product detection and reporting by pharmacist | SF-REP-001 | Pharmacist, patient (optional), supplier/manufacturer, regulatory authority | To enable pharmacists to promptly identify, isolate, document and report suspected substandard or falsified medical products to regulatory authorities using a digital system. | 1. Identify anomalies in medication appearance, packaging, or reported effectiveness.<br>2. Isolate the product and verify with supplier/manufacturer if needed.<br>3. Advise the patient, if applicable.<br>4. Log into the digital reporting tool.<br>5. Enter product and incident details, including optional patient info and photos.<br>6. Submit the report and receive confirmation.<br>7. Receive tracking number and follow-up communication from the authority. |

> [!NOTE]
> **Source Table Review Notes (`litlfred/dth-sfp#1` §3):**
> - F2: Report type in Fig. 4 (p. 30) omits 'unregistered/unlicensed medical products' (the third WHO SF category defined on p. ix and p. 1), offering only substandard and falsified branches.
> - F5: Fig. 4 (p. 30 / PDF p. 42) has 5 BPMN 2.0 defects: (1) step 2 repeats gateway 1 ('Is the product registered?'); (2) gateway 1 has an unlabelled bypass arrow to the end event; (3) gateway 5 is labelled 'Select type of report' (imperative task label) rather than a question; (4) step numbers 6, 7, 8 repeat on both parallel paths; (5) symbol usage violates Annex 3 rules. Redrawn cleanly in processes/SF-REP-001.bpmn while keeping Fig. 4 as the cited L1 figure.
