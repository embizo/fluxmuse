"""Assembles the avatar-test videos (formats A, B, C) with ffmpeg.

Takes the raw media (infographics or product images, voiceover clips, talking-
head clips from the Colab notebook or selfie clips) and produces a vertical
1080x1920 H.264 MP4 with burned-in captions and, for format A, the
"AI presenter" label for the whole video.

Every format uses the same four beats from FluxMuse_Dry_Run.md:
hook -> proof -> offer -> cta. A beat's length is its voiceover's length when
audio is given, otherwise a reading-time default (a silent draft).

Usage (FluxMuse dry run defaults):
    python3 docs/go-to-market/_build/avatar_test/assemble_video.py B
    python3 docs/go-to-market/_build/avatar_test/assemble_video.py A --audio DIR --clips DIR
    python3 docs/go-to-market/_build/avatar_test/assemble_video.py C --clips DIR   (selfie_hook.mp4, selfie_cta.mp4)

--audio DIR: en_*_{hook,proof,offer,cta}.wav from the Colab notebook.
--clips DIR: formatA_{hook,cta}.mp4 (A) or selfie_{hook,cta}.mp4 (C).
Needs imageio-ffmpeg (pip install imageio-ffmpeg); Poppins and Inter installed for the captions.
"""
import argparse
import glob
import os
import subprocess
import tempfile

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
GTM = os.path.normpath(os.path.join(HERE, "../.."))
OUT_DIR = os.path.join(GTM, "08_Flux_Loop/Avatar_Test_Run/dry_run_output")
IG = os.path.join(GTM, "assets/infographics")
W, H, FPS = 1080, 1920, 30
NIGHT = "0x0F1419"

# The dry-run script (FluxMuse_Dry_Run.md). On-screen captions stay short; the voice carries the detail.
BEATS = [
    ("hook", "how-fluxmuse-works_square_dark.png", 4.0, "Still answering DMs at 11pm?"),
    ("proof", "whatsapp-commerce-flow_square_dark.png", 12.0,
     "Send your product photos on WhatsApp\\Nget a shop link back\\N\\NReplies in your customers' language\\NAn alert for every order"),
    ("offer", "founding-member-offer_square.png", 5.0, "From R149 a month\\N30% off your first two months\\N(South African sign-ups)"),
    ("cta", "how-fluxmuse-works_square_dark.png", 4.0, "Tap the link and say hi\\NThabo sets you up himself"),
]
TALKING = {"hook", "cta"}  # beats where formats A and C show a face


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r


def duration(path):
    r = subprocess.run([FF, "-i", path], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise SystemExit(f"no duration for {path}")


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def captions(path, spans, label):
    """ASS subtitles: the hook big and high, the rest as a lower block; optional fixed corner label."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Poppins,88,&H00FFFFFF,&H00FFFFFF,&H00191410,&H96191410,1,0,0,0,100,100,0,0,3,18,0,8,70,70,170,1
Style: Body,Inter,54,&H00FFFFFF,&H00FFFFFF,&H00191410,&H96191410,1,0,0,0,100,100,0,0,3,16,0,2,70,70,190,1
Style: Label,Inter,34,&H0000005A,&H0000005A,&H00006AFF,&H00006AFF,1,0,0,0,100,100,0,0,3,10,0,9,40,40,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for (name, start, end, text) in spans:
        style = "Hook" if name == "hook" else "Body"
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}")
    if label:
        total = spans[-1][2]
        lines.append(f"Dialogue: 1,{ass_time(0)},{ass_time(total)},Label,,0,0,0,,AI presenter")
    with open(path, "w") as f:
        f.write(head + "\n".join(lines) + "\n")


def image_segment(img, secs, out):
    """A square infographic on Night, scaled to the frame width, with a slow push-in."""
    frames = max(1, int(round(secs * FPS)))
    vf = (f"scale={W * 2}:-1,zoompan=z='min(zoom+0.0006,1.08)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":s={W}x{W}:fps={FPS},pad={W}:{H}:0:(oh-ih)/2-120:color={NIGHT},format=yuv420p")
    run([FF, "-y", "-loop", "1", "-i", img, "-vf", vf, "-t", f"{secs:.3f}", "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-an", out])


def clip_segment(clip, secs, out):
    """A talking-head or selfie clip, cropped to fill 9:16, trimmed or held to the beat length."""
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
          f"tpad=stop_mode=clone:stop_duration=30,format=yuv420p")
    run([FF, "-y", "-i", clip, "-vf", vf, "-t", f"{secs:.3f}", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "20", "-an", out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("format", choices=["A", "B", "C"])
    ap.add_argument("--audio", help="dir with en_*_{hook,proof,offer,cta}.wav")
    ap.add_argument("--clips", help="dir with formatA_{hook,cta}.mp4 or selfie_{hook,cta}.mp4")
    ap.add_argument("--out", help="output mp4")
    a = ap.parse_args()

    if a.format in "AC" and not a.clips:
        raise SystemExit(f"format {a.format} needs --clips (the {'avatar' if a.format == 'A' else 'selfie'} hook and cta clips)")
    audio = {}
    if a.audio:
        for name, *_ in BEATS:
            hits = sorted(glob.glob(os.path.join(a.audio, f"en_*_{name}.wav")))
            if hits:
                audio[name] = hits[0]
    prefix = "formatA" if a.format == "A" else "selfie"

    os.makedirs(OUT_DIR, exist_ok=True)
    draft = "" if len(audio) == len(BEATS) else "_DRAFT_no_voice"
    out = a.out or os.path.join(OUT_DIR, f"AV00{a.format}{draft}.mp4")

    with tempfile.TemporaryDirectory() as tmp:
        segs, spans, t = [], [], 0.0
        for name, img, default, text in BEATS:
            secs = duration(audio[name]) + 0.25 if name in audio else default
            seg = os.path.join(tmp, f"{name}.mp4")
            if a.format in "AC" and name in TALKING:
                clip_segment(os.path.join(a.clips, f"{prefix}_{name}.mp4"), secs, seg)
            else:
                image_segment(os.path.join(IG, img), secs, seg)
            segs.append(seg)
            spans.append((name, t, t + secs, text))
            t += secs

        listfile = os.path.join(tmp, "list.txt")
        with open(listfile, "w") as f:
            f.writelines(f"file '{s}'\n" for s in segs)
        joined = os.path.join(tmp, "joined.mp4")
        run([FF, "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", joined])

        ass = os.path.join(tmp, "captions.ass")
        captions(ass, spans, label=(a.format == "A"))

        cmd = [FF, "-y", "-i", joined]
        if audio:
            # Each beat's voice starts at its beat; beats without audio stay silent.
            for name, *_ in BEATS:
                if name in audio:
                    cmd += ["-i", audio[name]]
            delays, idx = [], 1
            for (name, start, _, _) in spans:
                if name in audio:
                    ms = int(start * 1000)
                    delays.append(f"[{idx}:a]adelay={ms}|{ms}[a{idx}]")
                    idx += 1
            mix = ";".join(delays) + ";" + "".join(f"[a{i}]" for i in range(1, idx)) + f"amix=inputs={idx - 1}:normalize=0[aout]"
            cmd += ["-filter_complex", f"[0:v]ass={ass}[v];{mix}", "-map", "[v]", "-map", "[aout]",
                    "-c:a", "aac", "-b:a", "160k"]
        else:
            cmd += ["-vf", f"ass={ass}", "-an"]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", "-t", f"{t:.3f}", out]
        run(cmd)
    print(f"wrote {out} ({t:.1f}s{', no voice: timing draft only' if draft else ''})")


if __name__ == "__main__":
    main()
