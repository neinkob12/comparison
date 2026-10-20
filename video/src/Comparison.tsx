import React from 'react';
import {
	AbsoluteFill, Audio, Img, Sequence, Series, interpolate, random, spring, staticFile,
	useCurrentFrame, useVideoConfig,
} from 'remotion';

type Side = {label: string; img: string | null; emoji?: string | null; fact?: string};
type Segment = {
	kind: 'intro' | 'q' | 'hook' | 'mid' | 'explain' | 'outro' | 'loop' | 'scene';
	audio: string; audioB?: string; bAt?: number; speak: number; gap?: number; hold: number; duration: number; voiceAt?: number;
	share?: string; winAudio?: string; aAt?: number; winAt?: number; best?: 'a' | 'b'; note?: string;
	statement?: string; stamps?: [string, string]; glitch?: number; glitchMode?: string;
	instant?: boolean; progress?: [number, number]; popup?: {text: string; at: 'start' | 'reveal'};
	scene?: any; step?: [number, number]; header?: string;
	title?: string; sub?: string; a?: Side; b?: Side; pct?: [number, number];
};
export type Timeline = {
	id: string; channel: string; handle: string | null; fps: number; noFollow?: boolean;
	durationInFrames: number; segments: Segment[];
};

const C = {
	red: '#e3263b', redDark: '#7a0f1c', blue: '#2350e6', blueDark: '#0e2470',
	yellow: '#ffd23f', mint: '#19b8a6', green: '#16c45f', greenDark: '#06612c',
	ink: '#0d0c12', white: '#ffffff',
};

const fontFaces = `
@font-face{font-family:Anton;src:url(${staticFile('fonts/Anton.woff2')}) format('woff2');}
@font-face{font-family:ArchivoBlack;src:url(${staticFile('fonts/ArchivoBlack.woff2')}) format('woff2');}
`;
const DISPLAY = 'Anton, "Arial Narrow", Impact, sans-serif';
const HEAVY = 'ArchivoBlack, "Arial Black", sans-serif';
const EMOJI = '"Noto Color Emoji", "Apple Color Emoji", sans-serif';

const stroke = (px: number) => ({
	WebkitTextStroke: `${px}px ${C.ink}`, paintOrder: 'stroke fill' as const,
	textShadow: `0 ${px}px 0 ${C.ink}`,
});

const COUNT = 90; // 3-2-1 in Frames

const Half: React.FC<{side: Side; top: boolean; pct: number; win: boolean; revealAt: number; mid: boolean; enterAt: number; compact?: boolean}> = ({side, top, pct, win, revealAt, mid, enterAt, compact}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	// Reinfliegen: oben von links, unten von rechts, mit Bewegungsunschaerfe
	const fly = enterAt < 0 ? 1 : spring({frame: frame - enterAt, fps, config: {damping: 16, stiffness: 260, mass: 0.6}});
	const flyX = (1 - fly) * (top ? -1150 : 1150);
	const blur = Math.min(18, Math.abs(flyX) / 40);
	const enter = 1;
	const rev = spring({frame: frame - revealAt, fps, config: {damping: 9, mass: 0.7}});
	const shown = frame >= revealAt;
	const count = Math.round(interpolate(frame - revealAt, [0, 14], [0, pct], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
	const base = mid ? (top ? C.yellow : C.mint) : top ? C.red : C.blue;
	const dark = mid ? '#3a2a00' : top ? C.redDark : C.blueDark;
	const t = (frame - revealAt);
	const greenIn = shown && win ? interpolate(t, [0, 6], [0, 1], {extrapolateRight: 'clamp'}) : 0;
	const flash = shown && win ? interpolate(t, [0, 3, 12], [0, 0.55, 0], {extrapolateRight: 'clamp'}) : 0;
	const dim = shown && !win ? interpolate(t, [0, 8], [0, 0.5], {extrapolateRight: 'clamp'}) : 0;
	const pulse = shown && win ? 1 + 0.035 * Math.sin(t / 4) : 1;
	const lose = shown && !win ? interpolate(t, [0, 8], [0, 1], {extrapolateRight: 'clamp'}) : 0;
	const loseScale = 1 - 0.15 * lose;
	const crown = spring({frame: frame - revealAt - 4, fps, config: {damping: 8, mass: 0.6}});
	const visual = side.img ? (
		<Img src={staticFile(side.img)} style={{
			width: 470, height: 470, objectFit: 'cover', borderRadius: 36,
			border: `${greenIn > 0.5 ? 16 : 10}px solid ${greenIn > 0.5 ? C.green : C.white}`, boxShadow: greenIn > 0.5 ? `0 0 90px 20px ${C.green}` : '0 24px 60px rgba(0,0,0,.45)',
			filter: lose > 0 ? `grayscale(${lose}) brightness(${1 - 0.45 * lose})` : 'none',
		}} />
	) : side.emoji ? (
		<div style={{
			width: compact ? 270 : 420, height: compact ? 270 : 420, borderRadius: 210, background: C.white, border: `10px solid ${greenIn > 0.5 ? C.green : C.ink}`,
			display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EMOJI, fontSize: compact ? 160 : 250, lineHeight: 1,
			boxShadow: '0 24px 60px rgba(0,0,0,.35)',
		}}>{side.emoji}</div>
	) : <div style={{width: 500, height: 500}} />;
	return (
		<div style={{
			position: 'absolute', left: 0, right: 0, height: 960, top: top ? 0 : 960, overflow: 'hidden',
			background: `radial-gradient(circle at 50% ${top ? 60 : 40}%, ${base} 0%, ${dark} 120%)`,
		}}>
			<AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.green} 0%, ${C.greenDark} 120%)`, opacity: greenIn}} />
			<div style={{
				position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center',
				justifyContent: top ? 'flex-end' : 'flex-start', paddingTop: top ? 0 : 150, paddingBottom: top ? 150 : 0, gap: 30,
				transform: `translateX(${flyX}px) skewX(${(top ? 1 : -1) * blur * 0.6}deg)`, filter: blur > 0.5 ? `blur(${blur}px)` : 'none',
				opacity: enterAt >= 0 && frame < enterAt ? 0 : 1,
			}}>
				{top ? null : <Label text={side.label} enter={enter} state={shown ? (win ? 'win' : 'lose') : null} />}
				<div style={{position: 'relative', transform: `scale(${(0.6 + 0.4 * enter) * pulse * loseScale})`}}>
					{visual}
					{shown && win ? (
						<div style={{position: 'absolute', top: -85, right: -85, fontFamily: EMOJI, fontSize: 150, lineHeight: 1,
							transform: `scale(${crown}) rotate(${22 + 6 * Math.sin(t / 5)}deg)`}}>👑</div>
					) : null}
					{shown && !win ? (
						<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
							fontFamily: HEAVY, fontSize: 380, color: 'rgba(255,40,60,.55)', lineHeight: 1}}>✕</div>
					) : null}
					{shown ? (
						<div style={{
							position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
							fontFamily: DISPLAY, fontSize: 230, color: C.white, transform: `scale(${rev})`, ...stroke(12),
						}}>{count}%</div>
					) : null}
				</div>
				{top ? <Label text={side.label} enter={enter} state={shown ? (win ? 'win' : 'lose') : null} /> : null}
			</div>
			{shown && win ? <Confetti t={t} seed={top ? 'a' : 'b'} /> : null}
			<AbsoluteFill style={{background: '#000', opacity: dim}} />
			<AbsoluteFill style={{background: C.white, opacity: flash}} />
		</div>
	);
};

const Confetti: React.FC<{t: number; seed: string}> = ({t, seed}) => {
	const cols = [C.yellow, C.white, '#7CFFB2', '#ff4fd8', '#4fd8ff'];
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{new Array(46).fill(0).map((_, i) => {
				const ang = random(seed + 'a' + i) * Math.PI * 2;
				const sp = 18 + random(seed + 's' + i) * 30;
				const x = 540 + Math.cos(ang) * sp * t;
				const y = 480 + Math.sin(ang) * sp * t + 0.9 * t * t;
				const size = 14 + random(seed + 'z' + i) * 18;
				const op = interpolate(t, [0, 30, 45], [1, 1, 0], {extrapolateRight: 'clamp'});
				return <div key={i} style={{position: 'absolute', left: x, top: y, width: size, height: size * 0.6,
					background: cols[i % cols.length], opacity: op, transform: `rotate(${t * 20 + i * 30}deg)`, borderRadius: 3}} />;
			})}
		</AbsoluteFill>
	);
};

const Label: React.FC<{text: string; enter: number; state: 'win' | 'lose' | null}> = ({text, enter, state}) => (
	<div style={{
		fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.02, color: state === 'win' ? C.yellow : C.white, textAlign: 'center',
		textTransform: 'uppercase', maxWidth: 940, opacity: state === 'lose' ? 0.55 * enter : enter,
		transform: `translateY(${(1 - enter) * 40}px) scale(${state === 'win' ? 1.12 : state === 'lose' ? 0.88 : 1})`,
		...stroke(8),
	}}>{text}</div>
);

// Mitte: ODER waehrend der Frage, dann 3-2-1, dann weg
const Center: React.FC<{speakEnd: number; count: number}> = ({speakEnd, count}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	if (frame < speakEnd) {
		const s = spring({frame: frame - 6, fps, config: {damping: 10}});
		return (
			<div style={{
				position: 'absolute', left: 540 - 120, top: 960 - 70, width: 240, height: 140, borderRadius: 70,
				background: C.white, border: `8px solid ${C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
				fontFamily: HEAVY, fontSize: 64, color: C.ink, transform: `scale(${s}) rotate(-4deg)`,
			}}>ODER</div>
		);
	}
	const t = frame - speakEnd;
	if (t >= count) return null;
	const n = Math.ceil((count - t) / 30);
	const local = t % 30;
	const s = spring({frame: local, fps, config: {damping: 8, mass: 0.5}});
	const ring = interpolate(t, [0, count], [1, 0]);
	return (
		<div style={{position: 'absolute', left: 540 - 130, top: 960 - 130, width: 260, height: 260}}>
			<svg width={260} height={260} style={{position: 'absolute', inset: 0}}>
				<circle cx={130} cy={130} r={118} fill={C.white} stroke={C.ink} strokeWidth={10} />
				<circle cx={130} cy={130} r={100} fill="none" stroke={C.red} strokeWidth={16}
					strokeDasharray={2 * Math.PI * 100} strokeDashoffset={2 * Math.PI * 100 * (1 - ring)}
					transform="rotate(-90 130 130)" strokeLinecap="round" />
			</svg>
			<div style={{
				position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
				fontFamily: DISPLAY, fontSize: 150, color: n === 1 ? C.red : C.ink, transform: `scale(${0.4 + 0.6 * s + (n === 1 ? 0.08 * Math.sin(local) : 0)})`,
			}}>{n}</div>
		</div>
	);
};

const Question: React.FC<{s: Segment}> = ({s}) => {
	const revealAt = s.speak + (s.gap ?? 0);
	const bAt = s.bAt ?? 4;
	const [pa, pb] = s.pct!;
	const mid = s.kind === 'mid';
	const frame = useCurrentFrame();
	const punch = s.instant ? 1 : interpolate(frame, [0, 7], [1.12, 1], {extrapolateRight: 'clamp'});
	const rt = frame - revealAt;
	const shake = rt >= 0 && rt < 10 ? Math.sin(rt * 2.6) * (10 - rt) * 2.5 : 0;
	const ct = frame - s.speak;
	const count = s.gap ?? COUNT;
	const panic = ct >= count - 30 && ct < count ? 0.25 * (0.5 + 0.5 * Math.sin(ct * 1.2)) : 0;
	return (
		<AbsoluteFill style={{transform: `scale(${punch}) translate(${shake}px, ${-shake * 0.5}px)`}}>
			<Half side={s.a!} top pct={pa} win={pa >= pb} revealAt={revealAt} mid={mid} enterAt={s.instant ? -1 : 0} compact={!!s.statement} />
			<Half side={s.b!} top={false} pct={pb} win={pb > pa} revealAt={revealAt} mid={mid} enterAt={s.instant ? -1 : bAt} compact={!!s.statement} />
			{s.progress ? <Progress n={s.progress[0]} total={s.progress[1]} /> : null}
			{s.popup ? <Popup text={s.popup.text} from={s.popup.at === 'reveal' ? revealAt + 6 : 4} until={s.popup.at === 'reveal' ? s.duration : 4 + 80} /> : null}
			{s.statement ? <Statement text={s.statement} /> : null}
			<Center speakEnd={s.speak} count={count} />
			<AbsoluteFill style={{boxShadow: `inset 0 0 220px 60px rgba(255,0,0,${panic})`, pointerEvents: 'none'}} />
			<Audio src={staticFile(s.audio)} />
			{s.audioB ? <Sequence from={bAt}><Audio src={staticFile(s.audioB)} /></Sequence> : null}
			{s.instant ? null : <Audio src={staticFile('sfx/whoosh.mp3')} volume={0.7} />}
			{s.instant ? null : <Sequence from={bAt}><Audio src={staticFile('sfx/whoosh.mp3')} volume={0.7} /></Sequence>}
			<Sequence from={s.speak} durationInFrames={count}><Audio src={staticFile('sfx/countdown.mp3')} startFrom={Math.max(0, COUNT - count)} volume={0.9} /></Sequence>
			<Sequence from={revealAt}><Audio src={staticFile('sfx/check.mp3')} volume={0.8} /></Sequence>
			{s.winAudio ? <Sequence from={revealAt + 12}><Audio src={staticFile(s.winAudio)} /></Sequence> : null}
		</AbsoluteFill>
	);
};

// Fortschritt oben: FRAGE 3/8 + Balken (offene Schleife bis zum Ende)
const Progress: React.FC<{n: number; total: number}> = ({n, total}) => (
	<div style={{position: 'absolute', top: 64, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
		<div style={{fontFamily: HEAVY, fontSize: 38, color: C.white, ...stroke(5)}}>FRAGE {n}/{total}</div>
		<div style={{display: 'flex', gap: 8}}>
			{new Array(total).fill(0).map((_, i) => (
				<div key={i} style={{width: 64, height: 14, borderRadius: 7, border: `3px solid ${C.ink}`,
					background: i < n ? C.yellow : 'rgba(255,255,255,.35)'}} />
			))}
		</div>
	</div>
);

// Pop-up-Sticker (Teaser oder Markier-Aufruf)
const Popup: React.FC<{text: string; from: number; until: number}> = ({text, from, until}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	if (frame < from || frame >= until) return null;
	const s = spring({frame: frame - from, fps, config: {damping: 8, mass: 0.6}});
	const wob = Math.sin((frame - from) / 4) * 2;
	return (
		<div style={{position: 'absolute', top: 960, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: 'translateY(-50%)'}}>
			<div style={{
				fontFamily: HEAVY, fontSize: 46, lineHeight: 1.15, color: C.ink, background: C.yellow, border: `8px solid ${C.ink}`,
				borderRadius: 26, padding: '18px 34px', textAlign: 'center', maxWidth: 900, boxShadow: '0 16px 40px rgba(0,0,0,.45)',
				transform: `scale(${s}) rotate(${-4 + wob}deg)`,
			}}>{text}</div>
			<Sequence from={from} layout="none"><Audio src={staticFile('sfx/pop.mp3')} volume={0.8} /></Sequence>
		</div>
	);
};

// Loop-Ende: leere Farbflaechen wie bei Frage 1, kurzer Satz fuehrt zurueck an den Anfang
const Loop: React.FC<{s: Segment}> = ({s}) => (
	<AbsoluteFill>
		<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 960, background: `radial-gradient(circle at 50% 60%, ${C.red} 0%, ${C.redDark} 120%)`}} />
		<div style={{position: 'absolute', left: 0, right: 0, top: 960, height: 960, background: `radial-gradient(circle at 50% 40%, ${C.blue} 0%, ${C.blueDark} 120%)`}} />
		<Audio src={staticFile(s.audio)} />
	</AbsoluteFill>
);

// ---------- Erklaervideos: Szenen mit einfachen Animationen ----------
const eur = (v: number, d = 0) => v.toLocaleString('de-DE', {minimumFractionDigits: d, maximumFractionDigits: d}) + ' €';
const ease = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 3)});
const COL: Record<string, string> = {red: C.red, green: C.green, blue: C.blue, yellow: C.yellow, white: C.white, mint: C.mint};

const SceneHeader: React.FC<{text?: string; step?: [number, number]}> = ({text, step}) => (
	<div style={{position: 'absolute', top: 70, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14}}>
		{text ? <div style={{fontFamily: HEAVY, fontSize: 36, color: C.yellow, letterSpacing: 2}}>{text}</div> : null}
		{step ? (
			<div style={{display: 'flex', gap: 10}}>
				{new Array(step[1]).fill(0).map((_, i) => (
					<div key={i} style={{width: 54, height: 12, borderRadius: 6, background: i < step[0] ? C.yellow : 'rgba(255,255,255,.22)'}} />
				))}
			</div>
		) : null}
	</div>
);

const Title: React.FC<{text: string; top?: number}> = ({text, top = 250}) => {
	const frame = useCurrentFrame();
	const k = ease(frame, 0, 10);
	return (
		<div style={{position: 'absolute', top, left: 60, right: 60, textAlign: 'center', fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.04,
			color: C.white, textTransform: 'uppercase', opacity: k, transform: `translateY(${(1 - k) * 30}px)`}}>{text}</div>
	);
};

const Counter: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const start = Math.round(speak * (d.startFrac ?? 0.4));
	const v = interpolate(frame, [start, start + 36], [d.from ?? 0, d.value], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 3)});
	const pop = spring({frame: frame - start - 36, fps: 30, config: {damping: 8, mass: 0.6}});
	const k = ease(frame, start - 6, start);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 36, padding: 60}}>
			{d.emoji ? <div style={{fontFamily: EMOJI, fontSize: 170, lineHeight: 1}}>{d.emoji}</div> : null}
			<div style={{fontFamily: HEAVY, fontSize: 56, color: C.white, textAlign: 'center'}}>{d.kicker}</div>
			<div style={{fontFamily: DISPLAY, fontSize: 230, lineHeight: 1, color: COL[d.color ?? 'yellow'], opacity: k,
				transform: `scale(${1 + 0.08 * pop * (frame > start + 36 ? 1 : 0)})`, ...stroke(10)}}>{eur(v, d.decimals ?? 0)}</div>
			<div style={{fontFamily: HEAVY, fontSize: 52, color: C.white, textAlign: 'center', opacity: k}}>{d.caption}</div>
			{d.sub ? <div style={{fontFamily: HEAVY, fontSize: 36, color: 'rgba(255,255,255,.7)', textAlign: 'center', maxWidth: 900, opacity: ease(frame, start + 40, start + 50)}}>{d.sub}</div> : null}
		</AbsoluteFill>
	);
};

const Guess: React.FC<{d: any; speak: number; gap: number}> = ({d, speak, gap}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame, fps, config: {damping: 10}});
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 40}}>
			<div style={{width: 420, height: 420, borderRadius: 210, background: C.white, border: `10px solid ${C.ink}`, display: 'flex',
				alignItems: 'center', justifyContent: 'center', fontFamily: EMOJI, fontSize: 250, transform: `scale(${s})`}}>{d.emoji}</div>
			<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.02, color: C.white, textAlign: 'center', textTransform: 'uppercase', padding: '0 60px', ...stroke(8)}}>{d.title}</div>
			<div style={{fontFamily: HEAVY, fontSize: 58, color: C.ink, background: C.yellow, padding: '14px 34px', borderRadius: 20}}>{d.sub}</div>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 260, height: 260}}>
				<div style={{position: 'relative', left: 0, top: -960 + 130}}><Center speakEnd={speak} count={gap} /></div>
			</div>
			<Sequence from={speak} durationInFrames={gap}><Audio src={staticFile('sfx/countdown.mp3')} startFrom={Math.max(0, COUNT - gap)} volume={0.9} /></Sequence>
		</AbsoluteFill>
	);
};

const Checklist: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const n = d.items.length;
	return (
		<AbsoluteFill>
			<Title text={d.title} />
			<div style={{position: 'absolute', top: 560, left: 90, right: 90, display: 'flex', flexDirection: 'column', gap: 46}}>
				{d.items.map((it: any, i: number) => {
					const at = Math.round(speak * (0.22 + 0.7 * i / n));
					const k = spring({frame: frame - at, fps, config: {damping: 11, mass: 0.6}});
					return (
						<div key={i} style={{display: 'flex', alignItems: 'center', gap: 34, opacity: frame < at ? 0.15 : 1, transform: `translateX(${(1 - k) * -60}px)`}}>
							<div style={{width: 120, height: 120, borderRadius: 30, background: frame < at ? 'rgba(255,255,255,.15)' : C.green, display: 'flex',
								alignItems: 'center', justifyContent: 'center', fontFamily: HEAVY, fontSize: 80, color: C.white, transform: `scale(${0.6 + 0.4 * k})`}}>✓</div>
							<div style={{fontFamily: EMOJI, fontSize: 84}}>{it.emoji}</div>
							<div style={{fontFamily: HEAVY, fontSize: 60, color: C.white}}>{it.text}</div>
							<Sequence from={at} layout="none"><Audio src={staticFile('sfx/check.mp3')} volume={0.5} /></Sequence>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

const Split: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const total = d.parts.reduce((a: number, p: any) => a + p.value, 0);
	const at = Math.round(speak * (d.splitFrac ?? 0.45));
	const k = ease(frame, at, at + 24);
	return (
		<AbsoluteFill>
			<Title text={d.title} />
			<div style={{position: 'absolute', top: 520, left: 0, right: 0, textAlign: 'center', fontFamily: DISPLAY, fontSize: 170, color: C.yellow, ...stroke(8)}}>{d.big}</div>
			<div style={{position: 'absolute', top: 730, left: 0, right: 0, textAlign: 'center', fontFamily: HEAVY, fontSize: 44, color: C.white}}>{d.caption}</div>
			<div style={{position: 'absolute', top: 880, left: 90, right: 90, height: 150, borderRadius: 30, overflow: 'hidden', display: 'flex', border: `8px solid ${C.ink}`, background: 'rgba(255,255,255,.15)'}}>
				{d.parts.map((p: any, i: number) => (
					<div key={i} style={{width: `${(100 * p.value / total) * (i === 0 ? k : 1)}%`, background: COL[p.color], transition: 'none',
						opacity: i === 0 ? 1 : k}} />
				))}
			</div>
			<div style={{position: 'absolute', top: 1080, left: 90, right: 90, display: 'flex', flexDirection: 'column', gap: 26, opacity: k}}>
				{d.parts.map((p: any, i: number) => (
					<div key={i} style={{display: 'flex', alignItems: 'center', gap: 24}}>
						<div style={{width: 56, height: 56, borderRadius: 14, background: COL[p.color]}} />
						<div style={{fontFamily: HEAVY, fontSize: 56, color: C.white, flex: 1}}>{p.label}</div>
						<div style={{fontFamily: DISPLAY, fontSize: 80, color: COL[p.color]}}>{eur(p.value, 2)}</div>
					</div>
				))}
			</div>
		</AbsoluteFill>
	);
};

const Amort: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const r = Math.pow(1 + d.eff, 1 / 12) - 1;
	const A = d.P * r / (1 - Math.pow(1 + r, -d.n));
	let b = d.P;
	const rows = new Array(d.n).fill(0).map(() => {const i = b * r; b -= A - i; return i;});
	const shown = Math.round(interpolate(frame, [10, speak * 0.75], [0, Number(d.n)], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
	const W = 900, H = 640, bw = W / d.n;
	return (
		<AbsoluteFill>
			<Title text={d.title} />
			<div style={{position: 'absolute', top: 560, left: 90, width: W, height: H}}>
				{rows.map((i, m) => m < shown ? (
					<div key={m} style={{position: 'absolute', left: m * bw + 1, bottom: 0, width: bw - 3, height: H, display: 'flex', flexDirection: 'column'}}>
						<div style={{height: `${100 * i / A}%`, background: C.red}} />
						<div style={{flex: 1, background: C.green}} />
					</div>
				) : null)}
				<div style={{position: 'absolute', left: 0, right: 0, top: H + 18, display: 'flex', justifyContent: 'space-between', fontFamily: HEAVY, fontSize: 34, color: 'rgba(255,255,255,.8)'}}>
					<span>Monat 1</span><span>Monat {d.n}</span>
				</div>
			</div>
			<div style={{position: 'absolute', top: 1320, left: 90, right: 90, display: 'flex', flexDirection: 'column', gap: 18}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 20}}><div style={{width: 48, height: 48, borderRadius: 12, background: C.red}} /><div style={{fontFamily: HEAVY, fontSize: 48, color: C.white}}>Zinsen: {eur(rows[0], 2)} → {eur(rows[d.n - 1], 2)}</div></div>
				<div style={{display: 'flex', alignItems: 'center', gap: 20}}><div style={{width: 48, height: 48, borderRadius: 12, background: C.green}} /><div style={{fontFamily: HEAVY, fontSize: 48, color: C.white}}>Tilgung: {eur(A - rows[0], 2)} → {eur(A - rows[d.n - 1], 2)}</div></div>
			</div>
		</AbsoluteFill>
	);
};

const Cards: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill>
			<Title text={d.title} />
			<div style={{position: 'absolute', top: 540, left: 70, right: 70, display: 'flex', flexDirection: 'column', gap: 44}}>
				{d.cards.map((c: any, i: number) => {
					const at = Math.round(speak * (0.12 + 0.45 * i));
					const k = spring({frame: frame - at, fps, config: {damping: 12, mass: 0.6}});
					return (
						<div key={i} style={{background: c.good ? C.green : 'rgba(255,255,255,.12)', border: `8px solid ${c.good ? C.yellow : 'rgba(255,255,255,.3)'}`, borderRadius: 34,
							padding: '34px 40px', opacity: frame < at ? 0 : 1, transform: `scale(${0.85 + 0.15 * k})`}}>
							<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
								<div style={{fontFamily: HEAVY, fontSize: 52, color: C.white, flex: 1, paddingRight: 20}}>{c.head}</div>
								<div style={{fontFamily: DISPLAY, fontSize: 110, color: c.good ? C.yellow : C.white, whiteSpace: 'nowrap', ...stroke(6)}}>{c.value}</div>
							</div>
							<div style={{fontFamily: HEAVY, fontSize: 40, lineHeight: 1.25, color: 'rgba(255,255,255,.9)', marginTop: 10}}>{c.text}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

const Bars: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const max = Math.max(...d.items.map((it: any) => it.value));
	const base = d.base ?? 0;
	return (
		<AbsoluteFill>
			<Title text={d.title} />
			<div style={{position: 'absolute', top: 560, left: 80, right: 80, display: 'flex', flexDirection: 'column', gap: 54}}>
				{d.items.map((it: any, i: number) => {
					const at = Math.round(speak * (0.1 + 0.75 * i / d.items.length));
					const k = ease(frame, at, at + 22);
					const w = (it.value - base) / (max - base);
					return (
						<div key={i} style={{opacity: frame < at ? 0 : 1}}>
							<div style={{fontFamily: HEAVY, fontSize: 46, color: C.white, marginBottom: 12}}>{it.label}</div>
							<div style={{display: 'flex', alignItems: 'center', gap: 24}}>
								<div style={{height: 96, width: `${Math.max(8, 72 * w * k)}%`, borderRadius: 20, background: COL[it.color ?? (it.highlight ? 'yellow' : 'white')],
									border: `6px solid ${C.ink}`}} />
								<div style={{fontFamily: DISPLAY, fontSize: 78, color: it.highlight ? C.yellow : C.white, ...stroke(5)}}>{eur(Math.round(it.value * k))}</div>
							</div>
						</div>
					);
				})}
			</div>
			{d.note ? <div style={{position: 'absolute', bottom: 210, left: 80, right: 80, textAlign: 'center', fontFamily: HEAVY, fontSize: 32, color: 'rgba(255,255,255,.65)'}}>{d.note}</div> : null}
		</AbsoluteFill>
	);
};

const Stats: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill>
			<Title text={d.title} />
			<div style={{position: 'absolute', top: 600, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 70}}>
				{d.items.map((it: any, i: number) => {
					const at = Math.round(speak * (0.2 + 0.45 * i));
					const k = spring({frame: frame - at, fps, config: {damping: 8, mass: 0.6}});
					return (
						<div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', opacity: frame < at ? 0 : 1, transform: `scale(${k})`}}>
							<div style={{fontFamily: DISPLAY, fontSize: 220, lineHeight: 1, color: COL[it.color ?? 'yellow'], ...stroke(10)}}>{it.value}</div>
							<div style={{fontFamily: HEAVY, fontSize: 54, color: C.white}}>{it.label}</div>
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

const End: React.FC<{d: any; speak: number}> = ({d, speak}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const k = spring({frame: frame - 4, fps, config: {damping: 9}});
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', gap: 40, padding: 70}}>
			<div style={{fontFamily: HEAVY, fontSize: 58, color: C.white, textAlign: 'center'}}>{d.kicker}</div>
			<div style={{fontFamily: DISPLAY, fontSize: 210, lineHeight: 1, color: C.yellow, transform: `scale(${k})`, ...stroke(10)}}>{d.big}</div>
			<div style={{fontFamily: HEAVY, fontSize: 52, color: C.white, textAlign: 'center'}}>{d.caption}</div>
			{d.cta ? <div style={{fontFamily: HEAVY, fontSize: 50, color: C.ink, background: C.yellow, padding: '16px 34px', borderRadius: 20,
				opacity: ease(frame, speak * 0.5, speak * 0.5 + 8)}}>{d.cta}</div> : null}
			{d.note ? <div style={{position: 'absolute', bottom: 190, left: 70, right: 70, textAlign: 'center', fontFamily: HEAVY, fontSize: 30, lineHeight: 1.3, color: 'rgba(255,255,255,.65)'}}>{d.note}</div> : null}
		</AbsoluteFill>
	);
};

const Scene: React.FC<{s: Segment}> = ({s}) => {
	const d = s.scene;
	const body = d.type === 'counter' ? <Counter d={d} speak={s.speak} />
		: d.type === 'guess' ? <Guess d={d} speak={s.speak} gap={s.gap ?? 60} />
		: d.type === 'checklist' ? <Checklist d={d} speak={s.speak} />
		: d.type === 'split' ? <Split d={d} speak={s.speak} />
		: d.type === 'amort' ? <Amort d={d} speak={s.speak} />
		: d.type === 'cards' ? <Cards d={d} speak={s.speak} />
		: d.type === 'bars' ? <Bars d={d} speak={s.speak} />
		: d.type === 'stats' ? <Stats d={d} speak={s.speak} />
		: <End d={d} speak={s.speak} />;
	return (
		<AbsoluteFill style={{background: `radial-gradient(circle at 50% 35%, #26304f 0%, ${C.ink} 75%)`}}>
			{body}
			<SceneHeader text={s.header} step={s.step} />
			<Audio src={staticFile(s.audio)} />
		</AbsoluteFill>
	);
};

// Aussage oben (Mythos oder Fakt)
const Statement: React.FC<{text: string}> = ({text}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: frame - 2, fps, config: {damping: 12, mass: 0.6}});
	return (
		<div style={{position: 'absolute', top: 190, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
			<div style={{
				fontFamily: HEAVY, fontSize: 50, lineHeight: 1.18, color: C.ink, background: C.white, borderRadius: 28, border: `8px solid ${C.ink}`,
				padding: '24px 36px', textAlign: 'center', maxWidth: 940, boxShadow: '0 18px 44px rgba(0,0,0,.4)',
				transform: `scale(${s}) rotate(-1.5deg)`,
			}}>„{text}“</div>
		</div>
	);
};

// Intro: RAPPER fliegt von links rein, DUELL von rechts, beide rasten mit Impact ein
const Intro: React.FC<{s: Segment}> = ({s}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const a = spring({frame, fps, config: {damping: 13, stiffness: 260, mass: 0.6}});
	const b = spring({frame: frame - 7, fps, config: {damping: 13, stiffness: 260, mass: 0.6}});
	const shake = (start: number) => {
		const t = frame - start;
		return t >= 0 && t < 8 ? Math.sin(t * 2.4) * (8 - t) * 2.2 : 0;
	};
	const g = s.glitch && frame < s.glitch ? 1 : 0;
	const r = (k: string) => random(`${k}${frame}`);
	const gx = g ? (r('x') - 0.5) * 90 : 0;
	const gy = g ? (r('y') - 0.5) * 50 : 0;
	const sx = shake(7) + shake(14) + gx;
	const flash = interpolate(frame, [14, 16, 24], [0, 0.6, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const fit = (t?: string) => Math.min(290, Math.floor(1900 / Math.max(1, (t ?? '').length)));
	return (
		<AbsoluteFill style={{
			background: `linear-gradient(180deg, ${C.red} 0%, ${C.red} 50%, ${C.blue} 50%, ${C.blue} 100%)`,
			alignItems: 'center', justifyContent: 'center', transform: `translate(${sx}px, ${sx * 0.6 + gy}px) scale(1.06) skewX(${g ? (r('k') - 0.5) * 14 : 0}deg)`,
			filter: g ? `hue-rotate(${Math.floor(r('h') * 360)}deg) ${r('i') > 0.8 ? 'invert(1)' : ''} contrast(1.4)` : 'none',
		}}>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0, transform: 'rotate(-4deg)'}}>
				<div style={{
					fontFamily: DISPLAY, fontSize: fit(s.title), lineHeight: 0.95, color: C.white, whiteSpace: 'nowrap',
					transform: `translateX(${(1 - a) * -1300}px)`, ...stroke(14),
				}}>{s.title}</div>
				<div style={{
					fontFamily: DISPLAY, fontSize: fit(s.sub), lineHeight: 0.95, color: C.yellow, whiteSpace: 'nowrap',
					transform: `translateX(${(1 - b) * 1300}px)`, ...stroke(14),
				}}>{s.sub}</div>
			</div>
			<AbsoluteFill style={{background: C.white, opacity: flash}} />
			{g ? <Glitch frame={frame} /> : null}
			<Sequence from={0}><Audio src={staticFile('sfx/whoosh.mp3')} volume={0.7} /></Sequence>
			<Sequence from={7}><Audio src={staticFile('sfx/impact.mp3')} volume={0.9} /></Sequence>
			<Sequence from={7}><Audio src={staticFile('sfx/whoosh.mp3')} volume={0.6} /></Sequence>
			<Sequence from={14}><Audio src={staticFile('sfx/impact.mp3')} volume={1} /></Sequence>
			<Sequence from={s.voiceAt ?? 0}><Audio src={staticFile(s.audio)} volume={1} /></Sequence>
		</AbsoluteFill>
	);
};

// Aufloesung: beide Optionen mit Fakt, dann wird die bessere gruen gestempelt
const ExplainHalf: React.FC<{side: Side; top: boolean; factAt: number; winAt: number; best: boolean; stamps: [string, string]}> = ({side, top, factAt, winAt, best, stamps}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const f = spring({frame: frame - factAt, fps, config: {damping: 12, mass: 0.6}});
	const w = frame - winAt;
	const decided = w >= 0;
	const greenIn = decided && best ? interpolate(w, [0, 6], [0, 1], {extrapolateRight: 'clamp'}) : 0;
	const dim = decided && !best ? interpolate(w, [0, 8], [0, 0.55], {extrapolateRight: 'clamp'}) : 0;
	const stamp = spring({frame: w, fps, config: {damping: 9, mass: 0.6}});
	const base = top ? C.red : C.blue;
	const dark = top ? C.redDark : C.blueDark;
	return (
		<div style={{
			position: 'absolute', left: 0, right: 0, height: 960, top: top ? 0 : 960, overflow: 'hidden',
			background: `radial-gradient(circle at 50% ${top ? 60 : 40}%, ${base} 0%, ${dark} 120%)`,
		}}>
			<AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, ${C.green} 0%, ${C.greenDark} 120%)`, opacity: greenIn}} />
			<div style={{
				position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34,
				justifyContent: top ? 'flex-end' : 'flex-start', paddingTop: top ? 0 : 140, paddingBottom: top ? 140 : 0, paddingLeft: 60, paddingRight: 60,
			}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 26}}>
					{side.emoji ? <div style={{fontFamily: EMOJI, fontSize: 120, lineHeight: 1}}>{side.emoji}</div> : null}
					<div style={{fontFamily: DISPLAY, fontSize: 78, lineHeight: 1.02, color: C.white, textTransform: 'uppercase', maxWidth: 760, ...stroke(7)}}>{side.label}</div>
				</div>
				{side.fact ? <div style={{
					fontFamily: HEAVY, fontSize: 52, lineHeight: 1.18, color: C.ink, background: C.white, borderRadius: 26,
					padding: '26px 36px', textAlign: 'center', maxWidth: 940, whiteSpace: 'pre-line', boxShadow: '0 18px 44px rgba(0,0,0,.35)',
					opacity: frame < factAt ? 0 : 1, transform: `scale(${0.7 + 0.3 * f}) rotate(${top ? -1.5 : 1.5}deg)`,
				}}>{side.fact}</div> : null}
			</div>
			{decided ? (
				<div style={{
					position: 'absolute', top: top ? 70 : undefined, bottom: top ? undefined : 110, left: 0, right: 0, display: 'flex', justifyContent: 'center',
				}}>
					<div style={{
						fontFamily: DISPLAY, fontSize: 96, color: best ? C.ink : C.white, background: best ? C.yellow : 'rgba(0,0,0,.55)',
						border: `8px solid ${C.ink}`, borderRadius: 24, padding: '6px 40px', transform: `scale(${stamp}) rotate(${best ? -6 : 4}deg)`,
					}}>{best ? `✓ ${stamps[0]}` : `✕ ${stamps[1]}`}</div>
				</div>
			) : null}
			<AbsoluteFill style={{background: '#000', opacity: dim}} />
		</div>
	);
};

const Explain: React.FC<{s: Segment}> = ({s}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const aAt = s.aAt ?? 0;
	const bAt = s.bAt ?? 0;
	const winAt = s.winAt ?? 0;
	const pill = spring({frame, fps, config: {damping: 10}});
	const wt = frame - winAt;
	const shake = wt >= 0 && wt < 10 ? Math.sin(wt * 2.6) * (10 - wt) * 2.5 : 0;
	return (
		<AbsoluteFill style={{transform: `translate(${shake}px, ${-shake * 0.5}px)`}}>
			<ExplainHalf side={s.a!} top factAt={aAt} winAt={winAt} best={s.best === 'a'} stamps={s.stamps ?? ['BESSER', 'SCHLECHTER']} />
			<ExplainHalf side={s.b!} top={false} factAt={bAt} winAt={winAt} best={s.best === 'b'} stamps={s.stamps ?? ['BESSER', 'SCHLECHTER']} />
			<div style={{
				position: 'absolute', left: 540 - 250, top: 960 - 62, width: 500, height: 124, borderRadius: 62,
				background: C.yellow, border: `8px solid ${C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
				fontFamily: HEAVY, fontSize: 58, color: C.ink, transform: `scale(${pill}) rotate(-3deg)`,
			}}>AUFLÖSUNG</div>
			{s.note ? (
				<div style={{position: 'absolute', bottom: 40, left: 0, right: 0, textAlign: 'center', fontFamily: HEAVY, fontSize: 26,
					color: 'rgba(255,255,255,.75)'}}>{s.note}</div>
			) : null}
			<Audio src={staticFile('sfx/whoosh.mp3')} volume={0.6} />
			{s.audio ? <Sequence from={aAt}><Audio src={staticFile(s.audio)} /></Sequence> : null}
			{s.audioB ? <Sequence from={bAt}><Audio src={staticFile(s.audioB)} /></Sequence> : null}
			<Sequence from={winAt}><Audio src={staticFile('sfx/check.mp3')} volume={0.8} /></Sequence>
			<Sequence from={winAt}><Audio src={staticFile('sfx/bling.mp3')} volume={0.6} /></Sequence>
			{s.winAudio ? <Sequence from={winAt + 6}><Audio src={staticFile(s.winAudio)} /></Sequence> : null}
		</AbsoluteFill>
	);
};

// Kaputte Streifen, Farbversatz und Scanlines, solange der TTS-Bug laeuft
const Glitch: React.FC<{frame: number}> = ({frame}) => {
	const bars = new Array(7).fill(0).map((_, i) => {
		const y = random(`gy${frame}${i}`) * 1920;
		const h = 20 + random(`gh${frame}${i}`) * 140;
		const x = (random(`gx${frame}${i}`) - 0.5) * 300;
		const col = ['rgba(255,0,80,.55)', 'rgba(0,255,255,.5)', 'rgba(255,255,255,.6)', 'rgba(0,0,0,.7)'][i % 4];
		return <div key={i} style={{position: 'absolute', left: x, top: y, width: 1080 + 300, height: h, background: col, mixBlendMode: 'screen'}} />;
	});
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{bars}
			<AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(0,0,0,.25) 0 3px, transparent 3px 7px)'}} />
			{random(`gf${frame}`) > 0.7 ? <AbsoluteFill style={{background: random(`gc${frame}`) > 0.5 ? '#ff0050' : '#00ffff', opacity: 0.35}} /> : null}
		</AbsoluteFill>
	);
};

const Outro: React.FC<{s: Segment; handle: string | null}> = ({s, handle}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const a = spring({frame, fps, config: {damping: 11}});
	return (
		<AbsoluteFill style={{background: C.ink, alignItems: 'center', justifyContent: 'center', gap: 50, padding: 80}}>
			<div style={{fontFamily: DISPLAY, fontSize: 120, lineHeight: 1.05, color: C.white, textAlign: 'center', transform: `scale(${a})`}}>
				{s.title ?? 'WIE OFT LAGST DU RICHTIG?'}
			</div>
			<div style={{fontFamily: HEAVY, fontSize: 50, whiteSpace: 'nowrap', color: C.ink, background: C.yellow, padding: '14px 34px', borderRadius: 18}}>⬇ {s.sub ?? 'Schreibs in die Kommentare'}</div>
			{s.share ? <div style={{fontFamily: HEAVY, fontSize: 46, color: C.white, textAlign: 'center', maxWidth: 920}}>📲 {s.share}</div> : null}
			<FollowPill handle={handle} still />
			<Audio src={staticFile(s.audio)} />
		</AbsoluteFill>
	);
};

const FollowPill: React.FC<{handle: string | null; still?: boolean}> = ({handle, still}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame, fps, config: {damping: 12}});
	const tapped = frame > 22;
	return (
		<div style={{
			display: 'flex', alignItems: 'center', gap: 22, background: C.white, borderRadius: 80,
			padding: '18px 22px 18px 40px', boxShadow: '0 20px 50px rgba(0,0,0,.4)', transform: `scale(${s})`,
			position: still ? 'relative' : 'absolute', ...(still ? {} : {top: 70, left: 540, translate: '-50% 0'}),
		}}>
			<div style={{fontFamily: HEAVY, fontSize: 46, whiteSpace: 'nowrap', color: C.ink}}>{handle ?? 'Folg für Teil 2'}</div>
			<div style={{
				fontFamily: HEAVY, fontSize: 40, whiteSpace: 'nowrap', color: C.white, background: tapped ? C.green : C.red, borderRadius: 50,
				padding: '14px 30px', transform: `scale(${tapped ? 1 : 1 + 0.06 * Math.sin(frame / 3)})`,
			}}>{tapped ? '✓ Gefolgt' : '+ Folgen'}</div>
		</div>
	);
};

export const Comparison: React.FC<{timeline: Timeline}> = ({timeline}) => {
	const segs = timeline.segments;
	// Follow-Einblendung: Kanal A nach der Hook-Frage, Kanal B direkt nach dem Intro
	const followAt = segs.length ? segs[0].duration : 0;
	return (
		<AbsoluteFill style={{background: C.ink}}>
			<style>{fontFaces}</style>
			<Series>
				{segs.map((s, i) => (
					<Series.Sequence key={i} durationInFrames={s.duration}>
						{s.kind === 'intro' ? <Intro s={s} /> : s.kind === 'outro' ? <Outro s={s} handle={timeline.handle} />
							: s.kind === 'explain' ? <Explain s={s} /> : s.kind === 'loop' ? <Loop s={s} /> : s.kind === 'scene' ? <Scene s={s} /> : <Question s={s} />}
					</Series.Sequence>
				))}
			</Series>
			{segs.length && !timeline.noFollow ? (
				<Sequence from={followAt} durationInFrames={95}>
					<FollowPill handle={timeline.handle} />
				</Sequence>
			) : null}
		</AbsoluteFill>
	);
};
