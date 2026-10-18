# 규리 목소리 만들기

규리 목소리는 무료 TTS **Kokoro**로 만들어요. 원래 규리 녹음과 맞춘 값:

- 목소리: `af_heart`
- 속도: `0.85`
- 음 높이: 1.25배 (`ffmpeg -af "asetrate=30000,aresample=24000,atempo=0.8"`)
- 저장: mp3, 24kHz, 모노, 48kbps

`make_clip.py`는 대사 목록(JSON: `{"클립id": "대사"}`)을 받아서 `index.html`의 `window.CLIPS`에 넣을 수 있는 형식으로 만들어요.
녹음(data URI), 단어 시간(`words`), 입 모양 키(`keys`), 음량(`env`)이 들어 있어요.

필요한 것 (앱에는 들어가지 않고, 목소리를 만들 때만 씀):
- Python 패키지: `kokoro-onnx`, `soundfile`, `vosk`, `numpy`
- Kokoro 모델(`model_q8.onnx`)과 목소리 파일(`voices.npz`): npm 패키지 `kokoro-q8-shards`, `kokoro-local-runtime`의 `voices/*.bin`
- 단어 시간 맞추기용 Vosk 모델: `vosk/vosk-model-small-en-us-0.15.tar.gz` (앱에 있는 것)
- `ffmpeg`

```
python make_clip.py <작업폴더> lines.json   # → <작업폴더>/clips/clips.json
```
작업폴더 안에 `kok/model_q8.onnx`, `kok/voices.npz`, `vmodel/`(Vosk 모델 압축 푼 것)가 있어야 해요.
