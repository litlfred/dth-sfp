#!/usr/bin/env bun
/**
 * Validate this folio's glossary schemes against the platform's
 * folio-glossary/v1 schema, and check that every link resolves:
 *
 * - every `related` and `broader` reference in this instance's scheme names a
 *   term (or scheme) that exists here or in a mounted instance;
 * - every SKOS match (`exactMatch`, `closeMatch`, `broadMatch`, `narrowMatch`)
 *   into a MOUNTED instance's namespace (`dpi-h-ra`, `dth-sc`, `dth-pc`, `dth-hrh`)
 *   names a term in that instance's glossary;
 * - every glossary concept a block names in `meta.glossary` exists in this
 *   instance's glossary or a mounted instance's glossary;
 * - every ArchiMate element or view a block names in `meta.archimate` exists
 *   in the mounted dpi-h-ra model or in this DTH's own overlay (`archimate/`);
 * - the overlay adds nothing to smart-ra: each `overlay:base` copy names an item
 *   the pinned smart-ra model holds under the same id, and no item tagged
 *   `overlay:owner=dth-sfp` is already in smart-ra (owner, 2026-11-01, Q-RA1 A).
 *
 *   bun run scripts/glossary/validate.ts
 */
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { GlossarySchema } from "../../folio-assistant-core/schemas/glossary.ts";
import { instanceNs } from "../../folio-assistant-core/scripts/glossary-page.ts";

const MATCHES = ["exactMatch", "closeMatch", "broadMatch", "narrowMatch"] as const;

interface Instance {
  name: string;
  ns: string;
  root: string;
}

function instanceAt(root: string, file: string): Instance {
  const d = JSON.parse(readFileSync(join(root, file), "utf-8"));
  return { name: d.name, ns: instanceNs(d.name, d.stub, d), root };
}

/** Every term and scheme IRI an instance's `glossary/` declares. */
function glossaryIris(inst: Instance): {
  known: Set<string>;
  bareIds: Set<string>;
  docs: Array<{ f: string; g: ReturnType<typeof GlossarySchema.parse> }>;
} {
  const dir = join(inst.root, "glossary");
  const known = new Set<string>();
  const bareIds = new Set<string>();
  const docs: Array<{ f: string; g: ReturnType<typeof GlossarySchema.parse> }> = [];
  if (!existsSync(dir)) return { known, bareIds, docs };
  for (const f of readdirSync(dir).filter((x) => x.endsWith(".glossary.json"))) {
    const g = GlossarySchema.parse(JSON.parse(readFileSync(join(dir, f), "utf-8")));
    known.add(`${inst.ns}glossary/${g.id}`);
    for (const t of g.terms) {
      known.add(t.iri ?? `${inst.ns}glossary/${g.id}/${t.id}`);
      bareIds.add(t.id);
    }
    docs.push({ f, g });
  }
  return { known, bareIds, docs };
}

const self = instanceAt(".", "dth-sfp.json");
const mounted: Instance[] = [];
for (const [dir, file] of [
  ["dpi-h-ra", "dpi-h-ra.json"],
  ["dth-sc", "dth-sc.json"],
  ["dth-pc", "dth-pc.json"],
  ["dth-hrh", "dth-hrh.json"],
] as const) {
  if (existsSync(join(dir, file))) mounted.push(instanceAt(dir, file));
}

const here = glossaryIris(self);
const there = new Map(mounted.map((m) => [m, glossaryIris(m).known]));
let bad = 0;

function checkTermRef(ctx: string, r: string): boolean {
  if (!r.includes("://")) {
    if (!here.bareIds.has(r)) {
      console.error(`✗ ${ctx}: bare id "${r}" is not a term in ${self.name}`);
      bad++;
      return false;
    }
    return true;
  }
  if (r.startsWith(self.ns)) {
    if (!here.known.has(r)) {
      console.error(`✗ ${ctx}: ${r} is not a term in ${self.name}`);
      bad++;
      return false;
    }
    return true;
  }
  const inst = mounted.find((x) => r.startsWith(x.ns));
  if (inst && !there.get(inst)!.has(r)) {
    console.error(`✗ ${ctx}: ${r} is not a term in ${inst.name}`);
    bad++;
    return false;
  }
  return true;
}

for (const { f, g } of here.docs) {
  for (const t of g.terms) {
    if (!/^[A-Z]/.test(t.prefLabel)) {
      console.error(`✗ ${f}: ${t.id} prefLabel "${t.prefLabel}" is not Capitalized`);
      bad++;
    }
    for (const b of t.broader ?? []) {
      checkTermRef(`${f}: ${t.id} broader`, b);
    }
    for (const r of t.related ?? []) {
      checkTermRef(`${f}: ${t.id} related`, r);
    }
    for (const m of MATCHES) {
      for (const r of t[m] ?? []) {
        checkTermRef(`${f}: ${t.id} ${m}`, r);
      }
    }
  }
  const authored = g.terms.filter((t) => t.status === "authored").length;
  const linked = g.terms.filter((t) => MATCHES.some((m) => t[m]?.length)).length;
  console.log(`✓ ${f}: ${g.terms.length} terms (${authored} authored, ${linked} matched to another scheme)`);
}

// ── Glossary and ArchiMate links in block manifests ────────────────
const ra = mounted.find((m) => m.name === "dpi-h-ra");
if (ra && existsSync("folio/dth-sfp")) {
  const fail = (msg: string) => {
    console.error(`✗ ${msg}`);
    bad++;
  };
  const { readArchimate } = await import("../../cat-harness-tools/archimate/schemas/archimate.ts");
  type Loaded = { elements: Set<string>; views: Set<string>; all: Set<string>; model: ReturnType<typeof readArchimate> };
  const loadModels = (dir: string): Map<string, Loaded> => {
    const out = new Map<string, Loaded>();
    const cfgPath = join(dir, "cat-archimate.config.json");
    if (!existsSync(cfgPath)) return out;
    for (const cm of JSON.parse(readFileSync(cfgPath, "utf-8")).models ?? []) {
      const p = join(dir, cm.file);
      if (!existsSync(p)) continue;
      const model = readArchimate(readFileSync(p));
      const elements = new Set<string>(model.elements.map((e: { id: string }) => e.id));
      const views = new Set<string>(model.views.map((v: { id: string }) => v.id));
      const all = new Set<string>([...elements, ...views, ...model.relationships.map((r: { id: string }) => r.id)]);
      out.set(cm.id, { elements, views, all, model });
    }
    return out;
  };
  // ArchiMate models by owner: smart-ra's (mounted as dpi-h-ra) and this DTH's
  // own overlay (archimate/). A DTH builds an overlay and does not add to smart-ra.
  const byOwner: Record<string, Map<string, Loaded>> = {
    "smart-ra": loadModels(join(ra.root, "archimate")),
    "dth-sfp": loadModels("archimate"),
  };
  const ids = byOwner["smart-ra"];

  const raIriRe = /^https:\/\/litlfred\.github\.io\/smart-ra\/archimate\/([^/]+)\/(elements|views)\/([^/]+)\.jsonld$/;
  const dthIriRe = /^https:\/\/litlfred\.github\.io\/(dth-[a-z]+)\/archimate\/([^/]+)\/(elements|views)\/([^/]+)\.jsonld$/;
  const overlay = { owned: 0, base: 0, dth: 0 };
  for (const [ver, { model }] of byOwner["dth-sfp"]) {
    for (const e of [...model.elements, ...model.relationships, ...model.views]) {
      const prop = (k: string) => e.properties?.find((p: { key: string }) => p.key === k)?.value;
      const label = `archimate ${ver}: '${e.name || e.id}'`;
      const base = prop("overlay:base");
      const dth = prop("overlay:dth");
      if (base) {
        const m = base.match(raIriRe);
        if (!m) fail(`${label} has an overlay:base that is not a smart-ra ArchiMate IRI: ${base}`);
        else if (!ids.has(m[1])) fail(`${label} names smart-ra model ${m[1]}, which the pinned dpi-h-ra does not hold`);
        else if (m[3] !== e.id || !ids.get(m[1])!.all.has(m[3])) fail(`${label} copies ${m[3]}, which smart-ra ${m[1]} does not hold under this id`);
        else overlay.base++;
      } else if (dth) {
        const m = dth.match(dthIriRe);
        if (!m || m[1] === "dth-sfp" || m[4] !== e.id) fail(`${label} has an overlay:dth that is not another DTH's ArchiMate IRI for this id: ${dth}`);
        else overlay.dth++;
      } else if (prop("overlay:owner") === "dth-sfp") {
        for (const [rv, { all }] of ids) {
          if (all.has(e.id)) fail(`${label} (${e.id}) is owned by the overlay but smart-ra ${rv} already holds it; tag it overlay:base`);
        }
        overlay.owned++;
      } else {
        fail(`${label} (${e.id}) has none of overlay:base, overlay:dth, overlay:owner=dth-sfp`);
      }
    }
  }
  const iriRe = /^https:\/\/litlfred\.github\.io\/(smart-ra|dth-sfp)\/archimate\/([^/]+)\/(elements|views)\/([^/]+)\.jsonld$/;
  let archBlocks = 0;
  let archLinks = 0;
  let figMappings = 0;
  let glosBlocks = 0;
  let glosLinks = 0;
  const walk = (dir: string): string[] =>
    readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
      e.isDirectory() ? walk(join(dir, e.name)) : e.name.endsWith(".ts") ? [join(dir, e.name)] : [],
    );
  for (const file of walk("folio/dth-sfp")) {
    const src = readFileSync(file, "utf-8");
    if (!src.includes('"archimate"') && !src.includes('"glossary"')) continue;
    const m = src.match(/meta: (\{.*\}),\n/);
    if (!m) {
      console.error(`✗ ${file}: names "archimate" or "glossary" but its meta is not one line of JSON`);
      bad++;
      continue;
    }
    const meta = JSON.parse(m[1]);
    if (Array.isArray(meta.glossary) && meta.glossary.length > 0) {
      glosBlocks++;
      for (const gEntry of meta.glossary) {
        glosLinks++;
        checkTermRef(`${file} meta.glossary`, String(gEntry.iri));
      }
    }
    const a = meta.archimate;
    if (a) {
      archBlocks++;
      for (const x of [...(a.elements ?? []), ...(a.views ?? [])]) {
        archLinks++;
        const hit = String(x.iri).match(iriRe);
        const ok = hit && byOwner[hit[1]].get(hit[2])?.[hit[3] as "elements" | "views"].has(hit[4]);
        if (!ok) {
          console.error(`✗ ${file}: ${x.iri} (${x.name}) is not in the mounted dpi-h-ra ArchiMate model or the dth-sfp overlay`);
          bad++;
        }
      }
      for (const fm of a.figures ?? []) {
        figMappings++;
        const ok = [ids, byOwner["dth-sfp"]].some((o) => o.get(String(fm.model))?.views.has(String(fm.view)));
        if (!ok) {
          console.error(`✗ ${file}: figure ${fm.figure} view ${fm.view} is not in dpi-h-ra ArchiMate model ${fm.model}`);
          bad++;
        }
      }
    }
  }
  console.log(`✓ Glossary links: ${glosLinks} link(s) from ${glosBlocks} block(s) to dth-sfp / dpi-h-ra / dth-sc / dth-pc / dth-hrh checked`);
  console.log(
    `✓ ArchiMate: ${archLinks} link(s) and ${figMappings} figure-view mapping(s) from ${archBlocks} block(s) to dpi-h-ra and the dth-sfp overlay checked; overlay: ${overlay.owned} owned, ${overlay.base} smart-ra and ${overlay.dth} dth-phc reference copies`,
  );
} else {
  console.log("· dpi-h-ra or folio/dth-sfp is not present yet: ArchiMate and block glossary links not checked");
}
process.exit(bad ? 1 : 0);
