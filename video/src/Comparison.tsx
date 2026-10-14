import React from 'react';
import {
	AbsoluteFill, Audio, Img, Sequence, Series, interpolate, spring, staticFile,
	useCurrentFrame, useVideoConfig,
} from 'remotion';

type Side = {label: string; img: string | null; emoji?: string | null};
type Segment = {
	kind: 'intro' | 'q' | 'hook' | 'mid' | 'outro';
	audio: string; speak: number; gap?: number; hold: number; duration: number; voiceAt?: number;
	title?: string; sub?: string; a?: Side; b?: Side; pct?: [number, number];
};
export type Timeline = {
	id: string; channel: 'A' | 'B'; handle: string | null; fps: number;
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

const Half: React.FC<{side: Side; top: boolean; pct: number; win: boolean; revealAt: number; mid: boolean}> = ({side, top, pct, win, revealAt, mid}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const enter = spring({frame, fps, config: {damping: 14, mass: 0.6}, delay: top ? 0 : 4});
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
	const visual = side.img ? (
		<Img src={staticFile(side.img)} style={{
			width: 470, height: 470, objectFit: 'cover', borderRadius: 36,
			border: `10px solid ${greenIn > 0.5 ? C.green : C.white}`, boxShadow: '0 24px 60px rgba(0,0,0,.45)',
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
			}}>
				{top ? null : <Label text={side.label} enter={enter} />}
				<div style={{position: 'relative', transform: `scale(${(0.6 + 0.4 * enter) * pulse})`}}>
					{visual}
					{shown ? (
						<div style={{
							position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
							fontFamily: DISPLAY, fontSize: 230, color: C.white, transform: `scale(${rev})`, ...stroke(12),
						}}>{count}%</div>
					) : null}
				</div>
				{top ? <Label text={side.label} enter={enter} /> : null}
			</div>
			<AbsoluteFill style={{background: '#000', opacity: dim}} />
			<AbsoluteFill style={{background: C.white, opacity: flash}} />
		</div>
	);
};

const Label: React.FC<{text: string; enter: number}> = ({text, enter}) => (
	<div style={{
		fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.02, color: C.white, textAlign: 'center',
		textTransform: 'uppercase', maxWidth: 940, opacity: enter, transform: `translateY(${(1 - enter) * 40}px)`,
		...stroke(8),
	}}>{text}</div>
);

// Mitte: ODER waehrend der Frage, dann 3-2-1, dann weg
const Center: React.FC<{speakEnd: number}> = ({speakEnd}) => {
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
	if (t >= COUNT) return null;
	const n = 3 - Math.floor(t / 30);
	const local = t % 30;
	const s = spring({frame: local, fps, config: {damping: 8, mass: 0.5}});
	const ring = interpolate(t, [0, COUNT], [1, 0]);
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
				fontFamily: DISPLAY, fontSize: 150, color: C.ink, transform: `scale(${0.4 + 0.6 * s})`,
			}}>{n}</div>
		</div>
	);
};

const Question: React.FC<{s: Segment}> = ({s}) => {
	const revealAt = s.speak + (s.gap ?? 0);
	const [pa, pb] = s.pct!;
	const mid = s.kind === 'mid';
	return (
		<AbsoluteFill>
			<Half side={s.a!} top pct={pa} win={pa >= pb} revealAt={revealAt} mid={mid} />
			<Half side={s.b!} top={false} pct={pb} win={pb > pa} revealAt={revealAt} mid={mid} />
			<Center speakEnd={s.speak} />
			<Audio src={staticFile(s.audio)} />
			{[0, 30, 60].map((d) => (
				<Sequence key={d} from={s.speak + d} durationInFrames={10}><Audio src={staticFile('sfx/tick.mp3')} volume={0.8} /></Sequence>
			))}
			<Sequence from={revealAt}><Audio src={staticFile('sfx/bling.mp3')} volume={0.7} /></Sequence>
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
	return (
		<AbsoluteFill style={{
			background: `linear-gradient(180deg, ${C.red} 0%, ${C.red} 50%, ${C.blue} 50%, ${C.blue} 100%)`,
			alignItems: 'center', justifyContent: 'center', transform: `translate(${sx}px, ${sx * 0.6}px) scale(1.06)`,
		}}>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0, transform: 'rotate(-4deg)'}}>
				<div style={{
					fontFamily: DISPLAY, fontSize: 290, lineHeight: 0.95, color: C.white, whiteSpace: 'nowrap',
					transform: `translateX(${(1 - a) * -1300}px)`, ...stroke(14),
				}}>{s.title}</div>
				<div style={{
					fontFamily: DISPLAY, fontSize: 290, lineHeight: 0.95, color: C.yellow, whiteSpace: 'nowrap',
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

const Outro: React.FC<{s: Segment; handle: string | null}> = ({s, handle}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const a = spring({frame, fps, config: {damping: 11}});
	return (
		<AbsoluteFill style={{background: C.ink, alignItems: 'center', justifyContent: 'center', gap: 50, padding: 80}}>
			<div style={{fontFamily: DISPLAY, fontSize: 120, lineHeight: 1.05, color: C.white, textAlign: 'center', transform: `scale(${a})`}}>
				WIE OFT WARST DU BEI DER <span style={{color: C.yellow}}>MEHRHEIT?</span>
			</div>
			<div style={{fontFamily: HEAVY, fontSize: 56, color: C.white, opacity: 0.85}}>⬇ Ab in die Kommentare</div>
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
						{s.kind === 'intro' ? <Intro s={s} /> : s.kind === 'outro' ? <Outro s={s} handle={timeline.handle} /> : <Question s={s} />}
					</Series.Sequence>
				))}
			</Series>
			{segs.length ? (
				<Sequence from={followAt} durationInFrames={95}>
					<FollowPill handle={timeline.handle} />
				</Sequence>
			) : null}
		</AbsoluteFill>
	);
};
