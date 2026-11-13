import React from 'react';
import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from 'remotion';
import { Camera, FlaskConical, Laptop, Sun, Vibrate, Wind } from 'lucide-react';
import { C, CENTER_X, POPPINS } from './theme';
import { at, ease, mix, pop } from './timing';
import { AppTile, Background, Captions, TopLockup, Wipe } from './components/Base';
import { EndCard, LineChart, Meter, Panel, StepHeading } from './components/Patterns';
import { VOICEOVER_FILE } from './voiceover';

// Example reel wired to src/data/captions.json (the content-ideas reel.starter.json story).
// Replace the scenes, keep the structure: every beat starts at a caption cue via at(id).

const MomentScene: React.FC = () => {
  const f = useCurrentFrame();
  const pGood = ease(f, at(1) + 6, 40);
  const pBad = ease(f, at(5) + 6, 26);
  const value = pBad > 0 ? Math.round(mix(98, 51, pBad)) : Math.round(mix(60, 98, pGood));
  return (
    <Panel start={0} end={at(7)}>
      <AppTile icon={Laptop} label="Lab" size={150} scale={pop(f, at(1))} style={{ left: CENTER_X - 220, top: 360 }} />
      <AppTile icon={Camera} label="Factory camera" size={150} color={C.lime} border={C.lime} glow scale={pop(f, at(3))} style={{ left: CENTER_X + 70, top: 360 }} />
      <LineChart good={[60, 72, 85, 93, 98]} bad={[98, 74, 51]} pGood={pGood} pBad={pBad} width={560} height={230} label="Defects caught" value={`${value}%`} style={{ position: 'absolute', left: CENTER_X - 304, top: 640, width: 608 }} />
    </Panel>
  );
};

const TurnScene: React.FC = () => {
  const f = useCurrentFrame();
  const tiles = [
    { icon: Sun, label: 'Glare', t: at(9) },
    { icon: Wind, label: 'Dust', t: at(10) },
    { icon: Vibrate, label: 'Shake', t: at(11) },
  ];
  return (
    <Panel start={at(7)} end={at(13)}>
      <StepHeading kicker="WHAT CHANGED" title={<>The lab never saw <span style={{ color: C.lime }}>the glare.</span></>} left={120} width={840} />
      {tiles.map((t, i) => (
        <AppTile key={t.label} icon={t.icon} label={t.label} size={180} color={C.danger} border={C.borderHi} scale={pop(f, t.t)} style={{ left: CENTER_X - 300 - 90 + i * 300, top: 640 }} />
      ))}
    </Panel>
  );
};

const LessonScene: React.FC = () => {
  const f = useCurrentFrame();
  const v = mix(1, 5, ease(f, at(15), 30));
  return (
    <Panel start={at(13)} end={at(17)}>
      <StepHeading kicker="THE LESSON" title={<>Test the slice, <span style={{ color: C.lime }}>not the average.</span></>} left={120} width={840} />
      <AppTile icon={Camera} label="Real frames" size={170} color={C.lime} border={C.lime} scale={pop(f, at(14))} style={{ left: CENTER_X - 85, top: 620 }} />
      <Meter icon={FlaskConical} label="Glare slice tests passing" value={v} total={5} left={120} top={980} width={840} opacity={ease(f, at(15), 10)} />
    </Panel>
  );
};

export const Reel: React.FC<{ showCaptions: boolean }> = ({ showCaptions }) => (
  <AbsoluteFill style={{ backgroundColor: C.bg, fontFamily: POPPINS, color: C.ivory }}>
    <Background />
    {VOICEOVER_FILE ? <Audio src={staticFile(VOICEOVER_FILE)} /> : null}
    <MomentScene />
    <TurnScene />
    <LessonScene />
    <EndCard />
    <TopLockup />
    <Wipe t={at(7)} />
    {showCaptions ? <Captions /> : null}
  </AbsoluteFill>
);
