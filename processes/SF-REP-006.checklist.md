# Submit SF report offline and synchronise (SF-REP-006) — BPMN 2.0 Verification Checklist

- **Process ID:** `Process_SF_REP_006` (`SF-REP-006`)
- **L1 Source Sections:** `sec-023, sec-026, sec-031` (PDF pages 40, 44, 45, 46, 59)
- **Swimlanes bound to DAK Personas / ArchiMate Roles:**
  - `Lane_SF_REP_006_Reporter` → `pers:sfp-r-09` (`partitionElementRef="sfp-r-09"`) — Paramedic / Field Reporter in Low-Connectivity Area (SFP-R-09)
  - `Lane_SF_REP_006_App` → `pers:sfp-r-13` (`partitionElementRef="sfp-r-13"`) — SF Reporting App Offline Outbox & NMRA Sync Service (SFP-R-13)

## Narrative Summary

Subprocess of SF-REP-001 for capturing an SF report in low- or no-connectivity settings, queuing it in a local encrypted outbox, and synchronising automatically when connectivity is restored, drafted from Table 9 scenario 9 (Paramedic, p. 28 / PDF p. 40), Table 13 offline capability requirements (pp. 32-34 / PDF pp. 44-46), and Ch. 7 outbox implementation note (p. 47 / PDF p. 59).
