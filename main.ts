// Entry point for the news-image-20261124 entry,
// "The World in One Day — 24 November 2026".
//
// The finished front-page image ships in this repository as
// entry.png, drawn by build_image.py. This program's single task
// is to deliver that image to the harness output location:
// /output/entry.png, or $MAKEFUN_OUTPUT_DIR/entry.png when the
// harness redirects the output directory.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const imagePath = join(repoDir, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(imagePath, target);
console.log(`entry.png written to ${target}`);
