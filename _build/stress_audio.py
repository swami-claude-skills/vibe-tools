#!/usr/bin/env python3
"""stress_audio.py — run the vibe-dashboard audio_overview.py with exact-pronunciation markup and a noun/verb
stress audit.  Usage:
  python3 stress_audio.py SKILL_DIR audit NARRATION.txt
  python3 stress_audio.py SKILL_DIR build PAGE.html NARRATION.txt OUT.html [--trigger ..] [--artifact ..]
  python3 stress_audio.py SKILL_DIR plain NARRATION.txt OUT.txt     (markup -> plain words, for the browser-voice player)
Markup in the narration: [word](/phonemes/) speaks exactly those Kokoro phonemes, e.g. [records](/ɹᵻkˈɔːɹdz/).
"""
import os, re, sys
SKILL = sys.argv[1]; sys.path.insert(0, os.path.join(SKILL, 'scripts'))
import audio_overview as ao
MARK = re.compile(r'\[([^\]]+)\]\(/([^/]+)/\)')
# two-syllable words whose stress moves: noun/adjective = 1st syllable, verb = 2nd syllable
STRESS = ('record object project permit conduct contest convert produce progress subject increase decrease export import '
          'insert protest contract conflict refuse rebel combat compound console content convict desert extract perfect '
          'reject survey update upgrade upload download transfer transport discount escort torment suspect address '
          'research default digest present impact implant intern invite misprint object perfume prefix proceeds '
          'segment torment upset construct consort convoy decrease discharge exploit finance incline insult '
          'outlaw permit rebound recall redo refill refund rehash relay remake replay reprint reset retake '
          'retread rewind rewrite').split()
STEMS = sorted(set(STRESS), key=len, reverse=True)
WORD = re.compile(r'\b(' + '|'.join(STEMS) + r')(s|es|ed|ing|d)?\b', re.I)

def _tts():
    ao._ensure_tts()
    from kokoro_onnx import Kokoro
    return Kokoro(os.path.join(ao.CACHE, 'kokoro.onnx'), os.path.join(ao.CACHE, 'voices.bin'))

def _vowel_stress(ph):
    """which vowel group carries the primary stress: 1, 2 … (0 if none)"""
    groups = re.findall(r'[ˈˌ]?[ɑɐæʌɔəɚɛɜɪiɨʊuoeaᵻɒ][ːɑɐæʌɔəɚɛɜɪiɨʊuoeaᵻɒ]*', ph)
    for n, g in enumerate(groups, 1):
        if g.startswith('ˈ'): return n
    return 0

def audit(path):
    k = _tts(); txt = open(path, encoding='utf8').read()
    marked = [(m.group(1), m.group(2)) for m in MARK.finditer(txt)]
    plain = MARK.sub(lambda m: m.group(1), txt); hits = 0
    for sent in re.split(r'(?<=[.!?])\s+', plain):
        words = sent.split(); ph = k.tokenizer.phonemize(sent, 'en-us').split()
        for m in WORD.finditer(sent):
            hits += 1
            i = len(sent[:m.start()].split())
            p = ph[i] if i < len(ph) and len(ph) == len(words) else k.tokenizer.phonemize(m.group(0), 'en-us')
            fix = next((ph2 for w2, ph2 in marked if w2.lower() == m.group(0).lower()), None)
            if fix: p = fix + ' (marked)'
            st = _vowel_stress(p)
            print(f'{m.group(0):12} said {p:16} stress on syllable {st or "?"}  ←  {sent.strip()[:110]}')
    print(f'{hits} noun/verb stress word(s) found. Noun or adjective → syllable 1; verb → syllable 2. '
          'Fix any wrong one with [word](/phonemes/).')

def speak(text, mp3_path):
    """audio_overview.speak with [word](/phonemes/) support (paragraphs without markup are spoken exactly as before)"""
    if not MARK.search(text): return _orig(text, mp3_path)
    k = _tts(); import numpy as np, soundfile as sf, subprocess, tempfile
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    parts, sr = [], 24000
    for p in paras:
        p = ' '.join(p.split())
        if MARK.search(p):
            out, last = [], 0
            for m in MARK.finditer(p):
                if p[last:m.start()].strip(): out.append(k.tokenizer.phonemize(p[last:m.start()], 'en-us'))
                out.append(m.group(2)); last = m.end()
            if p[last:].strip(): out.append(k.tokenizer.phonemize(p[last:], 'en-us'))
            s, sr = k.create(' '.join(o.strip() for o in out), voice=ao.VOICE, speed=1.0, lang='en-us', is_phonemes=True)
        else:
            s, sr = k.create(p, voice=ao.VOICE, speed=1.0, lang='en-us')
        parts += [s, np.zeros(int(sr * 0.55), dtype=s.dtype)]
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, 'a.wav'); sf.write(wav, np.concatenate(parts), sr)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-b:a', '64k', mp3_path], check=True)
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3_path],
                         capture_output=True, text=True).stdout.strip()
    return float(dur or 0)
_orig, ao.speak = ao.speak, speak

cmd, args = sys.argv[2], sys.argv[3:]
if cmd == 'audit': audit(args[0])
elif cmd == 'plain': open(args[1], 'w', encoding='utf8').write(MARK.sub(lambda m: m.group(1), open(args[0], encoding='utf8').read()))
elif cmd == 'build':
    trig = art = None
    if '--trigger' in args: trig = args[args.index('--trigger') + 1]
    if '--artifact' in args: art = args[args.index('--artifact') + 1]
    ao.build(args[0], args[1], args[2], trig, art)
else: sys.exit(__doc__)
