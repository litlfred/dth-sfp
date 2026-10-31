# Receive, acknowledge and track SF report (SF-REP-002) — BPMN 2.0 Verification Checklist

- **Process ID:** `Process_SF_REP_002` (`SF-REP-002`)
- **L1 Source Sections:** `sec-023, sec-025, sec-026` (PDF pages 39, 40, 43)
- **Swimlanes bound to DAK Personas / ArchiMate Roles:**
  - `Lane_SF_REP_002_NMRA` → `pers:sfp-r-13` (`partitionElementRef="sfp-r-13"`) — NMRA Case Management System & Reviewer (SFP-R-13)
  - `Lane_SF_REP_002_Reporter` → `pers:sfp-r-01` (`partitionElementRef="sfp-r-01"`) — Reporter (SFP-R-01..SFP-R-12, SFP-R-14)

## Narrative Summary

Workflow for receiving an SF report, generating a unique tracking number, sending confirmation to the reporter, notifying the NMRA focal point, and serving status updates, drafted from Table 9 stages 5-6 (pp. 27-28 / PDF pp. 39-40) and Table 12 functional requirements SFR.FXNREQ.001-007 (p. 31 / PDF p. 43). Source gap note: the handbook states the required notifications and tracking number generation but does not specify SLA escalation timers; no escalation timer is inferred.
