import React from 'react';
import {
	AbsoluteFill, Audio, Img, Sequence, Series, interpolate, random, spring, staticFile,
	useCurrentFrame, useVideoConfig,
} from 'remotion';

type Side = {label: string; img: string | null; emoji?: string | null; fact?: string};
type Segment = {
	kind: 'intro' | 'q' | 'hook' | 'mid' | 'explain' | 'outro';
	audio: string; audioB?: string; bAt?: number; speak: number; gap?: number; hold: number; duration: number; voiceAt?: number;
	share?: string; winAudio?: string; banner?: string; aAt?: number; winAt?: number; best?: 'a' | 'b'; note?: string;
	title?: string; sub?: string; a?: Side; b?: Side; pct?: [number, number];
};
export type Timeline = {
	id: string; channel: string; handle: string | null; fps: number;
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

const COUNT = 81; // 3-2-1 in Frames (Standard, sonst s.gap)

const Half: React.FC<{side: Side; top: boolean; pct: number; win: boolean; revealAt: number; mid: boolean; enterAt: number}> = ({side, top, pct, win, revealAt, mid, enterAt}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	// Reinfliegen: oben von links, unten von rechts, mit Bewegungsunschaerfe
	const fly = spring({frame: frame - enterAt, fps, config: {damping: 16, stiffness: 260, mass: 0.6}});
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
			width: 420, height: 420, borderRadius: 210, background: C.white, border: `10px solid ${greenIn > 0.5 ? C.green : C.ink}`,
			display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EMOJI, fontSize: 250, lineHeight: 1,
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
				opacity: frame < enterAt ? 0 : 1,
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
	const step = count / 3;
	const n = 3 - Math.floor(t / step);
	const local = t - (3 - n) * step;
	const s = spring({frame: local * (30 / step), fps, config: {damping: 8, mass: 0.5}});
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

// Hook-Sticker: steht ab Frame 0, wackelt leicht, verschwindet zur Aufloesung
const Banner: React.FC<{text: string; until: number}> = ({text, until}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const out = spring({frame: frame - until + 4, fps, config: {damping: 14}});
	const pop = interpolate(frame, [0, 3, 8], [1, 1.12, 1], {extrapolateRight: 'clamp'});
	if (out > 0.98) return null;
	return (
		<div style={{
			position: 'absolute', top: 120, left: 0, right: 0, display: 'flex', justifyContent: 'center',
			transform: `scale(${pop * (1 - out)}) rotate(${-3 + 1.5 * Math.sin(frame / 4)}deg)`,
		}}>
			<div style={{
				fontFamily: HEAVY, fontSize: 54, color: C.ink, background: C.yellow, padding: '14px 30px', borderRadius: 22,
				border: `7px solid ${C.ink}`, boxShadow: '0 16px 40px rgba(0,0,0,.45)', whiteSpace: 'nowrap',
			}}>{text.replace(/\s*\p{Extended_Pictographic}+$/u, '')} <span style={{fontFamily: EMOJI}}>{text.match(/\p{Extended_Pictographic}+$/u)?.[0] ?? ''}</span></div>
		</div>
	);
};

const Question: React.FC<{s: Segment}> = ({s}) => {
	const revealAt = s.speak + (s.gap ?? 0);
	const bAt = s.bAt ?? 4;
	const [pa, pb] = s.pct!;
	const mid = s.kind === 'mid';
	const hook = s.kind === 'hook';
	const count = s.gap ?? COUNT;
	const frame = useCurrentFrame();
	const punch = interpolate(frame, [0, 7], [hook ? 1.06 : 1.12, 1], {extrapolateRight: 'clamp'});
	const rt = frame - revealAt;
	const shake = rt >= 0 && rt < 10 ? Math.sin(rt * 2.6) * (10 - rt) * 2.5 : 0;
	const ct = frame - s.speak;
	const panic = ct >= (hook ? 0 : count * 2 / 3) && ct < count ? (hook ? 0.35 : 0.25) * (0.5 + 0.5 * Math.sin(ct * (hook ? 2 : 1.2))) : 0;
	// Hook: beide Seiten stehen ab Frame 0, harter Einschlag + Wackeln + weisser Blitz
	const hs = hook && frame < 12 ? Math.sin(frame * 2.4) * (12 - frame) * 3 : 0;
	const hflash = hook ? interpolate(frame, [0, 2, 9], [0, 0.45, 0], {extrapolateRight: 'clamp'}) : 0;
	return (
		<AbsoluteFill style={{transform: `scale(${punch}) translate(${shake + hs}px, ${-(shake + hs) * 0.5}px)`}}>
			<Half side={s.a!} top pct={pa} win={pa >= pb} revealAt={revealAt} mid={mid} enterAt={hook ? -30 : 0} />
			<Half side={s.b!} top={false} pct={pb} win={pb > pa} revealAt={revealAt} mid={mid} enterAt={hook ? -30 : bAt} />
			<Center speakEnd={s.speak} count={count} />
			{hook && s.banner ? <Banner text={s.banner} until={revealAt} /> : null}
			<AbsoluteFill style={{background: C.white, opacity: hflash, pointerEvents: 'none'}} />
			<AbsoluteFill style={{boxShadow: `inset 0 0 220px 60px rgba(255,0,0,${panic})`, pointerEvents: 'none'}} />
			<Audio src={staticFile(s.audio)} />
			{s.audioB ? <Sequence from={bAt}><Audio src={staticFile(s.audioB)} /></Sequence> : null}
			<Audio src={staticFile('sfx/whoosh.mp3')} volume={0.7} />
			{hook ? <>
				<Audio src={staticFile('sfx/impact.mp3')} volume={1} />
				<Sequence from={2}><Audio src={staticFile('sfx/ring.mp3')} volume={0.5} /></Sequence>
				<Sequence from={4}><Audio src={staticFile('sfx/pop.mp3')} volume={0.9} /></Sequence>
				<Sequence from={bAt}><Audio src={staticFile('sfx/impact.mp3')} volume={0.8} /></Sequence>
			</> : null}
			<Sequence from={bAt}><Audio src={staticFile('sfx/whoosh.mp3')} volume={0.7} /></Sequence>
			<Sequence from={s.speak} durationInFrames={count}><Audio src={staticFile('sfx/countdown.mp3')} volume={0.9} playbackRate={90 / count} /></Sequence>
			<Sequence from={revealAt}><Audio src={staticFile('sfx/check.mp3')} volume={0.8} /></Sequence>
			{s.winAudio ? <Sequence from={revealAt + 12}><Audio src={staticFile(s.winAudio)} /></Sequence> : null}
		</AbsoluteFill>
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
	const sx = shake(7) + shake(14);
	const flash = interpolate(frame, [14, 16, 24], [0, 0.6, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const fit = (t?: string) => Math.min(290, Math.floor(1900 / Math.max(1, (t ?? '').length)));
	return (
		<AbsoluteFill style={{
			background: `linear-gradient(180deg, ${C.red} 0%, ${C.red} 50%, ${C.blue} 50%, ${C.blue} 100%)`,
			alignItems: 'center', justifyContent: 'center', transform: `translate(${sx}px, ${sx * 0.6}px) scale(1.06)`,
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
			<Sequence from={0}><Audio src={staticFile('sfx/whoosh.mp3')} volume={0.7} /></Sequence>
			<Sequence from={7}><Audio src={staticFile('sfx/impact.mp3')} volume={0.9} /></Sequence>
			<Sequence from={7}><Audio src={staticFile('sfx/whoosh.mp3')} volume={0.6} /></Sequence>
			<Sequence from={14}><Audio src={staticFile('sfx/impact.mp3')} volume={1} /></Sequence>
			<Sequence from={s.voiceAt ?? 0}><Audio src={staticFile(s.audio)} volume={1} /></Sequence>
		</AbsoluteFill>
	);
};

// Aufloesung: beide Optionen mit Fakt, dann wird die bessere gruen gestempelt
const ExplainHalf: React.FC<{side: Side; top: boolean; factAt: number; winAt: number; best: boolean}> = ({side, top, factAt, winAt, best}) => {
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
				<div style={{
					fontFamily: HEAVY, fontSize: 52, lineHeight: 1.18, color: C.ink, background: C.white, borderRadius: 26,
					padding: '26px 36px', textAlign: 'center', maxWidth: 940, whiteSpace: 'pre-line', boxShadow: '0 18px 44px rgba(0,0,0,.35)',
					opacity: frame < factAt ? 0 : 1, transform: `scale(${0.7 + 0.3 * f}) rotate(${top ? -1.5 : 1.5}deg)`,
				}}>{side.fact}</div>
			</div>
			{decided ? (
				<div style={{
					position: 'absolute', top: top ? 70 : undefined, bottom: top ? undefined : 110, left: 0, right: 0, display: 'flex', justifyContent: 'center',
				}}>
					<div style={{
						fontFamily: DISPLAY, fontSize: 96, color: best ? C.ink : C.white, background: best ? C.yellow : 'rgba(0,0,0,.55)',
						border: `8px solid ${C.ink}`, borderRadius: 24, padding: '6px 40px', transform: `scale(${stamp}) rotate(${best ? -6 : 4}deg)`,
					}}>{best ? '✓ BESSER' : '✕ SCHLECHTER'}</div>
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
			<ExplainHalf side={s.a!} top factAt={aAt} winAt={winAt} best={s.best === 'a'} />
			<ExplainHalf side={s.b!} top={false} factAt={bAt} winAt={winAt} best={s.best === 'b'} />
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
			<Sequence from={aAt}><Audio src={staticFile(s.audio)} /></Sequence>
			{s.audioB ? <Sequence from={bAt}><Audio src={staticFile(s.audioB)} /></Sequence> : null}
			<Sequence from={winAt}><Audio src={staticFile('sfx/check.mp3')} volume={0.8} /></Sequence>
			<Sequence from={winAt}><Audio src={staticFile('sfx/bling.mp3')} volume={0.6} /></Sequence>
			{s.winAudio ? <Sequence from={winAt + 6}><Audio src={staticFile(s.winAudio)} /></Sequence> : null}
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

// Follow-Popup mitten im Bild, Rest wird kurz unscharf (ca. 0.7 s sichtbar)
const FOLLOW = 27;
const FollowPopup: React.FC<{handle: string | null}> = ({handle}) => {
	const frame = useCurrentFrame();
	const fade = interpolate(frame, [0, 3, FOLLOW - 4, FOLLOW], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{
			backdropFilter: `blur(${18 * fade}px)`, WebkitBackdropFilter: `blur(${18 * fade}px)`, background: `rgba(0,0,0,${0.35 * fade})`,
			alignItems: 'center', justifyContent: 'center',
		}}>
			<div style={{opacity: fade, transform: `scale(${1.4 - 0.25 * fade})`}}>
				<FollowPill handle={handle} still tapAt={11} />
			</div>
			<Audio src={staticFile('sfx/pop.mp3')} volume={1} />
			<Sequence from={11}><Audio src={staticFile('sfx/check.mp3')} volume={0.6} /></Sequence>
		</AbsoluteFill>
	);
};

const FollowPill: React.FC<{handle: string | null; still?: boolean; tapAt?: number}> = ({handle, still, tapAt = 22}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame, fps, config: {damping: 12}});
	const tapped = frame > tapAt;
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
							: s.kind === 'explain' ? <Explain s={s} /> : <Question s={s} />}
					</Series.Sequence>
				))}
			</Series>
			{segs.length ? (
				<Sequence from={followAt} durationInFrames={FOLLOW}>
					<FollowPopup handle={timeline.handle} />
				</Sequence>
			) : null}
		</AbsoluteFill>
	);
};
