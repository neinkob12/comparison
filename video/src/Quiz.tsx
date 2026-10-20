import React from 'react';
import {
	AbsoluteFill, Audio, Loop, OffthreadVideo, Sequence, interpolate, spring, staticFile,
	useCurrentFrame, useVideoConfig,
} from 'remotion';

type Word = {w: string; s: number; e: number};
type Segment = {
	kind: 'intro' | 'q' | 'outro';
	audio: string; words: Word[]; speak: number; duration: number;
	title?: string; sub?: string;
	n?: number; word?: string; answer?: string; timer?: number; revealAt?: number;
	answerAudio?: string; answerWords?: Word[];
};
export type QuizTimeline = {
	id: string; format: 'quiz'; channel: string; handle: string | null; fps: number;
	durationInFrames: number; bg: string[]; items: {word: string; answer: string}[]; segments: Segment[];
};

const C = {
	ink: '#0b120e', white: '#ffffff', glass: 'rgba(8,18,14,0.48)', line: 'rgba(255,255,255,0.18)',
	accent: '#ffe27a', mint: '#8ff0c4', green: '#2fcf7a', greenDark: '#11663b',
};

const fontFaces = `
@font-face{font-family:Anton;src:url(${staticFile('fonts/Anton.woff2')}) format('woff2');}
@font-face{font-family:ArchivoBlack;src:url(${staticFile('fonts/ArchivoBlack.woff2')}) format('woff2');}
`;
const DISPLAY = 'Anton, "Arial Narrow", Impact, sans-serif';
const HEAVY = 'ArchivoBlack, "Arial Black", sans-serif';

const stroke = (px: number) => ({
	WebkitTextStroke: `${px}px ${C.ink}`, paintOrder: 'stroke fill' as const,
	textShadow: `0 ${px}px 0 ${C.ink}, 0 0 30px rgba(0,0,0,.45)`,
});

const FADE = 24;     // Frames Ueberblendung zwischen zwei Hintergruenden
const CLIP = 1200;   // Laenge der Hintergrund-Clips (40 s), danach von vorn

// Hintergrund: Clips nacheinander, weich ueberblendet, langsamer Zoom, Mitte etwas abgedunkelt fuer die Liste
const Background: React.FC<{bg: string[]; total: number}> = ({bg, total}) => {
	const frame = useCurrentFrame();
	const part = Math.ceil(total / Math.max(1, bg.length));
	return (
		<AbsoluteFill>
			{bg.map((src, i) => {
				const from = i * part;
				const op = i === 0 ? 1 : interpolate(frame, [from - FADE, from], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
				const zoom = interpolate(frame, [from - FADE, from + part], [1, 1.1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
				return (
					<Sequence key={src} from={Math.max(0, from - FADE)} durationInFrames={part + FADE}>
						<AbsoluteFill style={{opacity: op, transform: `scale(${zoom})`}}>
							<Loop durationInFrames={CLIP}>
								<OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
							</Loop>
						</AbsoluteFill>
					</Sequence>
				);
			})}
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.45) 0%, rgba(0,0,0,.15) 30%, rgba(0,0,0,.2) 70%, rgba(0,0,0,.55) 100%)'}} />
		</AbsoluteFill>
	);
};

const Header: React.FC<{title: string; sub: string; at: number}> = ({title, sub, at}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: frame - at, fps, config: {damping: 12, mass: 0.6}});
	return (
		<div style={{position: 'absolute', top: 190, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14}}>
			<div style={{fontFamily: DISPLAY, fontSize: Math.min(132, Math.floor(1500 / Math.max(1, title.length))), lineHeight: 1, whiteSpace: 'nowrap', color: C.white, letterSpacing: 2, transform: `scale(${0.7 + 0.3 * s})`, opacity: s, ...stroke(9)}}>{title}</div>
			<div style={{
				fontFamily: HEAVY, fontSize: 40, color: C.ink, background: C.accent, borderRadius: 40, padding: '10px 30px',
				transform: `scale(${s}) rotate(-2deg)`, boxShadow: '0 10px 30px rgba(0,0,0,.35)', whiteSpace: 'nowrap',
			}}>{sub}</div>
		</div>
	);
};

type RowState = {asked: number | null; timerFrom: number; timer: number; revealAt: number | null};

const ROW_H = 96;
const ROW_GAP = 12;

// Eine Zeile der Liste: Nummer, Stichwort, Timer als Fuellung, dann die Antwort
const Row: React.FC<{i: number; word: string; answer: string; st: RowState; active: boolean}> = ({i, word, answer, st, active}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const asked = st.asked !== null && frame >= st.asked;
	const revealed = st.revealAt !== null && frame >= st.revealAt;
	const pop = asked ? spring({frame: frame - st.asked!, fps, config: {damping: 10, mass: 0.5}}) : 0;
	const tt = frame - st.timerFrom;
	const timing = asked && !revealed && tt >= 0;
	const fill = timing ? interpolate(tt, [0, st.timer], [0, 1], {extrapolateRight: 'clamp'}) : 0;
	const secs = Math.max(1, Math.ceil((st.timer - tt) / fps));
	const rv = revealed ? spring({frame: frame - st.revealAt!, fps, config: {damping: 9, mass: 0.5}}) : 0;
	const greenIn = revealed ? interpolate(frame - st.revealAt!, [0, 6], [0, 1], {extrapolateRight: 'clamp'}) : 0;
	const wordSize = word.length > 12 ? 44 : 52;
	const ansSize = answer.length > 10 ? 38 : 46;
	return (
		<div style={{
			position: 'relative', height: ROW_H, borderRadius: 26, overflow: 'hidden', display: 'flex', alignItems: 'center',
			background: active ? 'rgba(255,255,255,0.16)' : 'rgba(255,255,255,0.06)',
			border: `3px solid ${active ? C.accent : C.line}`, transform: `scale(${active ? 1.04 : 1})`,
			boxShadow: active ? '0 12px 34px rgba(0,0,0,.35)' : 'none',
		}}>
			{/* Timer: Zeile fuellt sich von links */}
			<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${fill * 100}%`, background: 'rgba(255,226,122,0.28)'}} />
			<div style={{position: 'absolute', inset: 0, background: `linear-gradient(90deg, ${C.green} 0%, ${C.greenDark} 140%)`, opacity: greenIn * 0.55}} />
			<div style={{
				position: 'relative', width: 66, height: 66, marginLeft: 16, borderRadius: 33, flexShrink: 0,
				background: revealed ? C.green : asked ? C.accent : 'rgba(255,255,255,0.14)',
				display: 'flex', alignItems: 'center', justifyContent: 'center',
				fontFamily: HEAVY, fontSize: 36, color: asked ? C.ink : 'rgba(255,255,255,.7)',
			}}>{revealed ? '✓' : i + 1}</div>
			<div style={{
				position: 'relative', marginLeft: 24, fontFamily: HEAVY, fontSize: wordSize, color: C.white, whiteSpace: 'nowrap',
				transform: `scale(${asked ? 0.6 + 0.4 * pop : 1})`, transformOrigin: 'left center', opacity: asked ? 1 : 0.35,
				textShadow: '0 3px 12px rgba(0,0,0,.5)',
			}}>{asked ? word : '?'}</div>
			<div style={{flex: 1}} />
			{timing ? (
				<div style={{position: 'relative', marginRight: 26, fontFamily: DISPLAY, fontSize: 56, color: C.accent, ...stroke(5)}}>{secs}</div>
			) : null}
			{revealed ? (
				<div style={{
					position: 'relative', marginRight: 16, fontFamily: HEAVY, fontSize: ansSize, color: C.ink, background: C.white,
					borderRadius: 20, padding: '8px 22px', whiteSpace: 'nowrap', transform: `scale(${rv})`, transformOrigin: 'right center',
					boxShadow: '0 8px 20px rgba(0,0,0,.3)',
				}}>{answer}</div>
			) : null}
		</div>
	);
};

// Untertitel: immer 2-4 Woerter, aktives Wort hervorgehoben
const chunk = (words: Word[]) => {
	const out: Word[][] = [];
	let cur: Word[] = [];
	for (const w of words) {
		const len = cur.reduce((a, x) => a + x.w.length + 1, 0);
		if (cur.length && (cur.length >= 3 || len + w.w.length > 20)) {
			out.push(cur);
			cur = [];
		}
		cur.push(w);
	}
	if (cur.length) out.push(cur);
	return out;
};

const Subtitles: React.FC<{words: Word[]; at: number; until: number}> = ({words, at, until}) => {
	const frame = useCurrentFrame();
	const t = frame - at;
	if (t < 0 || frame >= until || !words.length) return null;
	const chunks = chunk(words);
	let idx = chunks.findIndex((c) => t < c[c.length - 1].e + 2);
	if (idx < 0) idx = chunks.length - 1;
	const c = chunks[idx];
	const pop = interpolate(t - c[0].s, [0, 4], [0.85, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<div style={{position: 'absolute', top: 1450, left: 50, right: 50, display: 'flex', justifyContent: 'center', flexWrap: 'wrap', gap: '0 22px', transform: `scale(${pop})`}}>
			{c.map((w, i) => {
				const on = t >= w.s && t < (c[i + 1]?.s ?? w.e + 6);
				return (
					<span key={i} style={{
						fontFamily: HEAVY, fontSize: 74, lineHeight: 1.15, color: on ? C.accent : C.white,
						textTransform: 'uppercase', ...stroke(10),
					}}>{w.w}</span>
				);
			})}
		</div>
	);
};

export const Quiz: React.FC<{timeline: QuizTimeline}> = ({timeline}) => {
	const frame = useCurrentFrame();
	const segs = timeline.segments;
	const starts: number[] = [];
	segs.reduce((acc, s) => (starts.push(acc), acc + s.duration), 0);
	// Zustand jeder Listenzeile aus den Fragen-Abschnitten
	const rows: RowState[] = timeline.items.map(() => ({asked: null, timerFrom: 0, timer: 0, revealAt: null}));
	segs.forEach((s, i) => {
		if (s.kind !== 'q') return;
		rows[s.n! - 1] = {asked: starts[i], timerFrom: starts[i] + s.speak, timer: s.timer!, revealAt: starts[i] + s.revealAt!};
	});
	const cur = Math.max(0, starts.findIndex((st, i) => frame >= st && frame < st + segs[i].duration));
	const curSeg = segs[cur];
	const outroIdx = segs.findIndex((s) => s.kind === 'outro');
	const inOutro = curSeg?.kind === 'outro';
	const intro = segs[0];
	const outro = segs[outroIdx];
	const listTop = 960 - (timeline.items.length * (ROW_H + ROW_GAP) - ROW_GAP) / 2 + 40;
	return (
		<AbsoluteFill style={{background: C.ink}}>
			<style>{fontFaces}</style>
			<Background bg={timeline.bg} total={timeline.durationInFrames} />
			{inOutro && outro
				? <Header title={outro.title ?? ''} sub={outro.sub ?? ''} at={starts[outroIdx]} />
				: <Header title={intro.title ?? ''} sub={intro.sub ?? ''} at={0} />}
			<div style={{
				position: 'absolute', top: listTop, left: 70, right: 70, display: 'flex', flexDirection: 'column', gap: ROW_GAP,
				padding: 0,
			}}>
				{timeline.items.map((it, i) => (
					<Row key={i} i={i} word={it.word} answer={it.answer} st={rows[i]} active={curSeg?.kind === 'q' && curSeg.n === i + 1} />
				))}
			</div>
			{segs.map((s, i) => (
				<React.Fragment key={i}>
					<Subtitles words={s.words} at={starts[i]} until={starts[i] + (s.kind === 'q' ? s.speak + 4 : s.duration)} />
					{s.answerWords ? <Subtitles words={s.answerWords} at={starts[i] + s.revealAt!} until={starts[i] + s.duration} /> : null}
					<Sequence from={starts[i]} durationInFrames={s.duration}>
						<Audio src={staticFile(s.audio)} />
						{s.kind === 'q' ? <>
							<Audio src={staticFile('sfx/whoosh.mp3')} volume={0.5} />
							{[0, 1, 2].map((k) => (
								<Sequence key={k} from={s.speak + k * 30}><Audio src={staticFile('sfx/tick.mp3')} volume={0.8} /></Sequence>
							))}
							<Sequence from={s.revealAt!}>
								<Audio src={staticFile('sfx/check.mp3')} volume={0.7} />
								<Audio src={staticFile(s.answerAudio!)} />
							</Sequence>
						</> : null}
					</Sequence>
				</React.Fragment>
			))}
		</AbsoluteFill>
	);
};
