import { paper, chapterRef } from "../schema/builders";

export default paper({
  title: "Digital transformation handbook for reporting substandard and falsified medical products",
  authors: ["World Health Organization"],
  date: "2026",
  meta: {
    documentKind: "smart-base:dth",
    level: "L2",
    targetLevel: "L2",
    isbn: "9789240120747",
    iris: "10665/384624",
    source: { library: "9789240120747-eng", repository: "litlfred/who-iris" },
    licence: "CC BY-NC-SA 3.0 IGO",
    status: "complete L2 DTH folio (litlfred/dth-sfp#1 Steps P4–P7): 43 outline sections, 27 structured tables, 6 figures, 15 personas (SFP-R-01..15), 9 user scenarios, 6 BPMN 2.0 processes (SF-REP-001..006), 4 DMN 1.3 decision tables (SFR.DT.01..04), 10 data elements (SFR.A1.DE1..10), 7 functional requirements, 11 non-functional requirement categories, 5 indicators, and 100% L1 normative coverage",
    figureViews: [
      { figure: "Fig. 1", block: "folio/dth-sfp/00-introduction/f-fig-01.md", model: "0.3.0-draft.1", view: "id-4e6e25746e8d4398add06fcbc4fb5a4e", viewName: "Capabilities-Goals" },
      { figure: "Fig. 2", block: "folio/dth-sfp/00-introduction/f-fig-02.md", model: "0.3.0-draft.1", view: "id-8c5dd12b8d4e425184f6003d0513d569", viewName: "Interoperability Layer" },
      { figure: "Fig. 3", block: "folio/dth-sfp/ch03-future-state/f-fig-03.md", model: "0.3.0-draft.1", view: "id-92267636cc42566ca5d2cff0e81be8c9", viewName: "DHSC Architecture Framework (DTH SC Fig. 14)" },
      { figure: "Fig. 4", block: "folio/dth-sfp/ch04-determine-requirements/f-fig-04.md", model: "0.3.0-draft.1", view: "id-bea56e01c8345fbc803dee47a17ccfd3", viewName: "Track and Trace through DHSC Components (DTH SC Fig. 24)" },
      { figure: "Fig. 5", block: "folio/dth-sfp/ch06-monitor-evaluate-scale/f-fig-05.md", model: "0.3.0-draft.1", view: "id-4e6e25746e8d4398add06fcbc4fb5a4e", viewName: "Capabilities-Goals" },
      { figure: "Fig. 6", block: "folio/dth-sfp/ch06-monitor-evaluate-scale/f-fig-06.md", model: "0.3.0-draft.1", view: "id-4e6e25746e8d4398add06fcbc4fb5a4e", viewName: "Capabilities-Goals" },
    ],
  },
  chapters: [
    chapterRef({ dir: "00-front-matter" }),
    chapterRef({ dir: "00-introduction" }),
    chapterRef({ dir: "ch01-assess-current-state" }),
    chapterRef({ dir: "ch02-shared-understanding-governance" }),
    chapterRef({ dir: "ch03-future-state" }),
    chapterRef({ dir: "ch04-determine-requirements" }),
    chapterRef({ dir: "ch05-plan-implementation" }),
    chapterRef({ dir: "ch06-monitor-evaluate-scale" }),
    chapterRef({ dir: "ch07-share-experiences" }),
    chapterRef({ dir: "references-resources" }),
    chapterRef({ dir: "annexes" }),
  ],
});
