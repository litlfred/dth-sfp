#!/usr/bin/env bun
/**
 * As-drawn figure SVGs for dth-sfp, generated from schema-backed data.
 *
 * The handbook's figures (who-iris/library/9789240120747-eng) are redrawn as
 * SVG that keeps each original's layout and style, from ONE data file per
 * figure under `figure-data/` (owner, 2026-11-16, litlfred/dth-sfp#11):
 *
 * - `as-drawn-figure/v1` (`*.json`): the drawing transcribed from the PDF's
 *   vector layer: semantic groups (`role`, optional glossary `concept` IRI)
 *   holding rects, paths, lines and text. Every label is SVG `<text>`, never
 *   pixels, and a label that names a glossary concept links to it.
 * - `as-drawn-bpmn-figure/v1` (`*.json`): a figure that IS a workflow points
 *   at a BPMN 2.0 file with diagram interchange (`bpmndi`) coordinates taken
 *   from the render, and is drawn from that file in the printed style.
 *
 * The generator holds no labels: every string comes from the data or the
 * BPMN file. The PDF crop stays the cited source (`figure.crop`).
 *
 *   bun run scripts/figures/as-drawn.ts            # write SVGs and JSON Schemas
 *   bun run scripts/figures/as-drawn.ts --check    # fail when either is stale
 */
import { existsSync, readdirSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { z } from "zod";
import { DOMParser } from "@xmldom/xmldom";

// ---------------------------------------------------------------------------
// Schema
// ---------------------------------------------------------------------------

const Num = z.number().finite();
const Point = z.tuple([Num, Num]);
/** A colour: hex, `none`, or a key of the figure's `palette`. */
const Colour = z.string().regex(/^(#[0-9a-fA-F]{6}|none|[a-z][a-zA-Z0-9-]*)$/);
const RelPath = z
  .string()
  .refine((f) => !f.startsWith("/") && !f.split("/").includes(".."), "relative to the repository root, without `..`");

const Common = {
  /** A stable id, unique in the figure. */
  id: z.string().regex(/^[a-z0-9][a-z0-9-]*$/).optional(),
  /** What this shape is in the figure, e.g. `layer`, `band`, `legend-item`. */
  role: z.string().optional(),
  /** A glossary concept IRI the shape names; the SVG links to it. */
  concept: z.string().url().optional(),
};
const Paint = {
  fill: Colour.optional(),
  stroke: Colour.optional(),
  strokeWidth: Num.nonnegative().optional(),
  dash: z.array(Num.nonnegative()).optional(),
  opacity: Num.min(0).max(1).optional(),
  fillRule: z.enum(["nonzero", "evenodd"]).optional(),
};

export const RectSchema = z.object({ kind: z.literal("rect"), ...Common, x: Num, y: Num, w: Num.nonnegative(), h: Num.nonnegative(), rx: Num.nonnegative().optional(), ...Paint }).strict();
export const PathSchema = z.object({ kind: z.literal("path"), ...Common, d: z.string().min(1), ...Paint }).strict();
export const LineSchema = z
  .object({
    kind: z.literal("line"),
    ...Common,
    points: z.array(Point).min(2),
    stroke: Colour,
    strokeWidth: Num.nonnegative().optional(),
    dash: z.array(Num.nonnegative()).optional(),
    /** Arrowheads, drawn in the line's colour. */
    arrow: z.enum(["start", "end", "both"]).optional(),
  })
  .strict();
export const CircleSchema = z.object({ kind: z.literal("circle"), ...Common, cx: Num, cy: Num, r: Num.positive(), ...Paint }).strict();
export const TextSchema = z
  .object({
    kind: z.literal("text"),
    ...Common,
    /** Start of the first line's baseline (before rotation). */
    x: Num,
    y: Num,
    /** The lines as printed: the source's own line breaks and wording. */
    lines: z.array(z.string()).min(1),
    /**
     * Each line's printed width, so the SVG keeps the printed line lengths
     * (`textLength`) when the reader's font is not the publication's.
     */
    widths: z.array(Num.positive()).optional(),
    size: Num.positive(),
    lineHeight: Num.positive().optional(),
    weight: z.enum(["light", "regular", "semibold", "bold"]).optional(),
    italic: z.boolean().optional(),
    condensed: z.boolean().optional(),
    fill: Colour,
    anchor: z.enum(["start", "middle", "end"]).optional(),
    /** -90 reads bottom to top, 90 top to bottom, about (x, y). */
    rotate: z.union([z.literal(-90), z.literal(90)]).optional(),
  })
  .strict();
export const UseSchema = z
  .object({ kind: z.literal("use"), ...Common, symbol: z.string().min(1), x: Num, y: Num, scale: Num.positive().optional() })
  .strict();

export type Element =
  | z.infer<typeof RectSchema>
  | z.infer<typeof PathSchema>
  | z.infer<typeof LineSchema>
  | z.infer<typeof CircleSchema>
  | z.infer<typeof TextSchema>
  | z.infer<typeof UseSchema>
  | { kind: "group"; id?: string; role?: string; concept?: string; label?: string; children: Element[] };

export const ElementSchema: z.ZodType<Element> = z.lazy(() =>
  z.union([RectSchema, PathSchema, LineSchema, CircleSchema, TextSchema, UseSchema, GroupSchema]),
);
export const GroupSchema = z
  .object({
    kind: z.literal("group"),
    ...Common,
    /** What the group is called in the figure, when it has a name. */
    label: z.string().optional(),
    children: z.array(z.lazy(() => ElementSchema)),
  })
  .strict();

/** Where the figure comes from: the publication, its page and the crop. */
export const FigureSourceSchema = z
  .object({
    /** The who-iris library entry. */
    library: z.string().regex(/^\d{13}-[a-z]{3}$/),
    /** What the publication calls it, e.g. `Fig. 3`. */
    label: z.string().regex(/^Fig\. \d+$/),
    caption: z.string().min(1),
    /** PDF page (1-based). */
    page: z.number().int().positive(),
    /** The L1 section that prints the caption, relative to the repository root. */
    section: RelPath,
    /** The PDF crop, kept as the cited source. */
    crop: RelPath,
    /** The drawing's region on the PDF page, in points: [x0, top, x1, bottom]. */
    region: z.tuple([Num, Num, Num, Num]),
    /** A printed source line under the figure ("Adapted from ..."), as printed. */
    credit: z.string().optional(),
    /** How the data was made, and anything a reviewer should know. */
    notes: z.array(z.string()).optional(),
  })
  .strict();

export const SymbolSchema = z
  .object({ width: Num.positive(), height: Num.positive(), title: z.string().optional(), children: z.array(z.lazy(() => ElementSchema)) })
  .strict();

export const AsDrawnFigureSchema = z
  .object({
    $schema: z.literal("as-drawn-figure/v1"),
    figure: FigureSourceSchema,
    /** The SVG this data draws, relative to the repository root. */
    out: RelPath.refine((f) => f.endsWith(".svg"), "an .svg file"),
    /** Canvas size, in PDF points (the units of every coordinate). */
    width: Num.positive(),
    height: Num.positive(),
    /** Output pixels per point (the crop PNG is 2). */
    scale: Num.positive().default(2),
    font: z.string().min(1),
    background: Colour.optional(),
    palette: z.record(z.string(), z.string().regex(/^#[0-9a-fA-F]{6}$/)).default({}),
    /** Pictograms the figure repeats, drawn once and placed with `use`. */
    symbols: z.record(z.string(), SymbolSchema).default({}),
    elements: z.array(ElementSchema),
  })
  .strict();
export type AsDrawnFigure = z.infer<typeof AsDrawnFigureSchema>;

/** A workflow figure drawn from a BPMN 2.0 file in the printed style. */
export const AsDrawnBpmnFigureSchema = z
  .object({
    $schema: z.literal("as-drawn-bpmn-figure/v1"),
    figure: FigureSourceSchema,
    out: RelPath.refine((f) => f.endsWith(".svg"), "an .svg file"),
    /** The BPMN 2.0 file, with bpmndi coordinates in output pixels. */
    bpmn: RelPath.refine((f) => f.endsWith(".bpmn"), "a .bpmn file"),
    width: Num.positive(),
    height: Num.positive(),
    font: z.string().min(1),
    style: z
      .object({
        task: z.object({ fill: Colour, text: Colour, number: Colour, size: Num.positive(), lineHeight: Num.positive() }).strict(),
        gateway: z.object({ fill: Colour, text: Colour, number: Colour, mark: Colour, size: Num.positive(), lineHeight: Num.positive() }).strict(),
        event: z.object({ stroke: Colour, strokeWidth: Num.positive(), text: Colour, size: Num.positive() }).strict(),
        lane: z.object({ fill: Colour, text: Colour, size: Num.positive(), width: Num.positive() }).strict(),
        flow: z.object({ stroke: Colour, strokeWidth: Num.positive(), labelled: Colour, arrow: Num.positive() }).strict(),
      })
      .strict(),
    /** Glossary concepts a task or gateway names, by BPMN id. */
    concepts: z.record(z.string(), z.string().url()).default({}),
  })
  .strict();
export type AsDrawnBpmnFigure = z.infer<typeof AsDrawnBpmnFigureSchema>;

// ---------------------------------------------------------------------------
// SVG
// ---------------------------------------------------------------------------

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const n = (v: number) => String(Math.round(v * 100) / 100);
const WEIGHT = { light: 300, regular: 400, semibold: 600, bold: 700 } as const;

function colour(c: string | undefined, palette: Record<string, string>): string | undefined {
  if (c === undefined) return undefined;
  if (c.startsWith("#") || c === "none") return c;
  const v = palette[c];
  if (!v) throw new Error(`colour "${c}" is not in the palette`);
  return v;
}

function paintAttrs(e: { fill?: string; stroke?: string; strokeWidth?: number; dash?: number[]; opacity?: number; fillRule?: string }, palette: Record<string, string>, defFill = "none"): string {
  const a: string[] = [`fill="${colour(e.fill, palette) ?? defFill}"`];
  if (e.fillRule === "evenodd") a.push(`fill-rule="evenodd"`);
  const s = colour(e.stroke, palette);
  if (s) a.push(`stroke="${s}"`, `stroke-width="${n(e.strokeWidth ?? 0.5)}"`);
  if (e.dash?.length) a.push(`stroke-dasharray="${e.dash.map(n).join(" ")}"`);
  if (e.opacity !== undefined) a.push(`opacity="${n(e.opacity)}"`);
  return a.join(" ");
}

function arrowHead(tip: [number, number], from: [number, number], fill: string, size: number): string {
  const ang = Math.atan2(tip[1] - from[1], tip[0] - from[0]);
  const l = size * 1.6, w = size;
  const bx = tip[0] - l * Math.cos(ang), by = tip[1] - l * Math.sin(ang);
  const px = (w / 2) * Math.sin(ang), py = (w / 2) * Math.cos(ang);
  return `<path d="M${n(tip[0])} ${n(tip[1])}L${n(bx + px)} ${n(by - py)}L${n(bx - px)} ${n(by + py)}Z" fill="${fill}"/>`;
}

function textSvg(t: z.infer<typeof TextSchema>, palette: Record<string, string>, font: string): string {
  const lh = t.lineHeight ?? t.size * 1.2;
  const attrs = [
    `x="${n(t.x)}"`, `y="${n(t.y)}"`, `font-family="${esc(font)}"`, `font-size="${n(t.size)}"`,
    `fill="${colour(t.fill, palette)}"`,
  ];
  if (t.weight && t.weight !== "regular") attrs.push(`font-weight="${WEIGHT[t.weight]}"`);
  if (t.italic) attrs.push(`font-style="italic"`);
  if (t.condensed) attrs.push(`font-stretch="condensed"`);
  if (t.anchor && t.anchor !== "start") attrs.push(`text-anchor="${t.anchor}"`);
  if (t.rotate) attrs.push(`transform="rotate(${t.rotate} ${n(t.x)} ${n(t.y)})"`);
  if (t.widths && t.widths.length !== t.lines.length) throw new Error(`text "${t.lines[0]}": ${t.widths.length} widths for ${t.lines.length} lines`);
  const fit = (i: number) => (t.widths ? ` textLength="${n(t.widths[i]!)}" lengthAdjust="spacingAndGlyphs"` : "");
  const body = t.lines.length === 1 && !t.widths
    ? esc(t.lines[0]!)
    : t.lines.map((l, i) => `<tspan x="${n(t.x)}"${i === 0 ? "" : ` dy="${n(lh)}"`}${fit(i)}>${esc(l)}</tspan>`).join("");
  return `<text ${attrs.join(" ")}>${body}</text>`;
}

function link(e: { concept?: string }, inner: string): string {
  return e.concept ? `<a href="${esc(e.concept)}" target="_blank">${inner}</a>` : inner;
}

function elementSvg(e: Element, fig: Pick<AsDrawnFigure, "palette" | "font">): string {
  const p = fig.palette;
  const idAttr = (e as { id?: string }).id ? ` id="${(e as { id?: string }).id}"` : "";
  const roleAttr = (e as { role?: string }).role ? ` data-role="${esc((e as { role?: string }).role!)}"` : "";
  switch (e.kind) {
    case "rect":
      return link(e, `<rect${idAttr}${roleAttr} x="${n(e.x)}" y="${n(e.y)}" width="${n(e.w)}" height="${n(e.h)}"${e.rx ? ` rx="${n(e.rx)}"` : ""} ${paintAttrs(e, p)}/>`);
    case "path":
      return link(e, `<path${idAttr}${roleAttr} d="${e.d}" ${paintAttrs(e, p)}/>`);
    case "circle":
      return link(e, `<circle${idAttr}${roleAttr} cx="${n(e.cx)}" cy="${n(e.cy)}" r="${n(e.r)}" ${paintAttrs(e, p)}/>`);
    case "line": {
      const s = colour(e.stroke, p)!;
      const w = e.strokeWidth ?? 0.5;
      const pts = e.points;
      const out = [`<polyline${idAttr}${roleAttr} points="${pts.map(([x, y]) => `${n(x)},${n(y)}`).join(" ")}" fill="none" stroke="${s}" stroke-width="${n(w)}"${e.dash?.length ? ` stroke-dasharray="${e.dash.map(n).join(" ")}"` : ""}/>`];
      const head = Math.max(2.2, w * 4.4);
      if (e.arrow === "end" || e.arrow === "both") out.push(arrowHead(pts[pts.length - 1]!, pts[pts.length - 2]!, s, head));
      if (e.arrow === "start" || e.arrow === "both") out.push(arrowHead(pts[0]!, pts[1]!, s, head));
      return out.join("");
    }
    case "text":
      return link(e, textSvg(e, p, fig.font));
    case "use":
      return link(e, `<use${idAttr}${roleAttr} href="#sym-${e.symbol}" transform="translate(${n(e.x)} ${n(e.y)})${e.scale ? ` scale(${n(e.scale)})` : ""}"/>`);
    case "group": {
      const label = e.label ? `<title>${esc(e.label)}</title>` : "";
      return link(e, `<g${idAttr}${roleAttr}>${label}${e.children.map((c) => elementSvg(c, fig)).join("")}</g>`);
    }
  }
}

export function renderAsDrawn(fig: AsDrawnFigure): string {
  const W = fig.width, H = fig.height, s = fig.scale;
  for (const name of usedSymbols(fig.elements)) if (!fig.symbols[name]) throw new Error(`symbol "${name}" is not declared`);
  const defs = Object.entries(fig.symbols)
    .map(([k, sym]) => `<symbol id="sym-${k}" viewBox="0 0 ${n(sym.width)} ${n(sym.height)}" width="${n(sym.width)}" height="${n(sym.height)}" overflow="visible">${sym.title ? `<title>${esc(sym.title)}</title>` : ""}${sym.children.map((c) => elementSvg(c, fig)).join("")}</symbol>`)
    .join("");
  const title = `${fig.figure.label}. ${fig.figure.caption}`;
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n(W)} ${n(H)}" width="${n(W * s)}" height="${n(H * s)}" role="img" aria-labelledby="title">`,
    `<title id="title">${esc(title)}</title>`,
    `<desc>As drawn in WHO, Digital transformation handbook for reporting substandard and falsified medical products (2025), ${esc(fig.figure.label)}, PDF p. ${fig.figure.page}. Generated by dth-sfp scripts/figures/as-drawn.ts from ${esc(dataPathOf(fig))}.</desc>`,
    defs ? `<defs>${defs}</defs>` : "",
    fig.background ? `<rect width="${n(W)}" height="${n(H)}" fill="${colour(fig.background, fig.palette)}"/>` : "",
    ...fig.elements.map((e) => elementSvg(e, fig)),
    `</svg>`,
    "",
  ].join("\n");
}

function usedSymbols(els: Element[], acc = new Set<string>()): Set<string> {
  for (const e of els) {
    if (e.kind === "use") acc.add(e.symbol);
    if (e.kind === "group") usedSymbols(e.children, acc);
  }
  return acc;
}

const dataPaths = new WeakMap<object, string>();
const dataPathOf = (fig: object) => dataPaths.get(fig) ?? "figure data";

// ---------------------------------------------------------------------------
// BPMN, drawn in the printed style
// ---------------------------------------------------------------------------

const BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL";
const BPMNDI = "http://www.omg.org/spec/BPMN/20100524/DI";
const DC = "http://www.omg.org/spec/DD/20100524/DC";
const DI = "http://www.omg.org/spec/DD/20100524/DI";
/** dth-sfp's extension attribute for the step number a figure prints on a node. */
export const SFP_NS = "https://litlfred.github.io/dth-sfp/ns/figure#";

interface Bounds { x: number; y: number; w: number; h: number }

export function renderBpmnAsDrawn(fig: AsDrawnBpmnFigure, xml: string): string {
  const doc = new DOMParser().parseFromString(xml, "text/xml");
  const byId = new Map<string, globalThis.Element>();
  const all = doc.getElementsByTagNameNS(BPMN, "*");
  for (let i = 0; i < all.length; i++) {
    const el = all.item(i)!;
    const id = el.getAttribute("id");
    if (id) byId.set(id, el as unknown as globalThis.Element);
  }
  const shapes = doc.getElementsByTagNameNS(BPMNDI, "BPMNShape");
  const edges = doc.getElementsByTagNameNS(BPMNDI, "BPMNEdge");
  const bounds = (el: globalThis.Element): Bounds => {
    const b = el.getElementsByTagNameNS(DC, "Bounds").item(0);
    if (!b) throw new Error(`${el.getAttribute("bpmnElement")}: no dc:Bounds`);
    return { x: +b.getAttribute("x")!, y: +b.getAttribute("y")!, w: +b.getAttribute("width")!, h: +b.getAttribute("height")! };
  };
  const st = fig.style;
  const F = esc(fig.font);
  const name = (el: globalThis.Element) => (el.getAttribute("name") ?? "").split("\n");
  const textLines = (lines: string[], x: number, y: number, size: number, lh: number, fill: string, anchor = "start", weight?: number) =>
    `<text x="${n(x)}" y="${n(y)}" font-family="${F}" font-size="${n(size)}" fill="${fill}"${anchor !== "start" ? ` text-anchor="${anchor}"` : ""}${weight ? ` font-weight="${weight}"` : ""}>` +
    lines.map((l, i) => `<tspan x="${n(x)}"${i ? ` dy="${n(lh)}"` : ""}>${esc(l)}</tspan>`).join("") + `</text>`;
  const out: string[] = [];
  const wrapConcept = (id: string, inner: string) => (fig.concepts[id] ? `<a href="${esc(fig.concepts[id]!)}" target="_blank">${inner}</a>` : inner);

  // Lanes first, then flows, then nodes on top.
  const nodes: string[] = [];
  for (let i = 0; i < shapes.length; i++) {
    const sh = shapes.item(i)!;
    const ref = sh.getAttribute("bpmnElement")!;
    const el = byId.get(ref);
    if (!el) throw new Error(`BPMNShape names unknown element ${ref}`);
    const b = bounds(sh);
    const kind = el.localName;
    const step = el.getAttributeNS(SFP_NS, "step");
    if (kind === "lane" || kind === "participant") {
      const L = st.lane;
      out.push(wrapConcept(ref, `<g data-role="lane" id="${esc(ref)}"><rect x="${n(b.x)}" y="${n(b.y)}" width="${n(L.width)}" height="${n(b.h)}" fill="${L.fill}"/>` +
        `<text x="${n(b.x + L.width * 0.73)}" y="${n(b.y + b.h / 2)}" font-family="${F}" font-size="${n(L.size)}" fill="${L.text}" text-anchor="middle" transform="rotate(-90 ${n(b.x + L.width * 0.73)} ${n(b.y + b.h / 2)})">${esc(name(el).join(" "))}</text></g>`));
    } else if (kind === "task" || kind.endsWith("Task")) {
      const T = st.task;
      nodes.push(wrapConcept(ref, `<g data-role="task" id="${esc(ref)}"><rect x="${n(b.x)}" y="${n(b.y)}" width="${n(b.w)}" height="${n(b.h)}" fill="${T.fill}"/>` +
        textLines(name(el), b.x + T.size * 0.39, b.y + T.size * 1.34, T.size, T.lineHeight, T.text) +
        (step ? `<text x="${n(b.x + b.w - T.size * 0.63)}" y="${n(b.y + b.h - T.size * 0.43)}" font-family="${F}" font-size="${n(T.size * 1.11)}" font-weight="700" fill="${T.number}" text-anchor="end">${esc(step)}</text>` : "") + `</g>`));
    } else if (kind === "exclusiveGateway") {
      const G = st.gateway;
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2, mw = b.w * 0.094, mh = b.h * 0.094;
      const mx = cx, my = b.y + b.h * 0.232;
      nodes.push(wrapConcept(ref, `<g data-role="gateway" id="${esc(ref)}"><path d="M${n(cx)} ${n(b.y)}L${n(b.x + b.w)} ${n(cy)}L${n(cx)} ${n(b.y + b.h)}L${n(b.x)} ${n(cy)}Z" fill="${G.fill}"/>` +
        `<path d="M${n(mx - mw)} ${n(my - mh)}L${n(mx + mw)} ${n(my + mh)}M${n(mx + mw)} ${n(my - mh)}L${n(mx - mw)} ${n(my + mh)}" stroke="${G.mark}" stroke-width="${n(b.w * 0.05)}"/>` +
        textLines(name(el), cx, cy - G.lineHeight * (name(el).length - 1) / 2 + G.size * 0.52, G.size, G.lineHeight, G.text, "middle") +
        (step ? `<text x="${n(cx)}" y="${n(b.y + b.h * 0.845)}" font-family="${F}" font-size="${n(G.size * 0.93)}" font-weight="700" fill="${G.number}" text-anchor="middle">${esc(step)}</text>` : "") + `</g>`));
    } else if (kind === "startEvent" || kind === "endEvent") {
      const E = st.event;
      const r = b.w / 2;
      const label = name(el).filter(Boolean);
      nodes.push(`<g data-role="${kind}" id="${esc(ref)}"><circle cx="${n(b.x + r)}" cy="${n(b.y + r)}" r="${n(r - E.strokeWidth / 2)}" fill="#ffffff" stroke="${E.stroke}" stroke-width="${n(E.strokeWidth)}"/>` +
        (label.length ? `<text x="${n(b.x + r)}" y="${n(b.y + r + E.size * 0.27)}" font-family="${F}" font-size="${n(E.size)}" font-weight="700" font-stretch="condensed" fill="${E.text}" text-anchor="middle" textLength="${n(b.w * 0.58)}" lengthAdjust="spacingAndGlyphs">${esc(label.join(" "))}</text>` : "") + `</g>`);
    } else {
      throw new Error(`${ref}: BPMN ${kind} has no as-drawn style`);
    }
  }
  for (let i = 0; i < edges.length; i++) {
    const ed = edges.item(i)!;
    const ref = ed.getAttribute("bpmnElement")!;
    const el = byId.get(ref);
    if (!el || el.localName !== "sequenceFlow") throw new Error(`BPMNEdge names ${ref}, not a sequenceFlow`);
    const wps = ed.getElementsByTagNameNS(DI, "waypoint");
    const pts: [number, number][] = [];
    for (let j = 0; j < wps.length; j++) pts.push([+wps.item(j)!.getAttribute("x")!, +wps.item(j)!.getAttribute("y")!]);
    const label = el.getAttribute("name");
    const F2 = st.flow;
    const strokeC = label ? F2.labelled : F2.stroke;
    let s = `<g data-role="flow" id="${esc(ref)}"><polyline points="${pts.map(([x, y]) => `${n(x)},${n(y)}`).join(" ")}" fill="none" stroke="${strokeC}" stroke-width="${n(F2.strokeWidth)}"/>` +
      arrowHead(pts[pts.length - 1]!, pts[pts.length - 2]!, strokeC, F2.arrow);
    const lb = ed.getElementsByTagNameNS(BPMNDI, "BPMNLabel").item(0);
    if (label && lb) {
      const b = bounds(lb);
      // The label's bounds are its text box: the height is the font size, the bottom the baseline.
      s += `<text x="${n(b.x)}" y="${n(b.y + b.h)}" font-family="${F}" font-size="${n(b.h)}" fill="${F2.labelled}">${esc(label)}</text>`;
    }
    out.push(s + `</g>`);
  }
  const title = `${fig.figure.label}. ${fig.figure.caption}`;
  return [
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n(fig.width)} ${n(fig.height)}" width="${n(fig.width)}" height="${n(fig.height)}" role="img" aria-labelledby="title">`,
    `<title id="title">${esc(title)}</title>`,
    `<desc>As drawn in WHO, Digital transformation handbook for reporting substandard and falsified medical products (2025), ${esc(fig.figure.label)}, PDF p. ${fig.figure.page}. Generated by dth-sfp scripts/figures/as-drawn.ts from ${esc(fig.bpmn)}.</desc>`,
    ...out,
    ...nodes,
    `</svg>`,
    "",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

export const SCHEMA_FILES = {
  "as-drawn-figure.v1.schema.json": AsDrawnFigureSchema,
  "as-drawn-bpmn-figure.v1.schema.json": AsDrawnBpmnFigureSchema,
} as const;

export function jsonSchemaText(file: keyof typeof SCHEMA_FILES): string {
  const js = z.toJSONSchema(SCHEMA_FILES[file], { io: "input", unrepresentable: "any" }) as Record<string, unknown>;
  return JSON.stringify({ $id: `https://litlfred.github.io/dth-sfp/v0/figure-data/schemas/${file}`, ...js }, null, 2) + "\n";
}

export function build(root: string, check: boolean): string[] {
  const problems: string[] = [];
  const emit = (path: string, text: string) => {
    const abs = join(root, path);
    if (check) {
      if (!existsSync(abs) || readFileSync(abs, "utf8") !== text) problems.push(`${path} is stale: run \`bun run figures:svg\``);
    } else {
      mkdirSync(dirname(abs), { recursive: true });
      writeFileSync(abs, text);
    }
  };
  for (const f of Object.keys(SCHEMA_FILES) as (keyof typeof SCHEMA_FILES)[]) emit(`figure-data/schemas/${f}`, jsonSchemaText(f));
  const dir = join(root, "figure-data");
  for (const f of readdirSync(dir).filter((f) => f.endsWith(".json")).sort()) {
    const raw = JSON.parse(readFileSync(join(dir, f), "utf8"));
    const rel = `figure-data/${f}`;
    if (raw.$schema === "as-drawn-figure/v1") {
      const r = AsDrawnFigureSchema.safeParse(raw);
      if (!r.success) { problems.push(`${rel}: ${z.prettifyError(r.error)}`); continue; }
      dataPaths.set(r.data, rel);
      emit(r.data.out, renderAsDrawn(r.data));
    } else if (raw.$schema === "as-drawn-bpmn-figure/v1") {
      const r = AsDrawnBpmnFigureSchema.safeParse(raw);
      if (!r.success) { problems.push(`${rel}: ${z.prettifyError(r.error)}`); continue; }
      emit(r.data.out, renderBpmnAsDrawn(r.data, readFileSync(join(root, r.data.bpmn), "utf8")));
    }
  }
  return problems;
}

if (import.meta.main) {
  const check = process.argv.includes("--check");
  const root = resolve(import.meta.dir, "../..");
  const problems = build(root, check);
  for (const p of problems) console.error(`  ✗ ${p}`);
  if (problems.length) process.exit(1);
  console.log(check ? "as-drawn figures: up to date" : "as-drawn figures: written");
}
