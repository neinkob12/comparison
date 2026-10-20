import React from 'react';
import {
	AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, staticFile,
	useCurrentFrame, useVideoConfig,
} from 'remotion';

type Word = {w: string; s: number; e: number};
type Segment = {
	kind: 'intro' | 'q' | 'outro';
	audio: string; words: Word[]; speak: number; duration: number; bg: string; bgFrom: number;
	title?: string; sub?: string;
	n?: number; say?: string; answer?: string; timer?: number; revealAt?: number;
	answerAudio?: string; answerWords?: Word[];
};
export type QuizTimeline = {
	id: string; format: 'quiz'; channel: string; handle: string | null; fps: number;
	durationInFrames: number; music: string | null; items: {answer: string}[]; segments: Segment[];
};

// Bewusst ruhig: Weiss, ein warmer Sandton, sonst nur Schatten
const C = {
	ink: '#0a0d0c', white: '#ffffff', soft: 'rgba(255,255,255,0.72)', sand: '#efe2c4',
	strip: 'rgba(8,12,10,0.55)',
};

const fontFaces = `
@font-face{font-family:Anton;src:url(${staticFile('fonts/Anton.woff2')}) format('woff2');}
@font-face{font-family:ArchivoBlack;src:url(${staticFile('fonts/ArchivoBlack.woff2')}) format('woff2');}
`;
const DISPLAY = 'Anton, "Arial Narrow", Impact, sans-serif';
const HEAVY = 'ArchivoBlack, "Arial Black", sans-serif';

const shadow = (px: number) => ({
	WebkitTextStroke: `${px}px rgba(0,0,0,.85)`, paintOrder: 'stroke fill' as const,
	textShadow: '0 4px 18px rgba(0,0,0,.55)',
});

const ease = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

const FADE = 14; // Ueberblendung zwischen den Clips

// Jede Frage bekommt ihren eigenen Naturclip, weich ueberblendet, ganz langsamer Zoom
const Backgrounds: React.FC<{segs: Segment[]; starts: number[]}> = ({segs, starts}) => {
	const frame = useCurrentFrame();
	return (
		<AbsoluteFill>
			{segs.map((s, i) => {
				const from = starts[i];
				const op = i === 0 ? 1 : ease(frame, from - FADE, from);
				const zoom = 1 + 0.06 * ease(frame, from - FADE, from + s.duration);
				return (
					<Sequence key={i} from={Math.max(0, from - FADE)} durationInFrames={s.duration + FADE * 2}>
						<AbsoluteFill style={{opacity: op, transform: `scale(${zoom})`}}>
							<OffthreadVideo src={staticFile(s.bg)} startFrom={s.bgFrom} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
						</AbsoluteFill>
					</Sequence>
				);
			})}
			<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.35) 0%, rgba(0,0,0,.12) 35%, rgba(0,0,0,.12) 70%, rgba(0,0,0,.4) 100%)'}} />
		</AbsoluteFill>
	);
};

const Banner: React.FC = () => (
	<div style={{position: 'absolute', top: 175, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
		<div style={{
			fontFamily: HEAVY, fontSize: 44, letterSpacing: 3, color: C.white, background: C.strip, padding: '12px 30px',
			borderRadius: 14, textTransform: 'uppercase',
		}}>Allgemeinwissen Quiz</div>
	</div>
);

// Mitte oben: waehrend gesprochen wird ein Wort (Karaoke), in der Bedenkzeit die ganze Frage + duenner Timer
const TOP = 330;

const OneWord: React.FC<{words: Word[]; at: number; until: number; size?: number}> = ({words, at, until, size = 96}) => {
	const frame = useCurrentFrame();
	const t = frame - at;
	if (t < 0 || frame >= until || !words.length) return null;
	let i = words.findIndex((w, k) => t < (words[k + 1]?.s ?? Infinity));
	if (i < 0) i = words.length - 1;
	const w = words[i];
	const op = ease(t, w.s - 1, w.s + 2);
	return (
		<div style={{position: 'absolute', top: TOP, left: 40, right: 40, height: 220, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
			<div style={{
				fontFamily: HEAVY, fontSize: w.w.length > 12 ? size * 0.75 : size, color: C.white, textTransform: 'uppercase',
				opacity: 0.4 + 0.6 * op, transform: `scale(${0.94 + 0.06 * op})`, ...shadow(8),
			}}>{w.w}</div>
		</div>
	);
};

const Thinking: React.FC<{text: string; from: number; len: number}> = ({text, from, len}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame - from;
	if (t < 0 || t >= len) return null;
	const op = ease(t, 0, 6) * (1 - ease(t, len - 4, len));
	const left = 1 - t / len;
	const secs = Math.max(1, Math.ceil((len - t) / fps));
	return (
		<div style={{position: 'absolute', top: TOP, left: 70, right: 70, height: 220, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 26, opacity: op}}>
			<div style={{fontFamily: HEAVY, fontSize: 54, lineHeight: 1.18, color: C.white, textAlign: 'center', ...shadow(6)}}>{text}</div>
			<div style={{display: 'flex', alignItems: 'center', gap: 18}}>
				<div style={{width: 420, height: 10, borderRadius: 5, background: 'rgba(255,255,255,.22)', overflow: 'hidden'}}>
					<div style={{width: `${left * 100}%`, height: '100%', background: C.sand, borderRadius: 5}} />
				</div>
				<div style={{fontFamily: DISPLAY, fontSize: 40, color: C.sand, width: 30, ...shadow(4)}}>{secs}</div>
			</div>
		</div>
	);
};

const Hook: React.FC<{title: string; sub: string; until: number}> = ({title, sub, until}) => {
	const frame = useCurrentFrame();
	const op = ease(frame, 0, 8) * (1 - ease(frame, until - 8, until));
	return (
		<div style={{position: 'absolute', top: TOP, left: 60, right: 60, height: 220, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 16, opacity: op}}>
			<div style={{fontFamily: DISPLAY, fontSize: Math.min(120, Math.floor(1700 / Math.max(1, title.length))), lineHeight: 1.02, color: C.white, textAlign: 'center', textTransform: 'uppercase', ...shadow(7)}}>{title}</div>
			{sub ? <div style={{fontFamily: HEAVY, fontSize: 42, color: C.sand, textAlign: 'center', ...shadow(5)}}>{sub}</div> : null}
		</div>
	);
};

// Liste in der Mitte: schmaler dunkler Streifen mit 1. bis 8., Antworten erscheinen daneben
const ROW = 92;
const List: React.FC<{items: {answer: string}[]; revealAt: (number | null)[]; active: number}> = ({items, revealAt, active}) => {
	const frame = useCurrentFrame();
	const top = 600;
	return (
		<div style={{position: 'absolute', top, left: 110, right: 60}}>
			<div style={{position: 'absolute', left: 0, top: -14, width: 96, height: items.length * ROW + 28, borderRadius: 18, background: C.strip}} />
			{items.map((it, i) => {
				const at = revealAt[i];
				const shown = at !== null && frame >= at;
				const op = shown ? ease(frame, at!, at! + 8) : 0;
				const on = i === active;
				return (
					<div key={i} style={{position: 'relative', height: ROW, display: 'flex', alignItems: 'center'}}>
						<div style={{
							width: 96, textAlign: 'center', fontFamily: DISPLAY, fontSize: 62,
							color: on ? C.sand : shown ? C.white : C.soft,
						}}>{i + 1}.</div>
						<div style={{
							marginLeft: 26, fontFamily: HEAVY, fontSize: it.answer.length > 16 ? 46 : 56, color: C.white, whiteSpace: 'nowrap',
							textTransform: 'uppercase', opacity: op, transform: `translateX(${(1 - op) * -16}px)`, ...shadow(6),
						}}>{it.answer}</div>
					</div>
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
	const revealAt: (number | null)[] = timeline.items.map(() => null);
	segs.forEach((s, i) => {
		if (s.kind === 'q') revealAt[s.n! - 1] = starts[i] + s.revealAt! + 6;
	});
	const cur = Math.max(0, starts.findIndex((st, i) => frame >= st && frame < st + segs[i].duration));
	const curSeg = segs[cur];
	const total = timeline.durationInFrames;
	return (
		<AbsoluteFill style={{background: C.ink}}>
			<style>{fontFaces}</style>
			<Backgrounds segs={segs} starts={starts} />
			<Banner />
			<List items={timeline.items} revealAt={revealAt} active={curSeg?.kind === 'q' ? curSeg.n! - 1 : -1} />
			{segs.map((s, i) => {
				const st = starts[i];
				return (
					<React.Fragment key={i}>
						{s.kind === 'q' ? <>
							<OneWord words={s.words} at={st} until={st + s.speak} />
							<Thinking text={s.say!} from={st + s.speak} len={s.timer!} />
							<OneWord words={s.answerWords!} at={st + s.revealAt!} until={st + s.duration} size={104} />
						</> : <>
							<Sequence from={st} durationInFrames={s.duration}><Hook title={s.title ?? ''} sub={s.sub ?? ''} until={s.duration} /></Sequence>
						</>}
						<Sequence from={st} durationInFrames={s.duration}>
							<Audio src={staticFile(s.audio)} />
							{s.kind === 'q' ? <>
								{[0, 1, 2].map((k) => (
									<Sequence key={k} from={s.speak + k * 30}><Audio src={staticFile('sfx/tick.mp3')} volume={0.35} /></Sequence>
								))}
								<Sequence from={s.revealAt!}>
									<Audio src={staticFile('sfx/pop.mp3')} volume={0.4} />
									<Audio src={staticFile(s.answerAudio!)} />
								</Sequence>
							</> : null}
						</Sequence>
					</React.Fragment>
				);
			})}
			{timeline.music ? (
				<Audio src={staticFile(timeline.music)} loop
					volume={(f) => 0.32 * interpolate(f, [0, 15, total - 30, total], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
			) : null}
		</AbsoluteFill>
	);
};
