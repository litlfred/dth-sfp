import { chapter, section } from "../../schema/builders";

export default chapter({
  title: "Front matter (Imprint, Acknowledgements, Abbreviations and Glossary)",
  label: "chap:00-front-matter",
  sections: [
    section({
      title: "Front matter (Imprint, Acknowledgements, Abbreviations and Glossary)",
      label: "sec:00-front-matter",
      blocks: ["p-sec-000", "p-sec-001", "p-sec-002", "p-sec-front-matter", "t-abbreviations", "t-glossary"],
    }),
  ],
});
