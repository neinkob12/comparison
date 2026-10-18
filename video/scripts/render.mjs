// Rendert alle uebergebenen Videos: node scripts/render.mjs a01 b01
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const ids = process.argv.slice(2);
// Cloud-Container hat Chromium hier; lokal (Mac) laedt Remotion sich selbst einen Browser
const cloudChrome = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const browserExecutable = process.env.REMOTION_CHROME || (fs.existsSync(cloudChrome) ? cloudChrome : null);
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
fs.mkdirSync('../out', {recursive: true});
for (const id of ids) {
	const timeline = JSON.parse(fs.readFileSync(`public/timelines/${id}.json`, 'utf8'));
	const inputProps = {timeline};
	const composition = await selectComposition({serveUrl, id: 'Comparison', inputProps, browserExecutable});
	const out = `../out/${id}.mp4`;
	await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: out, inputProps, browserExecutable, concurrency: 4, crf: 20});
	console.log('fertig:', out);
}
