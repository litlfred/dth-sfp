<!-- GENERATED from dth-sfp/processes/SF-REP-001.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — SF-REP-001: Detect and report suspected SF medical product

> **Generated, and not the authority.** This is `dth-sfp/processes/SF-REP-001.bpmn` (process `Process_SF_REP_001`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

End-to-end workflow for detecting and reporting a suspected substandard or falsified (SF) medical product, formalised from Table 10 (SF-REP-001 process matrix, page 29 / PDF page 41), Figure 4 (workflow diagram, page 30 / PDF page 42), and Table 9 (9 user scenarios, pages 27-28 / PDF pages 39-40).

## Begin — Observe suspected SF product (`Start_SF_REP_001`)

- Begin here: Reporter observes a suspected substandard or falsified medical product, quality defect, or lack of therapeutic efficacy / adverse reaction (Table 9 scenarios 1-9, Table 10 step 1).
- Call `workflow_start` with `process: "Process_SF_REP_001"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_1_OpenAppAndCheckReg` (Open reporting app & check registration (DE1, DE3))

### 1. Open reporting app & check registration (DE1, DE3) (`Task_1_OpenAppAndCheckReg`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 1-2 (Table 10, Figure 4): Open the SF reporting system (web/mobile/USSD) and query the National Product Catalogue (dth-pc) by product name, brand, or GTIN (SFR.A1.DE3, SFR.FXNREQ.006).
- Record it: `workflow_complete` with `node: "Task_1_OpenAppAndCheckReg"`.
- next: → `Gw_IsRegistered` (Product in national catalogue?)

### Decide — Product in national catalogue? (`Gw_IsRegistered`)

- Gateway 1 (Figure 4, SFR.DT.01): Is the suspected medical product found in the National Product Catalogue / regulatory registration database?
- Call `workflow_complete` with `node: "Gw_IsRegistered"` and `outcome` set to the label that holds:
  - «Registered» → `Task_3_EnterProductDetails` (Select product & auto-populate type (SFR.DT.02))
  - «Unregistered» → `Task_FlagUnregistered` (Record unregistered product details (F2))

### 2. Select product & auto-populate type (SFR.DT.02) (`Task_3_EnterProductDetails`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 3 (Table 10, Figure 4): Select the registered product record and automatically populate product type (SFR.A1.DE5) and manufacturer (SFR.A1.DE4) via decision table SFR.DT.02 (SFR.FXNREQ.006).
- Record it: `workflow_complete` with `node: "Task_3_EnterProductDetails"`.
- next: → `Task_4_EnterBatchExpiry` (Enter or scan batch (DE6) & expiry (DE7))

### 3. Record unregistered product details (F2) (`Task_FlagUnregistered`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 2a (Figure 4 bypass branch, Finding F2/F5): Record free-text product name, manufacturer claim, and unregistered/unlicensed status when the product is absent from the National Product Catalogue.
- Record it: `workflow_complete` with `node: "Task_FlagUnregistered"`.
- next: → `Task_4_EnterBatchExpiry` (Enter or scan batch (DE6) & expiry (DE7))

### 4. Enter or scan batch (DE6) & expiry (DE7) (`Task_4_EnterBatchExpiry`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 4 (Table 10, Figure 4): Enter or scan the product batch/lot number (SFR.A1.DE6) and expiration date (SFR.A1.DE7) via manual entry or barcode scanner (SFR.FXNREQ.007).
- Record it: `workflow_complete` with `node: "Task_4_EnterBatchExpiry"`.
- next: → `Task_5_SelectReportType` (Select channel & SF category (DE2, DE8))

### 5. Select channel & SF category (DE2, DE8) (`Task_5_SelectReportType`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 5 (Table 10, Figure 4): Record report communication mode (SFR.A1.DE2) and select suspected SF report type (SFR.A1.DE8, decision table SFR.DT.01).
- Record it: `workflow_complete` with `node: "Task_5_SelectReportType"`.
- next: → `Gw_ReportCategory` (Suspected category?)

### Decide — Suspected category? (`Gw_ReportCategory`)

- Gateway 2 (Figure 4 step 5, SFR.DT.01): Route to substandard quality defect/therapeutic failure capture or suspected falsification capture.
- Call `workflow_complete` with `node: "Gw_ReportCategory"` and `outcome` set to the label that holds:
  - «Substandard» → `Task_6a_SubstandardDetails` (Describe quality defect or ADR (DE9))
  - «Falsified» → `Task_6b_FalsifiedDetails` (Describe suspected falsification (DE9))

### 6. Describe quality defect or ADR (DE9) (`Task_6a_SubstandardDetails`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 6a (Table 10, Figure 4 substandard branch): Describe suspected quality defects, packaging anomalies, lack of therapeutic effect, or adverse reactions (SFR.A1.DE9).
- Record it: `workflow_complete` with `node: "Task_6a_SubstandardDetails"`.
- next: → `Task_7_AttachPhotos` (Attach product & packaging photos)

### 7. Describe suspected falsification (DE9) (`Task_6b_FalsifiedDetails`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 6b (Table 10, Figure 4 falsified branch): Describe suspected counterfeit features, tampered seals, altered labels, or illicit supply source (SFR.A1.DE9).
- Record it: `workflow_complete` with `node: "Task_6b_FalsifiedDetails"`.
- next: → `Task_7_AttachPhotos` (Attach product & packaging photos)

### 8. Attach product & packaging photos (`Task_7_AttachPhotos`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 7a/7b (Table 10, Figure 4): Attach photographs of the suspected product, label, batch mark, and packaging in supported image formats (SFR.FXNREQ.002).
- Record it: `workflow_complete` with `node: "Task_7_AttachPhotos"`.
- next: → `Gw_ContactInfo` (Provide contact details (DE10)?)

### Decide — Provide contact details (DE10)? (`Gw_ContactInfo`)

- Gateway 3 (Figure 4 step 8): Does the reporter elect to provide personal contact details (SFR.A1.DE10) for follow-up or submit anonymously?
- Call `workflow_complete` with `node: "Gw_ContactInfo"` and `outcome` set to the label that holds:
  - «Contact» → `Task_8a_EnterContact` (Confirm profile, region & contact (DE10))
  - «Anonymous» → `Task_8b_RemainAnonymous` (Omit personal contact details)

### 9. Confirm profile, region & contact (DE10) (`Task_8a_EnterContact`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 8a (Table 10, Figure 4): Confirm reporter profile, auto-assign geographic region via SFR.DT.03 (SFR.FXNREQ.001), and record reporter contact information (SFR.A1.DE10).
- Record it: `workflow_complete` with `node: "Task_8a_EnterContact"`.
- next: → `Task_9_SubmitReport` (Submit SF report to NMRA)

### 10. Omit personal contact details (`Task_8b_RemainAnonymous`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 8b (Table 10, Figure 4): Submit report without personal identifier or contact details while preserving regional origin metadata.
- Record it: `workflow_complete` with `node: "Task_8b_RemainAnonymous"`.
- next: → `Task_9_SubmitReport` (Submit SF report to NMRA)

### 11. Submit SF report to NMRA (`Task_9_SubmitReport`)

- Who: the `Reporter (SFP-R-01..12, R-14)` lane (role `pers:sfp-r-01`).
- What: Step 9 (Table 10, Figure 4): Transmit the completed SF report online or queue via the encrypted offline outbox workflow (SF-REP-006).
- Record it: `workflow_complete` with `node: "Task_9_SubmitReport"`.
- next: → `Task_10_ReceiveAndValidate` (Receive report, assign tracking ID & log)

### 12. Receive report, assign tracking ID & log (`Task_10_ReceiveAndValidate`)

- Who: the `NMRA & Reporting System (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Step 10 (Table 10, SFR.FXNREQ.003-004): Validate mandatory data elements (DE1-DE10), assign a unique report ID (DE1) and tracking number, and store in the NMRA repository.
- Record it: `workflow_complete` with `node: "Task_10_ReceiveAndValidate"`.
- next: → `Task_11_SendAcknowledgement` (Return confirmation & tracking ID)

### 13. Return confirmation & tracking ID (`Task_11_SendAcknowledgement`)

- Who: the `NMRA & Reporting System (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Step 11 (Table 10, SFR.FXNREQ.003-004): Send immediate submission confirmation and tracking number to the reporter.
- Record it: `workflow_complete` with `node: "Task_11_SendAcknowledgement"`.
- next: → `Task_12_InitialScreening` (Screen report & trigger triage (SF-REP-002))

### 14. Screen report & trigger triage (SF-REP-002) (`Task_12_InitialScreening`)

- Who: the `NMRA & Reporting System (SFP-R-13)` lane (role `pers:sfp-r-13`).
- What: Step 12 (Table 10, SFR.FXNREQ.005): Notify the NMRA focal point in real time and initiate regulatory screening and triage (SF-REP-002 / SF-REP-003).
- Record it: `workflow_complete` with `node: "Task_12_InitialScreening"`.
- next: → `End_SF_REP_001` (SF report queued for assessment)

## Done — SF report queued for assessment (`End_SF_REP_001`)

- The instance completes here: SF report is registered, acknowledged, and queued for regulatory triage and investigation. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
