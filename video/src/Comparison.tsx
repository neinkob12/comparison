import React from 'react';
import {
	AbsoluteFill, Audio, Img, Sequence, Series, interpolate, spring, staticFile,
	useCurrentFrame, useVideoConfig,
} from 'remotion';

type Side = {label: string; img: string | null};
type Segment = {
	kind: 'intro' | 'q' | 'hook' | 'mid' | 'outro';
	audio: string; speak: number; gap?: number; hold: number; duration: number;
	title?: string; sub?: string; a?: Side; b?: Side; pct?: [number, number]; num?: number; total?: number;
};
export type Timeline = {
	id: string; channel: 'A' | 'B'; handle: string | null; fps: number;
	durationInFrames: number; segments: Segment[];
};

const C = {
	red: '#e3263b', redDark: '#7a0f1c', blue: '#2350e6', blueDark: '#0e2470',
	yellow: '#ffd23f', green: '#1fbf6a', ink: '#0d0c12', white: '#ffffff',
};

const fontFaces = `
@font-face{font-family:Anton;src:url(${staticFile('fonts/Anton.woff2')}) format('woff2');}
@font-face{font-family:ArchivoBlack;src:url(${staticFile('fonts/ArchivoBlack.woff2')}) format('woff2');}
`;
const DISPLAY = 'Anton, "Arial Narrow", Impact, sans-serif';
const HEAVY = 'ArchivoBlack, "Arial Black", sans-serif';

const stroke = (px: number) => ({
	WebkitTextStroke: `${px}px ${C.ink}`, paintOrder: 'stroke fill' as const,
	textShadow: `0 ${px}px 0 ${C.ink}`,
});

const Half: React.FC<{side: Side; top: boolean; pct: number; win: boolean; revealAt: number; mid: boolean}> = ({side, top, pct, win, revealAt, mid}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const enter = spring({frame, fps, config: {damping: 14, mass: 0.6}, delay: top ? 0 : 4});
	const rev = spring({frame: frame - revealAt, fps, config: {damping: 9, mass: 0.7}});
	const shown = frame >= revealAt;
	const count = Math.round(interpolate(frame - revealAt, [0, 14], [0, pct], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
	const base = mid ? (top ? C.yellow : C.green) : top ? C.red : C.blue;
	const dark = mid ? C.ink : top ? C.redDark : C.blueDark;
	const dim = shown && !win ? interpolate(frame - revealAt, [0, 8], [0, 0.45], {extrapolateRight: 'clamp'}) : 0;
	return (
		<div style={{
			position: 'absolute', left: 0, right: 0, height: 960, top: top ? 0 : 960,
			background: `radial-gradient(circle at 50% ${top ? 60 : 40}%, ${base} 0%, ${dark} 120%)`,
			display: 'flex', flexDirection: 'column', alignItems: 'center',
			justifyContent: top ? 'flex-end' : 'flex-start',
			paddingTop: top ? 0 : 110, paddingBottom: top ? 110 : 0, gap: 34,
		}}>
			{top ? null : <Label text={side.label} enter={enter} mid={mid} />}
			<div style={{position: 'relative', transform: `scale(${0.6 + 0.4 * enter})`}}>
				{side.img ? (
					<Img src={staticFile(side.img)} style={{
						width: mid ? 0 : 500, height: 500, objectFit: 'cover', borderRadius: 36,
						border: `10px solid ${C.white}`, boxShadow: '0 24px 60px rgba(0,0,0,.45)',
					}} />
				) : (
					<div style={{width: mid ? 0 : 500, height: mid ? 0 : 500}} />
				)}
				{shown ? (
					<div style={{
						position: 'absolute', inset: mid ? -170 : 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
						fontFamily: DISPLAY, fontSize: 230, color: C.white, transform: `scale(${rev})`, ...stroke(12),
					}}>{count}%</div>
				) : null}
			</div>
			{top ? <Label text={side.label} enter={enter} mid={mid} /> : null}
			<AbsoluteFill style={{background: '#000', opacity: dim, pointerEvents: 'none'}} />
		</div>
	);
};

const Label: React.FC<{text: string; enter: number; mid: boolean}> = ({text, enter, mid}) => (
	<div style={{
		fontFamily: DISPLAY, fontSize: mid ? 120 : 92, lineHeight: 1.02, color: C.white, textAlign: 'center',
		textTransform: 'uppercase', maxWidth: 940, opacity: enter, transform: `translateY(${(1 - enter) * 40}px)`,
		...stroke(8),
	}}>{text}</div>
);

const Oder: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = spring({frame: frame - 6, fps, config: {damping: 10}});
	return (
		<div style={{
			position: 'absolute', left: 540 - 120, top: 960 - 70, width: 240, height: 140, borderRadius: 70,
			background: C.white, border: `8px solid ${C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
			fontFamily: HEAVY, fontSize: 64, color: C.ink, transform: `scale(${s}) rotate(-4deg)`,
		}}>ODER</div>
	);
};

const Counter: React.FC<{num: number; total: number}> = ({num, total}) => (
	<div style={{
		position: 'absolute', top: 185, left: 60, padding: '10px 26px', borderRadius: 40, background: 'rgba(0,0,0,.55)',
		fontFamily: HEAVY, fontSize: 40, color: C.white,
	}}>{num}/{total}</div>
);

const Question: React.FC<{s: Segment}> = ({s}) => {
	const revealAt = s.speak + (s.gap ?? 0);
	const [pa, pb] = s.pct!;
	const mid = s.kind === 'mid';
	return (
		<AbsoluteFill>
			<Half side={s.a!} top pct={pa} win={pa >= pb} revealAt={revealAt} mid={mid} />
			<Half side={s.b!} top={false} pct={pb} win={pb > pa} revealAt={revealAt} mid={mid} />
			<Oder />
			{s.kind === 'q' ? <Counter num={s.num!} total={s.total!} /> : null}
			{mid ? <Banner text="KURZE PAUSE" /> : null}
			<Audio src={staticFile(s.audio)} />
			<Sequence from={revealAt}><Audio src={staticFile('sfx/pop.mp3')} volume={0.6} /></Sequence>
		</AbsoluteFill>
	);
};

const Banner: React.FC<{text: string}> = ({text}) => (
	<div style={{
		position: 'absolute', top: 120, left: 0, right: 0, textAlign: 'center', fontFamily: HEAVY, fontSize: 54,
		color: C.ink, letterSpacing: 4,
	}}>{text}</div>
);

const Intro: React.FC<{s: Segment}> = ({s}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const a = spring({frame, fps, config: {damping: 11}});
	const b = spring({frame: frame - 8, fps, config: {damping: 12}});
	return (
		<AbsoluteFill style={{background: `linear-gradient(180deg, ${C.red} 0%, ${C.red} 50%, ${C.blue} 50%, ${C.blue} 100%)`, alignItems: 'center', justifyContent: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 170, whiteSpace: 'nowrap', color: C.white, transform: `scale(${a}) rotate(-3deg)`, ...stroke(12)}}>{s.title}</div>
			<div style={{fontFamily: HEAVY, fontSize: 70, color: C.ink, background: C.yellow, padding: '12px 36px', borderRadius: 18, marginTop: 30, transform: `scale(${b})`}}>{s.sub}</div>
			<Audio src={staticFile(s.audio)} />
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
			<FollowPill handle={handle} from={20} still />
			<Audio src={staticFile(s.audio)} />
		</AbsoluteFill>
	);
};

const FollowPill: React.FC<{handle: string | null; from: number; still?: boolean}> = ({handle, from, still}) => {
	const frame = useCurrentFrame() - from;
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
	let followAt = 0;
	if (segs.length) {
		const first = segs[0];
		followAt = timeline.channel === 'A' ? first.duration : first.duration - 10;
	}
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
					<FollowPill handle={timeline.handle} from={0} />
				</Sequence>
			) : null}
		</AbsoluteFill>
	);
};
