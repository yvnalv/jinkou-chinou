# Generated Voiceover & Word Timestamp Output Folder

Store synthesized per-scene voiceover clips and their timing JSON files here (or under the project's `public/vo/`):
- `scene-01.mp3`, `scene-02.mp3`, ... : one clip per scene from `generate_databro_cloned_vo.py`, wired in via `voiceoverCues` on `<DatabroBaseCanvas />`.
- `scene-01.json`, ... : `speechEndFrame`, word timings, and ready `captions` (`DatabroCaptionCue[]`: `{ text, startFrame, endFrame }`, relative to the clip start). Offset them by the scene start frame plus the head delay for the fixed `Y = 1480px` Closed Captions.
