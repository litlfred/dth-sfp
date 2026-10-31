![SF-REP-004 — Take regulatory action on confirmed SF product (Intro, §2.1, §2.2)](../media/SF-REP-004.svg)

<!-- GENERATED from dth-sfp/processes/SF-REP-004.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — SF-REP-004: Execute recall, alert and enforcement

> **Generated, and not the authority.** This is `dth-sfp/processes/SF-REP-004.bpmn` (process `Process_SF_REP_004`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

Workflow for national regulatory alerts, supply chain batch quarantine/recall, law enforcement referral for criminal falsification, and regulatory sanctions, formalised from Introduction (page 1 / PDF page 13), §2.1-2.2 (pages 14-15 / PDF pages 26-27), and Table 4 (page 12 / PDF page 24).

## Begin — Confirmed SF product determination (`Start_SF_REP_004`)

- Begin here: Triggered when investigation (SF-REP-003) confirms a substandard or falsified medical product.
- Call `workflow_start` with `process: "Process_SF_REP_004"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_401_IssueRapidAlert` (Issue national alert & notify facilities)

### 1. Issue national alert & notify facilities (`Task_401_IssueRapidAlert`)

- Who: the `NMRA Enforcement Authority (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Publish rapid national safety/quality alert to health facilities, pharmacies, and the public.
- Record it: `workflow_complete` with `node: "Task_401_IssueRapidAlert"`.
- next: → `Task_402_OrderRecallWithdrawal` (Order batch quarantine or recall)

### 2. Order batch quarantine or recall (`Task_402_OrderRecallWithdrawal`)

- Who: the `NMRA Enforcement Authority (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Issue mandatory regulatory order for batch quarantine, recall, or market withdrawal.
- Record it: `workflow_complete` with `node: "Task_402_OrderRecallWithdrawal"`.
- next: → `Task_403_ExecuteSupplyChainRecall` (Trace batch (DE6), quarantine & remove stock)

### 3. Trace batch (DE6), quarantine & remove stock (`Task_403_ExecuteSupplyChainRecall`)

- Who: the `Supply Chain & Dispensers (SFP-R-14, R-06)` lane (role `pers:sfp-r-14`).
- What: Trace affected batch/lot numbers (SFR.A1.DE6), quarantine inventory, and execute recall across distribution and dispensing points (dth-sc Recall).
- Record it: `workflow_complete` with `node: "Task_403_ExecuteSupplyChainRecall"`.
- next: → `Gw_401_CriminalFalsification` (Criminal falsification or trafficking?)

### Decide — Criminal falsification or trafficking? (`Gw_401_CriminalFalsification`)

- Determine whether the confirmed incident involves deliberate falsification, unlicensed manufacturing, or illicit trafficking.
- Call `workflow_complete` with `node: "Gw_401_CriminalFalsification"` and `outcome` set to the label that holds:
  - «Quality defect» → `Task_404_ApplySanctions` (Apply regulatory sanctions & close action)
  - «Falsified / illicit» → `Task_405_LawEnforcementReferral` (Refer case to law enforcement & customs)

### 4. Apply regulatory sanctions & close action (`Task_404_ApplySanctions`)

- Who: the `NMRA Enforcement Authority (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Record enforcement outcome, apply regulatory sanctions, and close the national enforcement case.
- Record it: `workflow_complete` with `node: "Task_404_ApplySanctions"`.
- next: → `End_SF_REP_004` (Regulatory action completed)

### 5. Refer case to law enforcement & customs (`Task_405_LawEnforcementReferral`)

- Who: the `Law Enforcement & Customs (SFP-R-15)` lane (role `pers:sfp-r-15`).
- What: Coordinate with law enforcement, customs, and justice authorities for seizure and criminal investigation (§2.1-2.2).
- Record it: `workflow_complete` with `node: "Task_405_LawEnforcementReferral"`.
- next: → `Task_404_ApplySanctions` (Apply regulatory sanctions & close action)

## Done — Regulatory action completed (`End_SF_REP_004`)

- The instance completes here: National recall and enforcement actions completed. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
