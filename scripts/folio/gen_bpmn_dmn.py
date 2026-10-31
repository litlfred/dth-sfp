#!/usr/bin/env python3
"""Generate the 6 BPMN 2.0 XML processes, deterministic SVGs, checklists, and 4 DMN 1.3 decision tables for dth-sfp."""
from pathlib import Path
import html

ROOT = Path("/tmp/fix-dth-sfp-l2/dth-sfp")
PROC_DIR = ROOT / "processes"
DEC_DIR = ROOT / "decisions"
PROC_DEC_DIR = PROC_DIR / "decisions"
MEDIA_DIR = ROOT / "folio" / "dth-sfp" / "media"

for d in (PROC_DIR, DEC_DIR, PROC_DEC_DIR, MEDIA_DIR):
    d.mkdir(parents=True, exist_ok=True)

RESOURCES = [
    ("sfp-r-01", "Doctor / Healthcare Professional Reporter (SFP-R-01)"),
    ("sfp-r-02", "Nurse Reporter (SFP-R-02)"),
    ("sfp-r-03", "Individual / Patient Reporter (SFP-R-03)"),
    ("sfp-r-04", "Community Health Worker Reporter (SFP-R-04)"),
    ("sfp-r-05", "Laboratory Technician (SFP-R-05)"),
    ("sfp-r-06", "Pharmacist Reporter (SFP-R-06)"),
    ("sfp-r-07", "Dentist Reporter (SFP-R-07)"),
    ("sfp-r-08", "Midwife Reporter (SFP-R-08)"),
    ("sfp-r-09", "Paramedic / Field Reporter (SFP-R-09)"),
    ("sfp-r-10", "Pharmacy Technician Reporter (SFP-R-10)"),
    ("sfp-r-11", "Public Health Worker Reporter (SFP-R-11)"),
    ("sfp-r-12", "Veterinarian Reporter (SFP-R-12)"),
    ("sfp-r-13", "National Medicines Regulatory Authority (NMRA) Reviewer & Case System (SFP-R-13)"),
    ("sfp-r-14", "Pharmaceutical Manufacturer / Supplier / Supply Chain Actor (SFP-R-14)"),
    ("sfp-r-15", "Governance, Law Enforcement & Global Surveillance (WHO GSMS) Actor (SFP-R-15)"),
]

PROCESS_SPECS = [
    {
        "code": "SF-REP-001",
        "id": "Process_SF_REP_001",
        "name": "Detect and report suspected SF medical product (SF-REP-001)",
        "source_secs": ["sec-023", "sec-024", "sec-025", "sec-037"],
        "pdf_pages": [39, 40, 41, 42, 43, 66, 67],
        "doc": (
            "End-to-end workflow for detecting and reporting a suspected substandard or falsified (SF) medical product, "
            "formalised from Table 10 (SF-REP-001 process matrix, p. 29 / PDF p. 41), Fig. 4 (workflow diagram, p. 30 / PDF p. 42), "
            "and Table 9 (9 user scenarios, pp. 27-28 / PDF pp. 39-40). "
            "Finding F5 corrections applied and recorded: (1) Fig. 4 step 2 duplicated gateway 1 ('Is the product registered?') — collapsed into task Task_CheckRegistration followed by exclusive gateway Gw_IsRegistered; "
            "(2) Fig. 4 gateway 1 had an unlabelled bypass arrow to the end event — replaced by explicit branch Task_FlagUnregistered documenting Finding F2 (unregistered/unlicensed products defined in glossary p. ix but omitted from DE8); "
            "(3) Fig. 4 gateway 5 was labelled as an imperative ('Select type of report') — separated into user task Task_SelectReportType and exclusive gateway Gw_ReportCategory ('Suspected category: Substandard or Falsified?'); "
            "(4) Fig. 4 repeated step numbers 6, 7, 8 on both branches — assigned distinct node IDs and labels on the substandard branch (6a-8a) and falsified branch (6b-8b) before converging at Gw_MergeSubmission; "
            "(5) all symbols conform to OMG BPMN 2.0 and Annex 3 (pp. 54-55 / PDF pp. 66-67)."
        ),
        "lanes": [
            {
                "id": "Lane_SF_REP_001_HCP",
                "name": "Healthcare professional / patient / supplier reporter (SFP-R-01..SFP-R-12, SFP-R-14)",
                "role": "sfp-r-01",
                "persona": "pers:sfp-r-01",
                "doc": "Personas pers:sfp-r-01..pers:sfp-r-12 and pers:sfp-r-14. Observes suspected quality defect, falsification, or therapeutic failure/adverse reaction and submits an SF report.",
                "nodes": [
                    ("startEvent", "Start_SF_REP_001", "Observe suspected SF product or adverse reaction"),
                    ("userTask", "Task_1_OpenAppAndCheckReg", "1. Open SF reporting app & check product registration (DE1, DE3)"),
                    ("exclusiveGateway", "Gw_IsRegistered", "Is product in national product catalogue?"),
                    ("userTask", "Task_FlagUnregistered", "2a. Record suspected unregistered product details (F2 note)"),
                    ("userTask", "Task_3_EnterProductDetails", "3. Select registered product & auto-populate product type (SFR.DT.02)"),
                    ("userTask", "Task_4_EnterBatchExpiry", "4. Enter or scan batch number (DE6) & expiry date (DE7)"),
                    ("userTask", "Task_5_SelectReportType", "5. Select report channel & suspected SF category (DE2, DE8, SFR.DT.01)"),
                    ("exclusiveGateway", "Gw_ReportCategory", "Suspected category?"),
                    ("userTask", "Task_6a_SubstandardDetails", "6a. Describe suspected quality defect / therapeutic failure & ADR (DE9)"),
                    ("userTask", "Task_7a_UploadSubstandardPhotos", "7a. Attach photos of defective product & packaging"),
                    ("userTask", "Task_6b_FalsifiedDetails", "6b. Describe suspected falsification, counterfeit label or source"),
                    ("userTask", "Task_7b_UploadFalsifiedPhotos", "7b. Attach photos of falsified packaging, seal & batch mark"),
                    ("exclusiveGateway", "Gw_ContactInfo", "8. Provide reporter contact details (DE10) or submit anonymously?"),
                    ("userTask", "Task_8a_EnterContact", "8a. Confirm reporter profile, region (SFR.DT.03) & contact (DE10)"),
                    ("userTask", "Task_8b_RemainAnonymous", "8b. Omit personal contact details (anonymous report)"),
                    ("sendTask", "Task_9_SubmitReport", "9. Submit SF report (online or via offline outbox SF-REP-006)"),
                ],
            },
            {
                "id": "Lane_SF_REP_001_NMRA",
                "name": "NMRA & SF Reporting System Back-End (SFP-R-13)",
                "role": "sfp-r-13",
                "persona": "pers:sfp-r-13",
                "doc": "Persona pers:sfp-r-13 / ArchiMate role National Regulatory Authority (id-8e67c8e9e1195cdc857b03a2c640e7fe). Validates report, assigns tracking number, notifies focal points, and triggers investigation.",
                "nodes": [
                    ("receiveTask", "Task_10_ReceiveAndValidate", "10. Receive SF report, assign tracking number & log in NMRA registry"),
                    ("serviceTask", "Task_11_SendAcknowledgement", "11. Return confirmation & tracking number to reporter (SFR.FXNREQ.003-004)"),
                    ("userTask", "Task_12_InitialScreening", "12. Screen report, notify focal point (SFR.FXNREQ.005) & trigger SF-REP-002/003"),
                    ("endEvent", "End_SF_REP_001", "SF report registered & queued for regulatory assessment"),
                ],
            },
        ],
        "flows": [
            ("Flow_01", "Start_SF_REP_001", "Task_1_OpenAppAndCheckReg", None),
            ("Flow_02", "Task_1_OpenAppAndCheckReg", "Gw_IsRegistered", None),
            ("Flow_03_Yes", "Gw_IsRegistered", "Task_3_EnterProductDetails", "Registered"),
            ("Flow_03_No", "Gw_IsRegistered", "Task_FlagUnregistered", "Not found (unregistered / F2)"),
            ("Flow_04a", "Task_FlagUnregistered", "Task_4_EnterBatchExpiry", None),
            ("Flow_04b", "Task_3_EnterProductDetails", "Task_4_EnterBatchExpiry", None),
            ("Flow_05", "Task_4_EnterBatchExpiry", "Task_5_SelectReportType", None),
            ("Flow_06", "Task_5_SelectReportType", "Gw_ReportCategory", None),
            ("Flow_07_Sub", "Gw_ReportCategory", "Task_6a_SubstandardDetails", "Substandard"),
            ("Flow_07_Fal", "Gw_ReportCategory", "Task_6b_FalsifiedDetails", "Falsified"),
            ("Flow_08a", "Task_6a_SubstandardDetails", "Task_7a_UploadSubstandardPhotos", None),
            ("Flow_08b", "Task_6b_FalsifiedDetails", "Task_7b_UploadFalsifiedPhotos", None),
            ("Flow_09a", "Task_7a_UploadSubstandardPhotos", "Gw_ContactInfo", None),
            ("Flow_09b", "Task_7b_UploadFalsifiedPhotos", "Gw_ContactInfo", None),
            ("Flow_10_Contact", "Gw_ContactInfo", "Task_8a_EnterContact", "Contact provided"),
            ("Flow_10_Anon", "Gw_ContactInfo", "Task_8b_RemainAnonymous", "Anonymous"),
            ("Flow_11a", "Task_8a_EnterContact", "Task_9_SubmitReport", None),
            ("Flow_11b", "Task_8b_RemainAnonymous", "Task_9_SubmitReport", None),
            ("Flow_12", "Task_9_SubmitReport", "Task_10_ReceiveAndValidate", None),
            ("Flow_13", "Task_10_ReceiveAndValidate", "Task_11_SendAcknowledgement", None),
            ("Flow_14", "Task_11_SendAcknowledgement", "Task_12_InitialScreening", None),
            ("Flow_15", "Task_12_InitialScreening", "End_SF_REP_001", None),
        ],
    },
    {
        "code": "SF-REP-002",
        "id": "Process_SF_REP_002",
        "name": "Receive, acknowledge and track SF report (SF-REP-002)",
        "source_secs": ["sec-023", "sec-025", "sec-026"],
        "pdf_pages": [39, 40, 43],
        "doc": (
            "Workflow for receiving an SF report, generating a unique tracking number, sending confirmation to the reporter, "
            "notifying the NMRA focal point, and serving status updates, drafted from Table 9 stages 5-6 (pp. 27-28 / PDF pp. 39-40) "
            "and Table 12 functional requirements SFR.FXNREQ.001-007 (p. 31 / PDF p. 43). "
            "Source gap note: the handbook states the required notifications and tracking number generation but does not specify "
            "SLA escalation timers; no escalation timer is inferred."
        ),
        "lanes": [
            {
                "id": "Lane_SF_REP_002_NMRA",
                "name": "NMRA Case Management System & Reviewer (SFP-R-13)",
                "role": "sfp-r-13",
                "persona": "pers:sfp-r-13",
                "doc": "Persona pers:sfp-r-13. Ingests submitted report, resolves product type and reporter region, mints tracking number, alerts focal point, and publishes status changes.",
                "nodes": [
                    ("startEvent", "Start_SF_REP_002", "SF report received from reporter"),
                    ("serviceTask", "Task_201_DeriveRegionAndProductType", "Derive reporter region (SFR.DT.03 / FXNREQ.001) & product type (SFR.DT.02 / FXNREQ.006)"),
                    ("serviceTask", "Task_202_GenerateTrackingNumber", "Generate unique tracking number (SFR.FXNREQ.003)"),
                    ("sendTask", "Task_203_SendConfirmation", "Send submission confirmation & tracking number to reporter (SFR.FXNREQ.004)"),
                    ("serviceTask", "Task_204_NotifyFocalPoint", "Send real-time alert to NMRA focal point (SFR.FXNREQ.005)"),
                    ("userTask", "Task_205_UpdateCaseStatus", "Update case status during assessment & publish to reporter feedback loop"),
                ],
            },
            {
                "id": "Lane_SF_REP_002_Reporter",
                "name": "Reporter (SFP-R-01..SFP-R-12, SFP-R-14)",
                "role": "sfp-r-01",
                "persona": "pers:sfp-r-01",
                "doc": "Persona pers:sfp-r-01. Receives confirmation and tracking number and checks status updates.",
                "nodes": [
                    ("receiveTask", "Task_206_ReceiveTrackingNumber", "Receive confirmation & tracking number"),
                    ("userTask", "Task_207_ViewStatusUpdates", "Check report progress via tracking number (Table 9 stages 5-6)"),
                    ("endEvent", "End_SF_REP_002", "Report acknowledged and tracked to closure"),
                ],
            },
        ],
        "flows": [
            ("Flow_201", "Start_SF_REP_002", "Task_201_DeriveRegionAndProductType", None),
            ("Flow_202", "Task_201_DeriveRegionAndProductType", "Task_202_GenerateTrackingNumber", None),
            ("Flow_203", "Task_202_GenerateTrackingNumber", "Task_203_SendConfirmation", None),
            ("Flow_204", "Task_203_SendConfirmation", "Task_204_NotifyFocalPoint", None),
            ("Flow_205", "Task_204_NotifyFocalPoint", "Task_205_UpdateCaseStatus", None),
            ("Flow_206", "Task_205_UpdateCaseStatus", "Task_206_ReceiveTrackingNumber", None),
            ("Flow_207", "Task_206_ReceiveTrackingNumber", "Task_207_ViewStatusUpdates", None),
            ("Flow_208", "Task_207_ViewStatusUpdates", "End_SF_REP_002", None),
        ],
    },
    {
        "code": "SF-REP-003",
        "id": "Process_SF_REP_003",
        "name": "Investigate SF report and follow up with reporter (SF-REP-003)",
        "source_secs": ["sec-004", "sec-023", "sec-024", "sec-031"],
        "pdf_pages": [13, 39, 40, 41, 59],
        "doc": (
            "Workflow for regulatory investigation of a reported suspect medical product, reporter follow-up when contact details "
            "are available (DE10), and laboratory quality/authenticity testing, drafted from Introduction (p. 1 / PDF p. 13), "
            "Table 9 stage 6 (pp. 27-28 / PDF pp. 39-40), Table 10 (p. 29 / PDF p. 41), and Ch. 7 (p. 47 / PDF p. 59). "
            "Source gap note: pharmacovigilance co-routing rules when DE9 (adverse reaction) is populated and detailed laboratory "
            "analytical protocols are not specified in the handbook and are recorded as explicit open decision points."
        ),
        "lanes": [
            {
                "id": "Lane_SF_REP_003_NMRA",
                "name": "NMRA Reviewer & Inspectorate (SFP-R-13)",
                "role": "sfp-r-13",
                "persona": "pers:sfp-r-13",
                "doc": "Persona pers:sfp-r-13. Screens SF report, requests follow-up information if contact details exist, coordinates sample analysis, and determines regulatory outcome.",
                "nodes": [
                    ("startEvent", "Start_SF_REP_003", "Screened SF report opened for investigation"),
                    ("userTask", "Task_301_ReviewDossier", "Review product, batch (DE6), expiry (DE7), photos & ADR details (DE9)"),
                    ("exclusiveGateway", "Gw_301_HasContact", "Did reporter provide contact info (DE10)?"),
                    ("sendTask", "Task_302_RequestFollowUp", "Request additional information or physical sample from reporter"),
                    ("userTask", "Task_303_DispatchSampleToLab", "Collect/receive sample & dispatch to quality control laboratory"),
                    ("userTask", "Task_306_EvaluateLabFindings", "Evaluate inspection & laboratory findings and share feedback with reporter"),
                    ("endEvent", "End_SF_REP_003", "Investigation complete (triggers SF-REP-004 / SF-REP-005 if confirmed)"),
                ],
            },
            {
                "id": "Lane_SF_REP_003_Reporter",
                "name": "Reporter (SFP-R-01..SFP-R-12)",
                "role": "sfp-r-01",
                "persona": "pers:sfp-r-01",
                "doc": "Persona pers:sfp-r-01. Provides supplementary details or retained product sample when contacted and receives outcome feedback.",
                "nodes": [
                    ("userTask", "Task_304_ProvideFollowUp", "Provide follow-up details or hand over suspect product sample"),
                ],
            },
            {
                "id": "Lane_SF_REP_003_Lab",
                "name": "Quality Control / Testing Laboratory (SFP-R-05)",
                "role": "sfp-r-05",
                "persona": "pers:sfp-r-05",
                "doc": "Persona pers:sfp-r-05. Conducts physical, chemical, or authenticity analysis on suspect product sample.",
                "nodes": [
                    ("userTask", "Task_305_PerformLabAnalysis", "Perform laboratory quality & authenticity testing and return certificate"),
                ],
            },
        ],
        "flows": [
            ("Flow_301", "Start_SF_REP_003", "Task_301_ReviewDossier", None),
            ("Flow_302", "Task_301_ReviewDossier", "Gw_301_HasContact", None),
            ("Flow_303_Yes", "Gw_301_HasContact", "Task_302_RequestFollowUp", "Contact available"),
            ("Flow_303_No", "Gw_301_HasContact", "Task_303_DispatchSampleToLab", "Anonymous report"),
            ("Flow_304", "Task_302_RequestFollowUp", "Task_304_ProvideFollowUp", None),
            ("Flow_305", "Task_304_ProvideFollowUp", "Task_303_DispatchSampleToLab", None),
            ("Flow_306", "Task_303_DispatchSampleToLab", "Task_305_PerformLabAnalysis", None),
            ("Flow_307", "Task_305_PerformLabAnalysis", "Task_306_EvaluateLabFindings", None),
            ("Flow_308", "Task_306_EvaluateLabFindings", "End_SF_REP_003", None),
        ],
    },
    {
        "code": "SF-REP-004",
        "id": "Process_SF_REP_004",
        "name": "Take regulatory action on confirmed SF product (SF-REP-004)",
        "source_secs": ["sec-004", "sec-013", "sec-014"],
        "pdf_pages": [13, 27, 28],
        "doc": (
            "Workflow for regulatory response and enforcement when a medical product is confirmed as substandard, falsified, or "
            "unregistered: issuing alerts, quarantining and recalling affected batches across the supply chain (linked to dth-sc "
            "Recall capability id-a9c92f8fa2924d4180e8f5512b0d0097 and Traceability id-e88f6d077d31407bb1af5f2ecfd3b48a), applying "
            "regulatory sanctions, and referring criminal falsification cases to law enforcement and customs (Introduction p. 1, §2.1 p. 15, §2.2 p. 16)."
        ),
        "lanes": [
            {
                "id": "Lane_SF_REP_004_NMRA",
                "name": "NMRA Regulatory Enforcement Authority (SFP-R-13)",
                "role": "sfp-r-13",
                "persona": "pers:sfp-r-13",
                "doc": "Persona pers:sfp-r-13 / ArchiMate role National Regulatory Authority (id-8e67c8e9e1195cdc857b03a2c640e7fe). Issues alert, orders recall/withdrawal, and coordinates enforcement.",
                "nodes": [
                    ("startEvent", "Start_SF_REP_004", "Confirmed SF medical product determination"),
                    ("userTask", "Task_401_IssueRapidAlert", "Issue national Medical Product Alert & notify health facilities"),
                    ("userTask", "Task_402_OrderRecallWithdrawal", "Order batch quarantine, recall or market withdrawal (dth-sc Recall)"),
                    ("exclusiveGateway", "Gw_401_CriminalFalsification", "Deliberate falsification or illicit trafficking?"),
                    ("userTask", "Task_404_ApplySanctions", "Apply regulatory sanctions & close national enforcement action"),
                    ("endEvent", "End_SF_REP_004", "Regulatory action completed & logged"),
                ],
            },
            {
                "id": "Lane_SF_REP_004_SupplyChain",
                "name": "Supply Chain Actors, Manufacturers & Dispensers (SFP-R-14, SFP-R-06)",
                "role": "sfp-r-14",
                "persona": "pers:sfp-r-14",
                "doc": "Personas pers:sfp-r-14 and pers:sfp-r-06. Trace affected batch/lot numbers (DE6) and remove/quarantine stock across warehouses and pharmacies.",
                "nodes": [
                    ("userTask", "Task_403_ExecuteSupplyChainRecall", "Trace affected batch (DE6), quarantine stock & remove from supply chain"),
                ],
            },
            {
                "id": "Lane_SF_REP_004_LawEnforcement",
                "name": "Law Enforcement, Customs & Multisector Authorities (SFP-R-15)",
                "role": "sfp-r-15",
                "persona": "pers:sfp-r-15",
                "doc": "Persona pers:sfp-r-15 (§2.2 multisector alignment). Investigates criminal falsification networks and border seizures.",
                "nodes": [
                    ("userTask", "Task_405_LawEnforcementReferral", "Refer case to law enforcement & customs for seizure/investigation (§2.1-2.2)"),
                ],
            },
        ],
        "flows": [
            ("Flow_401", "Start_SF_REP_004", "Task_401_IssueRapidAlert", None),
            ("Flow_402", "Task_401_IssueRapidAlert", "Task_402_OrderRecallWithdrawal", None),
            ("Flow_403", "Task_402_OrderRecallWithdrawal", "Task_403_ExecuteSupplyChainRecall", None),
            ("Flow_404", "Task_403_ExecuteSupplyChainRecall", "Gw_401_CriminalFalsification", None),
            ("Flow_405_Yes", "Gw_401_CriminalFalsification", "Task_405_LawEnforcementReferral", "Yes (falsified / illicit)"),
            ("Flow_405_No", "Gw_401_CriminalFalsification", "Task_404_ApplySanctions", "No (quality defect)"),
            ("Flow_406", "Task_405_LawEnforcementReferral", "Task_404_ApplySanctions", None),
            ("Flow_407", "Task_404_ApplySanctions", "End_SF_REP_004", None),
        ],
    },
    {
        "code": "SF-REP-005",
        "id": "Process_SF_REP_005",
        "name": "Report confirmed SF case to WHO GSMS (SF-REP-005)",
        "source_secs": ["sec-004", "sec-011"],
        "pdf_pages": [13, 24],
        "doc": (
            "Workflow for national regulatory focal points to submit validated SF incident reports to the WHO Global Surveillance "
            "and Monitoring System (GSMS) and coordinate regional/global Medical Product Alerts (Introduction p. 1 / PDF p. 13; "
            "Table 4 p. 12 / PDF p. 24). Drafted strictly from the handbook's stated step without inferring internal WHO GSMS workflows."
        ),
        "lanes": [
            {
                "id": "Lane_SF_REP_005_NMRA",
                "name": "NMRA Focal Point (SFP-R-13)",
                "role": "sfp-r-13",
                "persona": "pers:sfp-r-13",
                "doc": "Persona pers:sfp-r-13. Formats validated national SF case record and submits to WHO GSMS.",
                "nodes": [
                    ("startEvent", "Start_SF_REP_005", "National SF incident validated for global reporting"),
                    ("userTask", "Task_501_PrepareGSMSDossier", "Compile validated SF product, batch & investigation dossier"),
                    ("sendTask", "Task_502_SubmitToGSMS", "Transmit SF report to WHO GSMS (Table 4, Intro p. 1)"),
                ],
            },
            {
                "id": "Lane_SF_REP_005_GSMS",
                "name": "WHO Global Surveillance and Monitoring System (GSMS) (SFP-R-15)",
                "role": "sfp-r-15",
                "persona": "pers:sfp-r-15",
                "doc": "Persona pers:sfp-r-15 / ArchiMate Global Platforms (id-e3c4f0ec36f35eccb0d4c50f887316e5). Logs global surveillance record and issues WHO Medical Product Alert when warranted.",
                "nodes": [
                    ("receiveTask", "Task_503_RecordInGSMS", "Register incident in WHO GSMS database & assess cross-border risk"),
                    ("serviceTask", "Task_504_IssueGlobalAlert", "Assist Member States & issue WHO Medical Product Alert when necessary"),
                    ("endEvent", "End_SF_REP_005", "Global surveillance record updated"),
                ],
            },
        ],
        "flows": [
            ("Flow_501", "Start_SF_REP_005", "Task_501_PrepareGSMSDossier", None),
            ("Flow_502", "Task_501_PrepareGSMSDossier", "Task_502_SubmitToGSMS", None),
            ("Flow_503", "Task_502_SubmitToGSMS", "Task_503_RecordInGSMS", None),
            ("Flow_504", "Task_503_RecordInGSMS", "Task_504_IssueGlobalAlert", None),
            ("Flow_505", "Task_504_IssueGlobalAlert", "End_SF_REP_005", None),
        ],
    },
    {
        "code": "SF-REP-006",
        "id": "Process_SF_REP_006",
        "name": "Submit SF report offline and synchronise (SF-REP-006)",
        "source_secs": ["sec-023", "sec-026", "sec-031"],
        "pdf_pages": [40, 44, 45, 46, 59],
        "doc": (
            "Subprocess of SF-REP-001 for capturing an SF report in low- or no-connectivity settings, queuing it in a local "
            "encrypted outbox, and synchronising automatically when connectivity is restored, drafted from Table 9 scenario 9 "
            "(Paramedic, p. 28 / PDF p. 40), Table 13 offline capability requirements (pp. 32-34 / PDF pp. 44-46), and Ch. 7 "
            "outbox implementation note (p. 47 / PDF p. 59)."
        ),
        "lanes": [
            {
                "id": "Lane_SF_REP_006_Reporter",
                "name": "Paramedic / Field Reporter in Low-Connectivity Area (SFP-R-09)",
                "role": "sfp-r-09",
                "persona": "pers:sfp-r-09",
                "doc": "Persona pers:sfp-r-09 (Paramedic / field health worker). Captures SF report and product photos while offline.",
                "nodes": [
                    ("startEvent", "Start_SF_REP_006", "Detect suspect product without network connectivity"),
                    ("userTask", "Task_601_CompleteOfflineForm", "Complete SF report form (DE1-DE10) & attach photos in offline mode"),
                    ("userTask", "Task_602_SaveToOutbox", "Submit report to local encrypted device outbox"),
                ],
            },
            {
                "id": "Lane_SF_REP_006_App",
                "name": "SF Reporting App Offline Outbox & NMRA Sync Service (SFP-R-13)",
                "role": "sfp-r-13",
                "persona": "pers:sfp-r-13",
                "doc": "Persona pers:sfp-r-13 (SF Reporting POS App & Server). Queues report locally, detects connectivity, uploads to NMRA server, and delivers tracking number.",
                "nodes": [
                    ("serviceTask", "Task_603_QueueEncryptedOutbox", "Store report & attachments in local outbox queue (Table 13 offline NFR)"),
                    ("exclusiveGateway", "Gw_601_NetworkAvailable", "Network connectivity restored?"),
                    ("serviceTask", "Task_604_SyncToNMRAServer", "Synchronise queued SF report to NMRA server & trigger SF-REP-002"),
                    ("serviceTask", "Task_605_DeliverConfirmation", "Update local status & display assigned tracking number to reporter"),
                    ("endEvent", "End_SF_REP_006", "Offline SF report synchronised & acknowledged"),
                ],
            },
        ],
        "flows": [
            ("Flow_601", "Start_SF_REP_006", "Task_601_CompleteOfflineForm", None),
            ("Flow_602", "Task_601_CompleteOfflineForm", "Task_602_SaveToOutbox", None),
            ("Flow_603", "Task_602_SaveToOutbox", "Task_603_QueueEncryptedOutbox", None),
            ("Flow_604", "Task_603_QueueEncryptedOutbox", "Gw_601_NetworkAvailable", None),
            ("Flow_605_Yes", "Gw_601_NetworkAvailable", "Task_604_SyncToNMRAServer", "Online"),
            ("Flow_605_Wait", "Gw_601_NetworkAvailable", "Task_603_QueueEncryptedOutbox", "Offline (retain in outbox)"),
            ("Flow_606", "Task_604_SyncToNMRAServer", "Task_605_DeliverConfirmation", None),
            ("Flow_607", "Task_605_DeliverConfirmation", "End_SF_REP_006", None),
        ],
    },
]

def render_bpmn_and_svg(spec: dict) -> tuple[str, str, str]:
    code = spec["code"]
    pid = spec["id"]
    pname = spec["name"]
    pdoc = spec["doc"]

    # Compute deterministic layout coordinates for each node
    node_coords = {}
    lane_boxes = []
    y_cursor = 80
    max_x = 1200

    for l_idx, lane in enumerate(spec["lanes"]):
        lane_h = 180
        lane_y = y_cursor
        y_cursor += lane_h
        nodes = lane["nodes"]
        for n_idx, (ntype, nid, nlabel) in enumerate(nodes):
            nx = 180 + n_idx * 170
            ny = lane_y + 55
            if "Event" in ntype:
                nw, nh = 36, 36
                ny = lane_y + 72
            elif "Gateway" in ntype:
                nw, nh = 50, 50
                ny = lane_y + 65
            else:
                nw, nh = 130, 70
            node_coords[nid] = (nx, ny, nw, nh, ntype, nlabel, lane["id"])
            if nx + nw + 80 > max_x:
                max_x = nx + nw + 80
        lane_boxes.append((lane["id"], lane["name"], 40, lane_y, max_x - 40, lane_h))

    pool_h = y_cursor - 80

    # Incoming / outgoing maps
    incoming = {nid: [] for nid in node_coords}
    outgoing = {nid: [] for nid in node_coords}
    for fid, src, tgt, _ in spec["flows"]:
        outgoing[src].append(fid)
        incoming[tgt].append(fid)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"',
        '                  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"',
        '                  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"',
        '                  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"',
        '                  xmlns:bootstrap.processes="https://litlfred.github.io/bootstrap/v0/processes/ns#"',
        '                  xmlns:cat-harness.processes="https://litlfred.github.io/cat-harness/v0/processes/ns#"',
        f'                  id="Definitions_{pid}"',
        '                  targetNamespace="https://litlfred.github.io/dth-sfp/workflows"',
        '                  exporter="folio-assistant" exporterVersion="1">',
        '  <bpmn:import namespace="https://litlfred.github.io/bootstrap/v0/processes/ns#" location="https://litlfred.github.io/bootstrap/v0/processes/ns.jsonld" importType="http://www.w3.org/ns/json-ld"/>',
    ]
    for rid, rname in RESOURCES:
        lines.append(f'  <bpmn:resource id="{rid}" name="{html.escape(rname)}"/>')

    lines += [
        f'  <bpmn:collaboration id="Collaboration_{pid}">',
        f'    <bpmn:participant id="Participant_{pid}" name="{html.escape(pname)}" processRef="{pid}"/>',
        '  </bpmn:collaboration>',
        f'  <bpmn:process id="{pid}" name="{html.escape(pname)}" isExecutable="false">',
        f'    <bpmn:documentation>{html.escape(pdoc)}</bpmn:documentation>',
        '    <bpmn:extensionElements>',
        '      <cat-harness.processes:policy enforcement="advisory"/>',
        '    </bpmn:extensionElements>',
        f'    <bpmn:laneSet id="LaneSet_{pid}">',
    ]

    for lane in spec["lanes"]:
        lines.append(f'      <bpmn:lane id="{lane["id"]}" name="{html.escape(lane["name"])}" partitionElementRef="{lane["role"]}">')
        lines.append(f'        <bpmn:documentation>{html.escape(lane["doc"])}</bpmn:documentation>')
        for _, nid, _ in lane["nodes"]:
            lines.append(f'        <bpmn:flowNodeRef>{nid}</bpmn:flowNodeRef>')
        lines.append('      </bpmn:lane>')
    lines.append('    </bpmn:laneSet>')

    for lane in spec["lanes"]:
        for ntype, nid, nlabel in lane["nodes"]:
            lines.append(f'    <bpmn:{ntype} id="{nid}" name="{html.escape(nlabel)}">')
            for inc in incoming[nid]:
                lines.append(f'      <bpmn:incoming>{inc}</bpmn:incoming>')
            for out in outgoing[nid]:
                lines.append(f'      <bpmn:outgoing>{out}</bpmn:outgoing>')
            lines.append(f'    </bpmn:{ntype}>')

    for fid, src, tgt, flabel in spec["flows"]:
        name_attr = f' name="{html.escape(flabel)}"' if flabel else ''
        lines.append(f'    <bpmn:sequenceFlow id="{fid}" sourceRef="{src}" targetRef="{tgt}"{name_attr}/>')

    lines += [
        '  </bpmn:process>',
        f'  <bpmndi:BPMNDiagram id="BPMNDiagram_{pid}">',
        f'    <bpmndi:BPMNPlane id="BPMNPlane_{pid}" bpmnElement="Collaboration_{pid}">',
        f'      <bpmndi:BPMNShape id="Shape_Participant_{pid}" bpmnElement="Participant_{pid}" isHorizontal="true">',
        f'        <dc:Bounds x="20" y="80" width="{max_x - 20}" height="{pool_h}"/>',
        '      </bpmndi:BPMNShape>',
    ]
    for lid, lname, lx, ly, lw, lh in lane_boxes:
        lines += [
            f'      <bpmndi:BPMNShape id="Shape_{lid}" bpmnElement="{lid}" isHorizontal="true">',
            f'        <dc:Bounds x="{lx}" y="{ly}" width="{lw}" height="{lh}"/>',
            '      </bpmndi:BPMNShape>',
        ]
    for nid, (nx, ny, nw, nh, _, _, _) in node_coords.items():
        lines += [
            f'      <bpmndi:BPMNShape id="Shape_{nid}" bpmnElement="{nid}">',
            f'        <dc:Bounds x="{nx}" y="{ny}" width="{nw}" height="{nh}"/>',
            '      </bpmndi:BPMNShape>',
        ]
    for fid, src, tgt, _ in spec["flows"]:
        sx, sy, sw, sh, _, _, _ = node_coords[src]
        tx, ty, tw, th, _, _, _ = node_coords[tgt]
        lines += [
            f'      <bpmndi:BPMNEdge id="Edge_{fid}" bpmnElement="{fid}">',
            f'        <di:waypoint x="{sx + sw}" y="{sy + sh // 2}"/>',
            f'        <di:waypoint x="{tx}" y="{ty + th // 2}"/>',
            '      </bpmndi:BPMNEdge>',
        ]
    lines += [
        '    </bpmndi:BPMNPlane>',
        '  </bpmndi:BPMNDiagram>',
        '</bpmn:definitions>',
        '',
    ]
    bpmn_xml = "\n".join(lines)

    # Render clean deterministic SVG
    svg_h = y_cursor + 40
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_x + 20} {svg_h}" width="{max_x + 20}" height="{svg_h}" font-family="Inter, -apple-system, BlinkMacSystemFont, sans-serif">',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155"/>',
        '    </marker>',
        '  </defs>',
        f'  <rect x="0" y="0" width="{max_x + 20}" height="{svg_h}" fill="#ffffff"/>',
        f'  <text x="20" y="36" font-size="16" font-weight="700" fill="#0f172a">{html.escape(pname)}</text>',
        f'  <text x="20" y="56" font-size="11" fill="#475569">WHO DTH for SF Medical Product Reporting Systems — {code} (OMG BPMN 2.0)</text>',
    ]
    for lid, lname, lx, ly, lw, lh in lane_boxes:
        svg_lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>')
        svg_lines.append(f'  <rect x="{lx}" y="{ly}" width="110" height="{lh}" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1.5"/>')
        svg_lines.append(f'  <text x="{lx + 12}" y="{ly + 24}" font-size="11" font-weight="600" fill="#1e293b">{html.escape(lname[:28])}</text>')

    for fid, src, tgt, flabel in spec["flows"]:
        sx, sy, sw, sh, _, _, _ = node_coords[src]
        tx, ty, tw, th, _, _, _ = node_coords[tgt]
        x1, y1 = sx + sw, sy + sh // 2
        x2, y2 = tx, ty + th // 2
        svg_lines.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#334155" stroke-width="1.5" marker-end="url(#arrow)"/>')
        if flabel:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2 - 6
            svg_lines.append(f'  <text x="{mx}" y="{my}" font-size="9" fill="#0f172a" text-anchor="middle">{html.escape(flabel)}</text>')

    for nid, (nx, ny, nw, nh, ntype, nlabel, _) in node_coords.items():
        if ntype == "startEvent":
            cx, cy = nx + nw // 2, ny + nh // 2
            svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="18" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>')
            svg_lines.append(f'  <text x="{cx}" y="{ny + nh + 14}" font-size="9" fill="#1e293b" text-anchor="middle">{html.escape(nlabel[:26])}</text>')
        elif ntype == "endEvent":
            cx, cy = nx + nw // 2, ny + nh // 2
            svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="18" fill="#fee2e2" stroke="#dc2626" stroke-width="3"/>')
            svg_lines.append(f'  <text x="{cx}" y="{ny + nh + 14}" font-size="9" fill="#1e293b" text-anchor="middle">{html.escape(nlabel[:26])}</text>')
        elif "Gateway" in ntype:
            cx, cy = nx + nw // 2, ny + nh // 2
            pts = f"{cx},{ny} {nx+nw},{cy} {cx},{ny+nh} {nx},{cy}"
            svg_lines.append(f'  <polygon points="{pts}" fill="#fef9c3" stroke="#ca8a04" stroke-width="2"/>')
            svg_lines.append(f'  <text x="{cx}" y="{ny - 6}" font-size="9" font-weight="600" fill="#854d0e" text-anchor="middle">{html.escape(nlabel[:30])}</text>')
        else:
            svg_lines.append(f'  <rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="6" ry="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>')
            words = nlabel.split()
            line1 = " ".join(words[:4])
            line2 = " ".join(words[4:8])
            line3 = " ".join(words[8:])
            svg_lines.append(f'  <text x="{nx + nw // 2}" y="{ny + 24}" font-size="9.5" font-weight="600" fill="#1e3a8a" text-anchor="middle">{html.escape(line1)}</text>')
            if line2:
                svg_lines.append(f'  <text x="{nx + nw // 2}" y="{ny + 38}" font-size="9" fill="#1e3a8a" text-anchor="middle">{html.escape(line2)}</text>')
            if line3:
                svg_lines.append(f'  <text x="{nx + nw // 2}" y="{ny + 52}" font-size="9" fill="#1e3a8a" text-anchor="middle">{html.escape(line3[:26])}</text>')

    svg_lines.append('</svg>\n')
    svg_xml = "\n".join(svg_lines)

    checklist = f"""# {pname} — BPMN 2.0 Verification Checklist

- **Process ID:** `{pid}` (`{code}`)
- **L1 Source Sections:** `{", ".join(spec["source_secs"])}` (PDF pages {", ".join(str(p) for p in spec["pdf_pages"])})
- **Swimlanes bound to DAK Personas / ArchiMate Roles:**
""" + "\n".join(
        f"  - `{l['id']}` → `{l['persona']}` (`partitionElementRef=\"{l['role']}\"`) — {l['name']}"
        for l in spec["lanes"]
    ) + "\n\n## Narrative Summary\n\n" + pdoc + "\n"

    return bpmn_xml, svg_xml, checklist

for spec in PROCESS_SPECS:
    code = spec["code"]
    bpmn_xml, svg_xml, checklist = render_bpmn_and_svg(spec)
    (PROC_DIR / f"{code}.bpmn").write_text(bpmn_xml)
    (PROC_DIR / f"{code}.svg").write_text(svg_xml)
    (PROC_DIR / f"{code}.checklist.md").write_text(checklist)
    (MEDIA_DIR / f"{code}.svg").write_text(svg_xml)

# Write processes/README.md
(PROC_DIR / "README.md").write_text("""# Business Processes (BPMN 2.0) — `dth-sfp`

Six BPMN 2.0 business processes drafted from the WHO *Digital Transformation Handbook for Substandard and Falsified Medical Product Reporting Systems* (`who-iris/library/9789240120747-eng`, `litlfred/dth-sfp#1` §2.4 Step P6b):

| Process Code | File | Title | L1 Source | Swimlanes |
|---|---|---|---|---|
| `SF-REP-001` | [`SF-REP-001.bpmn`](SF-REP-001.bpmn) | Detect and report suspected SF medical product | Table 10 (p. 29), Fig. 4 (p. 30, redrawn with F5 fixes), Table 9 (pp. 27–28) | `pers:sfp-r-01`..`12`/`14`, `pers:sfp-r-13` |
| `SF-REP-002` | [`SF-REP-002.bpmn`](SF-REP-002.bpmn) | Receive, acknowledge and track SF report | Table 9 stages 5–6 (pp. 27–28), Table 12 (`SFR.FXNREQ.001`–`007`, p. 31) | `pers:sfp-r-13`, `pers:sfp-r-01` |
| `SF-REP-003` | [`SF-REP-003.bpmn`](SF-REP-003.bpmn) | Investigate SF report and follow up with reporter | Intro (p. 1), Table 9 stage 6 (pp. 27–28), Ch. 7 (p. 47) | `pers:sfp-r-13`, `pers:sfp-r-01`, `pers:sfp-r-05` |
| `SF-REP-004` | [`SF-REP-004.bpmn`](SF-REP-004.bpmn) | Take regulatory action on confirmed SF product | Intro (p. 1), §2.1 (p. 15), §2.2 (p. 16) | `pers:sfp-r-13`, `pers:sfp-r-14`, `pers:sfp-r-15` |
| `SF-REP-005` | [`SF-REP-005.bpmn`](SF-REP-005.bpmn) | Report confirmed SF case to WHO GSMS | Intro (p. 1), Table 4 (p. 12) | `pers:sfp-r-13`, `pers:sfp-r-15` |
| `SF-REP-006` | [`SF-REP-006.bpmn`](SF-REP-006.bpmn) | Submit SF report offline and synchronise | Table 9 (Paramedic, p. 28), Table 13 NFRs (pp. 32–35), Ch. 7 (p. 47) | `pers:sfp-r-09`, `pers:sfp-r-13` |
""")

# DMN 1.3 tables (SFR-DT-01..04)
DMN_SPECS = [
    {
        "file": "SFR-DT-01.dmn",
        "code": "SFR.DT.01",
        "id": "Decision_SFR_DT_01",
        "name": "SFR.DT.01 — Report type and registration status to workflow path",
        "hit_policy": "UNIQUE",
        "doc": (
            "Routes an SF report submission based on product registration status in the national product catalogue and "
            "suspected SF category (Fig. 4 gateways, p. 30 / PDF p. 42; SFR.A1.DE2 & SFR.A1.DE8, Table 11, p. 31 / PDF p. 43). "
            "Finding F2 recorded: the handbook glossary (p. ix) and Introduction (p. 1) define unregistered/unlicensed medical "
            "products as the third WHO category, but Fig. 4 and SFR.A1.DE8 provide only substandard and falsified options."
        ),
        "inputs": [
            ("In_Registered", "Product registered in national catalogue?", "isProductRegistered", "boolean"),
            ("In_Channel", "Reporting channel (SFR.A1.DE8)", "reportingChannel", "string"),
            ("In_Category", "Suspected SF category (Fig. 4 gateway 5)", "suspectedCategory", "string"),
        ],
        "outputs": [
            ("Out_Path", "workflowPath", "Workflow branch (SF-REP-001)", "string"),
            ("Out_Note", "regulatoryNote", "Regulatory handling note", "string"),
        ],
        "rules": [
            ("Rule_DT01_1", ["true", '"Healthcare professional"', '"Substandard"'], ['"substandard-branch"', '"Route through substandard quality defect / therapeutic failure branch (steps 6a-8a)"'], "Healthcare professional reporting a suspected substandard registered product (Fig. 4 left branch, DE8)."),
            ("Rule_DT01_2", ["true", '"Public"', '"Substandard"'], ['"substandard-branch"', '"Route through substandard quality defect / adverse reaction branch (steps 6a-8a)"'], "Public/patient reporting a suspected substandard registered product (Fig. 4 left branch, DE8)."),
            ("Rule_DT01_3", ["true", '"Pharmaceutical industry"', '"Substandard"'], ['"substandard-branch"', '"Route through manufacturer/importer quality defect branch (steps 6a-8a)"'], "Manufacturer/importer reporting a suspected substandard batch (Fig. 4 left branch, DE8)."),
            ("Rule_DT01_4", ["true", '"Healthcare professional"', '"Falsified"'], ['"falsified-branch"', '"Route through suspected falsification branch (steps 6b-8b) and flag for inspectorate"'], "Healthcare professional reporting a suspected falsified registered product (Fig. 4 right branch, DE8)."),
            ("Rule_DT01_5", ["true", '"Public"', '"Falsified"'], ['"falsified-branch"', '"Route through suspected falsification branch (steps 6b-8b)"'], "Public/patient reporting a suspected falsified product (Fig. 4 right branch, DE8)."),
            ("Rule_DT01_6", ["true", '"Pharmaceutical industry"', '"Falsified"'], ['"falsified-branch"', '"Route through counterfeit/falsification branch (steps 6b-8b) and notify law enforcement liaison"'], "Manufacturer/importer reporting counterfeit/falsified product misrepresentation (Fig. 4 right branch, DE8)."),
            ("Rule_DT01_7", ["false", "-", "-"], ['"unregistered-or-falsified-branch"', '"Finding F2/F5: Product not in national product catalogue; capture unregistered/unlicensed product details and route for regulatory verification"'], "Product not found in national product catalogue: Fig. 4 had an unlabelled bypass to End (F5) and omitted unregistered from DE8 (F2); captured explicitly for regulatory review."),
        ],
    },
    {
        "file": "SFR-DT-02.dmn",
        "code": "SFR.DT.02",
        "id": "Decision_SFR_DT_02",
        "name": "SFR.DT.02 — Selected product to applicable product type (SFR.A1.DE5)",
        "hit_policy": "FIRST",
        "doc": (
            "Derives the applicable product type (SFR.A1.DE5) from the product selected by the reporter in the National Product "
            "Catalogue (dth-pc/national-product-catalogue), per Table 12 requirement 6 (assigned ID SFR.FXNREQ.006, p. 31 / PDF p. 43): "
            "'As a public health agency, I want the system to assign the applicable type of product after a user selects a specific "
            "product, so that I can minimize reporting errors.' Finding F4 noted: SFR.A1.DE5 in Table 11 has an empty description "
            "and data type; the WHO medical product categories come from the handbook glossary definition of 'Medical product' (p. viii)."
        ),
        "inputs": [
            ("In_ProdId", "Selected product identifier (SFR.A1.DE3)", "productIdSelected", "boolean"),
            ("In_CatClass", "Catalogue product classification (dth-pc)", "catalogueCategory", "string"),
        ],
        "outputs": [
            ("Out_ProdType", "productType", "Assigned product type (SFR.A1.DE5)", "string"),
            ("Out_Source", "assignmentMode", "Assignment mode", "string"),
        ],
        "rules": [
            ("Rule_DT02_1", ["true", '"Medicine"'], ['"Medicine"', '"Auto-assigned from National Product Catalogue (SFR.FXNREQ.006)"'], "Selected catalogue item is a pharmaceutical medicine (glossary 'Medical product', p. viii)."),
            ("Rule_DT02_2", ["true", '"Vaccine"'], ['"Vaccine"', '"Auto-assigned from National Product Catalogue (SFR.FXNREQ.006)"'], "Selected catalogue item is a vaccine (glossary 'Medical product', p. viii)."),
            ("Rule_DT02_3", ["true", '"Diagnostic / IVD"'], ['"Diagnostic (in vitro diagnostic)"', '"Auto-assigned from National Product Catalogue (SFR.FXNREQ.006)"'], "Selected catalogue item is a diagnostic / in vitro diagnostic reagent or kit (Table 8 Lab Technician, glossary p. viii)."),
            ("Rule_DT02_4", ["true", '"Medical device"'], ['"Medical device"', '"Auto-assigned from National Product Catalogue (SFR.FXNREQ.006)"'], "Selected catalogue item is a medical device (glossary 'Medical product', p. viii)."),
            ("Rule_DT02_5", ["false", "-"], ['"Unclassified / manual entry"', '"Product not matched in catalogue; reporter enters product description manually (Finding F4: DE5 value set not specified in Table 11)"'], "Unmatched product: manual fallback noted per Finding F4."),
        ],
    },
    {
        "file": "SFR-DT-03.dmn",
        "code": "SFR.DT.03",
        "id": "Decision_SFR_DT_03",
        "name": "SFR.DT.03 — Reporter profile to assigned geographic region (SFR.FXNREQ.001)",
        "hit_policy": "FIRST",
        "doc": (
            "Derives the geographic region of an SF report from the authenticated reporter's profile or facility registration "
            "per Table 12 requirement SFR.FXNREQ.001 (p. 31 / PDF p. 43): 'As a public health agency, I want to know the region "
            "where the reporter is located based on the user's profile, so that I do not have to ask the user to enter that "
            "information in the report.'"
        ),
        "inputs": [
            ("In_HasProfile", "Reporter authenticated with registered profile?", "hasRegisteredProfile", "boolean"),
            ("In_FacilityRegion", "Profile / facility region attribute present?", "hasProfileRegion", "boolean"),
        ],
        "outputs": [
            ("Out_RegionSource", "regionResolution", "Region derivation outcome", "string"),
            ("Out_PromptUser", "promptReporterForRegion", "Prompt reporter to enter region manually?", "boolean"),
        ],
        "rules": [
            ("Rule_DT03_1", ["true", "true"], ['"Auto-populated from reporter profile / Health Facility Registry (SFR.FXNREQ.001)"', "false"], "Authenticated reporter with a profile region: system derives region automatically without prompting user (SFR.FXNREQ.001)."),
            ("Rule_DT03_2", ["true", "false"], ['"Profile lacks region attribute; prompt reporter to select region"', "true"], "Authenticated reporter whose profile has no region recorded."),
            ("Rule_DT03_3", ["false", "-"], ['"Anonymous or unauthenticated submission; region optional or selected manually"', "true"], "Unauthenticated or anonymous reporter (SFR.A1.DE10 omitted) has no stored user profile."),
        ],
    },
    {
        "file": "SFR-DT-04.dmn",
        "code": "SFR.DT.04",
        "id": "Decision_SFR_DT_04",
        "name": "SFR.DT.04 — Capability area and maturity stage to digital investment roadmap milestone (Table 6)",
        "hit_policy": "UNIQUE",
        "doc": (
            "Maps each SF reporting system capability domain and investment horizon (Short-term, Medium-term, Long-term) "
            "to the milestone activities defined in Table 6 ('Examples of short-, medium- and long-term milestones for "
            "developing an SF medical product reporting system', §3.1, p. 20 / PDF p. 32)."
        ),
        "inputs": [
            ("In_Domain", "Capability area (Table 6)", "capabilityArea", "string"),
            ("In_Horizon", "Roadmap horizon (Table 6)", "roadmapHorizon", "string"),
        ],
        "outputs": [
            ("Out_Milestone", "milestoneTarget", "Target roadmap milestone (Table 6, p. 20)", "string"),
        ],
        "rules": [
            ("Rule_DT04_1", ['"Governance and policy"', '"Short-term"'], ['"Establish multisectoral TWG, review legal/regulatory mandate for SF reporting, and define data privacy/confidentiality policy"'], "Table 6 row 1, Short-term."),
            ("Rule_DT04_2", ['"Governance and policy"', '"Medium-term"'], ['"Formalize SOPs for inter-agency coordination (NMRA, MOH, customs, law enforcement) and mandate digital SF reporting workflows"'], "Table 6 row 1, Medium-term."),
            ("Rule_DT04_3", ['"Governance and policy"', '"Long-term"'], ['"Institutionalize sustainable financing, cross-border regulatory harmonization, and continuous policy review"'], "Table 6 row 1, Long-term."),
            ("Rule_DT04_4", ['"Business processes and workflows"', '"Short-term"'], ['"Map current SF reporting processes, define standardized minimum data elements (DE1-DE10), and design core SF-REP-001 workflow"'], "Table 6 row 2, Short-term."),
            ("Rule_DT04_5", ['"Business processes and workflows"', '"Medium-term"'], ['"Implement automated acknowledgement/tracking numbers (SF-REP-002), reporter feedback loop, and laboratory investigation workflows (SF-REP-003)"'], "Table 6 row 2, Medium-term."),
            ("Rule_DT04_6", ['"Business processes and workflows"', '"Long-term"'], ['"Integrate end-to-end supply chain recall/traceability triggers (SF-REP-004) and automated WHO GSMS reporting (SF-REP-005)"'], "Table 6 row 2, Long-term."),
            ("Rule_DT04_7", ['"People and workforce"', '"Short-term"'], ['"Identify user personas (Tables 7-8), train initial pilot health workers and NMRA focal points, and launch awareness materials"'], "Table 6 row 3, Short-term."),
            ("Rule_DT04_8", ['"People and workforce"', '"Medium-term"'], ['"Expand training to all reporting personas (Table 9) and embed SF reporting in continuing professional development"'], "Table 6 row 3, Medium-term."),
            ("Rule_DT04_9", ['"People and workforce"', '"Long-term"'], ['"Embed SF surveillance competencies in pre-service curricula and sustain national community & professional reporting culture"'], "Table 6 row 3, Long-term."),
            ("Rule_DT04_10", ['"Data and interoperability"', '"Short-term"'], ['"Adopt standardized core data dictionary (Table 11) and link to National Product Catalogue and Facility Registry"'], "Table 6 row 4, Short-term."),
            ("Rule_DT04_11", ['"Data and interoperability"', '"Medium-term"'], ['"Enable standards-based exchange (FHIR / GS1 GTIN, batch, expiry) with pharmacovigilance, LMIS, and EHR systems"'], "Table 6 row 4, Medium-term."),
            ("Rule_DT04_12", ['"Data and interoperability"', '"Long-term"'], ['"Achieve full enterprise architecture interoperability across national HIE, track-and-trace, and global WHO GSMS platforms"'], "Table 6 row 4, Long-term."),
            ("Rule_DT04_13", ['"Technology and applications"', '"Short-term"'], ['"Deploy core digital SF reporting application (web/mobile with offline outbox SF-REP-006) in pilot regions"'], "Table 6 row 5, Short-term."),
            ("Rule_DT04_14", ['"Technology and applications"', '"Medium-term"'], ['"Scale application nationally with barcode scanning, multi-language support, and analytics dashboard"'], "Table 6 row 5, Medium-term."),
            ("Rule_DT04_15", ['"Technology and applications"', '"Long-term"'], ['"Operate high-availability national surveillance platform with advanced risk-based post-market surveillance analytics"'], "Table 6 row 5, Long-term."),
        ],
    },
]

def render_dmn(spec: dict) -> str:
    did = spec["id"]
    dname = spec["name"]
    ddoc = spec["doc"]
    hp = spec["hit_policy"]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/"',
        '             xmlns:dmndi="https://www.omg.org/spec/DMN/20191111/DMNDI/"',
        '             xmlns:dc="http://www.omg.org/spec/DMN/20180521/DC/"',
        f'             id="Definitions_{did}"',
        f'             name="{html.escape(dname)}"',
        '             namespace="https://litlfred.github.io/dth-sfp/decisions">',
        f'  <decision id="{did}" name="{html.escape(dname)}">',
        f'    <description>{html.escape(ddoc)}</description>',
        f'    <decisionTable id="DecisionTable_{did}" hitPolicy="{hp}">',
    ]
    for iid, ilabel, iexpr, itype in spec["inputs"]:
        lines += [
            f'      <input id="{iid}" label="{html.escape(ilabel)}">',
            f'        <inputExpression id="Expr_{iid}" typeRef="{itype}"><text>{iexpr}</text></inputExpression>',
            '      </input>',
        ]
    for oid, oname, olabel, otype in spec["outputs"]:
        lines.append(f'      <output id="{oid}" name="{oname}" label="{html.escape(olabel)}" typeRef="{otype}"/>')

    for rid, ins, outs, rdesc in spec["rules"]:
        lines.append(f'      <rule id="{rid}">')
        lines.append(f'        <description>{html.escape(rdesc)}</description>')
        for idx, iv in enumerate(ins, 1):
            lines.append(f'        <inputEntry id="{rid}_in_{idx}"><text>{html.escape(iv)}</text></inputEntry>')
        for idx, ov in enumerate(outs, 1):
            lines.append(f'        <outputEntry id="{rid}_out_{idx}"><text>{html.escape(ov)}</text></outputEntry>')
        lines.append('      </rule>')

    lines += [
        '    </decisionTable>',
        '  </decision>',
        '</definitions>',
        '',
    ]
    return "\n".join(lines)

for spec in DMN_SPECS:
    dmn_xml = render_dmn(spec)
    (DEC_DIR / spec["file"]).write_text(dmn_xml)
    (PROC_DEC_DIR / spec["file"]).write_text(dmn_xml)

dec_readme = """# Decision Tables (DMN 1.3) — `dth-sfp`

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
"""
(DEC_DIR / "README.md").write_text(dec_readme)
(PROC_DEC_DIR / "README.md").write_text(dec_readme)

print("Generated 6 BPMN files + SVGs + checklists and 4 DMN files.")
