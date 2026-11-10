import { chapter, section } from "../../schema/builders";

export default chapter({
  title: "Introduction",
  label: "chap:00-introduction",
  sections: [
    section({
      title: "Introduction",
      label: "sec:00-introduction",
      blocks: ["f-fig-01", "f-fig-02", "p-sec-003", "p-sec-004", "p-sec-005", "p-sec-006", "p-sec-007", "t-table-01"],
    }),
  ],
});
