### Scenario 9: Paramedic reporting a suspected SF medical product (Table 9, PDF p. 40)

- **Actor / Persona:** `pers:sfp-r-09` (Paramedic)
- **Workflow:** `bp:sf-rep-001` (`SF-REP-001`), `bp:sf-rep-002` (`SF-REP-002`)

| Stage | Activity |
|---|---|
| **1. Initial discovery of a suspect medical product** | Encounters defective emergency medicine or airway/infusion supply in an ambulance or field emergency with intermittent connectivity. |
| **2. Reporting the suspect product** | Records SF report in the mobile app offline outbox (subprocess SF-REP-006). |
| **3. Providing product details** | Scans barcode or enters product name, batch number, and expiry date offline. |
| **4. Uploading photos** | Attaches photos stored locally until connectivity is restored. |
| **5. Receiving confirmation and a tracking number** | App automatically syncs when online and delivers confirmation and tracking number. |
| **6. Follow-up and feedback** | Receives fleet/emergency medical services safety notice and NMRA follow-up. |
