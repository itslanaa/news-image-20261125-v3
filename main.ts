// News Image 20261125 — entrypoint (Node 22, standard library only).
//
// Front page: The World in One Day — Wednesday 25 November 2026.
// The front page is rendered ahead of time and shipped in this repository
// as entry.png, because the grading container has no Python or PIL and
// cannot draw it at run time. All this program does is place a copy of
// that finished image where the grader expects it.
//
// No network, no subprocess, no generated code: one file in, one file out,
// the same bytes on every run, twice in a row.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const IMAGE_NAME = "entry.png";
const FALLBACK_OUTPUT = "/output";

const sourceImage = new URL(`./${IMAGE_NAME}`, import.meta.url);
const destinationDir =
  process.env.MAKEFUN_OUTPUT_DIR ?? FALLBACK_OUTPUT;

mkdirSync(destinationDir, { recursive: true });
copyFileSync(sourceImage, join(destinationDir, IMAGE_NAME));
