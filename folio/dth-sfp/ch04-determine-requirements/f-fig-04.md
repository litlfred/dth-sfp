![Fig. 4. Workflow for reporting substandard and falsified medical products (L1 source diagram, p. 30 / PDF p. 42)](../media/vfig-p042.png)

*Source: `who-iris/library/9789240120747-eng/media/figures/vfig-p042.png` (PDF page 42). Mapped to `dpi-h-ra` ArchiMate view `Track and Trace through DHSC Components (DTH SC Fig. 24)` (`id-bea56e01c8345fbc803dee47a17ccfd3`).*

> [!WARNING]
> **Source Figure Review Findings (`litlfred/dth-sfp#1` §3):**
> - **F2: Fig. 4 omits the third WHO SF category ('unregistered/unlicensed medical products', p. ix & p. 1).**
> - **F5: Fig. 4 contains 5 BPMN 2.0 defects (step 2 repeats gateway 1; gateway 1 has an unlabelled bypass to End; gateway 5 is labelled 'Select type of report' rather than a question; step numbers 6-8 repeat on both branches; symbols deviate from Annex 3). Preserved as the L1 source figure and redrawn cleanly in bp:sf-rep-001 (processes/SF-REP-001.bpmn).**
