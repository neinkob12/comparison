import React from 'react';
import {Composition, staticFile} from 'remotion';
import {Comparison, Timeline} from './Comparison';

const empty: Timeline = {id: 'a01', channel: 'A', handle: null, fps: 30, durationInFrames: 300, segments: []};

export const Root: React.FC = () => (
	<Composition
		id="Comparison"
		component={Comparison}
		width={1080}
		height={1920}
		fps={30}
		durationInFrames={300}
		defaultProps={{timeline: empty}}
		calculateMetadata={async ({props}) => {
			let tl = props.timeline;
			if (!tl.segments.length) {
				tl = await fetch(staticFile(`timelines/${tl.id}.json`)).then((r) => r.json());
			}
			return {durationInFrames: tl.durationInFrames, props: {timeline: tl}};
		}}
	/>
);
