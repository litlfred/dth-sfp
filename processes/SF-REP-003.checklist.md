<!-- GENERATED from dth-sfp/processes/SF-REP-003.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — SF-REP-003: Investigate SF report and test samples

> **Generated, and not the authority.** This is `dth-sfp/processes/SF-REP-003.bpmn` (process `Process_SF_REP_003`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

Workflow for regulatory investigation, reporter follow-up, physical sample collection, and quality control laboratory testing, formalised from §1.3 (page 11 / PDF page 23), §2.2 (page 15 / PDF page 27), Table 7 SFP-R-05 (Laboratory technician, page 25 / PDF page 37), and Table 9 scenario 5 (page 28 

## Begin — Triaged report requires investigation (`Start_SF_REP_003`)

- Begin here: Triggered when a screened SF report requires regulatory investigation and laboratory verification.
- Call `workflow_start` with `process: "Process_SF_REP_003"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_301_ReviewDossier` (Examine SF report, photos & batch history)

### 1. Examine SF report, photos & batch history (`Task_301_ReviewDossier`)

- Who: the `NMRA Reviewer & Inspectorate (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Inspect submitted report details (DE1-DE10), attached photographs, and linked batch complaints (SFR.FXNREQ.010-012).
- Record it: `workflow_complete` with `node: "Task_301_ReviewDossier"`.
- next: → `Gw_301_HasContact` (Reporter contact available (DE10)?)

### Decide — Reporter contact available (DE10)? (`Gw_301_HasContact`)

- Check whether reporter contact information (SFR.A1.DE10) is available for follow-up inquiry.
- Call `workflow_complete` with `node: "Gw_301_HasContact"` and `outcome` set to the label that holds:
  - «Yes» → `Task_302_RequestFollowUp` (Request follow-up details or sample)
  - «Anonymous» → `Task_303_DispatchSampleToLab` (Collect sample & dispatch to QC lab)

### 2. Request follow-up details or sample (`Task_302_RequestFollowUp`)

- Who: the `NMRA Reviewer & Inspectorate (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Contact the reporter to request clarifying information or physical sample collection.
- Record it: `workflow_complete` with `node: "Task_302_RequestFollowUp"`.
- next: → `Task_304_ProvideFollowUp` (Provide follow-up details or physical sample)

### 3. Collect sample & dispatch to QC lab (`Task_303_DispatchSampleToLab`)

- Who: the `NMRA Reviewer & Inspectorate (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Obtain field/facility sample and dispatch under chain of custody to the quality control testing laboratory.
- Record it: `workflow_complete` with `node: "Task_303_DispatchSampleToLab"`.
- next: → `Task_305_PerformLabAnalysis` (Test sample identity, assay & packaging)

### 4. Provide follow-up details or physical sample (`Task_304_ProvideFollowUp`)

- Who: the `Reporter (SFP-R-01..12)` lane (role `pers:sfp-r-01`).
- What: Reporter provides additional product/clinical details or hands over the physical sample for inspection.
- Record it: `workflow_complete` with `node: "Task_304_ProvideFollowUp"`.
- next: → `Task_303_DispatchSampleToLab` (Collect sample & dispatch to QC lab)

### 5. Test sample identity, assay & packaging (`Task_305_PerformLabAnalysis`)

- Who: the `Quality Control Laboratory (SFP-R-05)` lane (role `pers:sfp-r-05`).
- What: Perform physical, chemical, or microbiological analysis of the suspected product sample and record analytical findings.
- Record it: `workflow_complete` with `node: "Task_305_PerformLabAnalysis"`.
- next: → `Task_306_EvaluateLabFindings` (Evaluate lab certificate & confirm status)

### 6. Evaluate lab certificate & confirm status (`Task_306_EvaluateLabFindings`)

- Who: the `NMRA Reviewer & Inspectorate (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Review laboratory analytical report and classify product as confirmed substandard, confirmed falsified, or compliant.
- Record it: `workflow_complete` with `node: "Task_306_EvaluateLabFindings"`.
- next: → `End_SF_REP_003` (Investigation concluded)

## Done — Investigation concluded (`End_SF_REP_003`)

- The instance completes here: Investigation record completed and routed for regulatory action if confirmed. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
