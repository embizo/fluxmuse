"""Builds docs/go-to-market/08_Flux_Loop/Avatar_Test_Run/FluxMuse_Avatar_Test_Colab.ipynb.

An open-source, free-GPU (Colab T4) way to make the media for the avatar test
dry run: avatar images, voices and talking-head clips. Editing (captions,
pans, the "AI presenter" label) happens afterwards with ffmpeg.

Usage:
    python3 docs/go-to-market/_build/avatar_test/build_colab_notebook.py
"""
import ast
import os

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "../../08_Flux_Loop/Avatar_Test_Run/FluxMuse_Avatar_Test_Colab.ipynb"))

md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
cells = []

cells.append(md("""# FluxMuse avatar test: open-source media on a free Colab GPU

Makes the raw media for the **FluxMuse dry run** (`FluxMuse_Dry_Run.md`) with open-source models, so no paid tool is needed:

| Step | Model | Licence (check before publishing) | Publishable? |
|---|---|---|---|
| 1. Avatar images | Stable Diffusion XL base 1.0 (default, fits a free T4) or FLUX.1 [schnell] (needs an L4/A100) | CreativeML Open RAIL++-M / Apache 2.0 | Yes, within the licence's use restrictions |
| 2a. English voice | Kokoro-82M | Apache 2.0 | Yes |
| 2b. isiZulu / Sesotho voice **check** | Meta MMS-TTS | CC-BY-NC 4.0 (**non-commercial**) | **No.** For the internal voice check only |
| 3. Talking clips (format A) | SadTalker | Apache 2.0 (its downloaded face models carry their own licences: check them) | Only if every model it downloads allows commercial use |

**Not run before shipping.** This notebook was written without a GPU, so treat the first run as a test. Each step says what to do if it fails.

**How to use it**
1. *Runtime → Change runtime type → T4 GPU* (free). An L4 or A100 is faster and lets you use FLUX.
2. Run the cells top to bottom. Steps 1–3 are independent: re-run any one without the others.
3. The last cell zips `/content/fluxmuse_avatar_test/` (images, audio, clips and `manifest.json`). Upload the zip to the Claude session, which assembles formats A, B and C with captions and the "AI presenter" label.

**Rules carried over from the test kit**
- Avatars face the camera, mouth closed, chest up, even light, no logos or text. **Don't match a face to an industry.**
- Reverse-image-search each avatar you keep, so it doesn't closely resemble a real person.
- The presenter speaks *as the brand's presenter*, never as a customer.
- Every attempt goes in the production log, including failures. `manifest.json` records model, prompt, seed and timings to make that easy.
"""))

cells.append(md("## 0. Setup"))
cells.append(code("""# Check the GPU and install the shared libraries (about 2 minutes).
!nvidia-smi --query-gpu=name,memory.total --format=csv || echo "No GPU: set Runtime > Change runtime type > T4 GPU"
!pip -q install -U diffusers transformers accelerate safetensors soundfile "kokoro>=0.9.4" misaki[en]
!apt-get -qq install -y espeak-ng ffmpeg > /dev/null"""))
cells.append(code("""import json, os, time, random
import torch

OUT = "/content/fluxmuse_avatar_test"
for d in ("avatars", "audio", "clips"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

MANIFEST_PATH = f"{OUT}/manifest.json"
manifest = json.load(open(MANIFEST_PATH)) if os.path.exists(MANIFEST_PATH) else {"items": []}

def log(kind, path, **info):
    \"\"\"One manifest row per output: what made it, how, and how long it took (for the production log).\"\"\"
    manifest["items"].append({"kind": kind, "path": os.path.relpath(path, OUT), **info,
                              "made_at": time.strftime("%Y-%m-%d %H:%M:%S")})
    json.dump(manifest, open(MANIFEST_PATH, "w"), indent=2)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
GPU = torch.cuda.get_device_name(0) if DEVICE == "cuda" else "none"
print("device:", DEVICE, "|", GPU)"""))

cells.append(md("""## 1. Avatar images

The six roster prompts from `Production_Prompts.md` §1, all ending in the shared technical suffix. Two seeds per prompt; keep the best 4–6 images overall.

- **Default:** SDXL base at 896×1152, which runs on a free T4 in about 30–60 s per image.
- **FLUX.1 [schnell]:** set `MODEL = "flux"`. It's sharper, but on a T4 it needs CPU offload and is very slow. Use an L4 or A100."""))
cells.append(code("""MODEL = "sdxl"          # "sdxl" (T4-friendly) or "flux" (L4/A100)
SEEDS = [11, 29]         # two per prompt; change to explore

SUFFIX = ("Photorealistic vertical portrait, chest-up, looking straight into the camera, relaxed natural expression, "
          "mouth gently closed, soft even daylight, shallow depth of field, plain softly blurred background, "
          "natural skin texture, no text, no logo.")
ROSTER = {
    1: "A friendly Black South African woman in her late 20s, short natural hair, plain mustard knit top, warm smile in her eyes, in a bright kitchen",
    2: "A Black South African man in his early 40s, neat beard, navy crew-neck jersey, calm and reassuring, against a softly lit shop interior",
    3: "A South African woman of mixed heritage in her mid 30s, hair tied back, denim shirt, open and practical look, in front of a plain green wall",
    4: "A young Black South African man in his early 20s, short fade, plain white T-shirt, energetic but natural, on a sunny street, background blurred",
    5: "A Black South African woman in her early 50s, headwrap, plain dark cardigan, kind and confident, in a softly lit living room",
    6: "A South African Indian man in his 30s, short hair, olive polo shirt, approachable, against a neutral studio backdrop",
}
NEGATIVE = ("text, watermark, logo, open mouth, teeth showing, extra fingers, hands near face, sunglasses, hat brim shadow, "
            "profile view, looking away, blurry face, cartoon, illustration, celebrity")"""))
cells.append(code("""from diffusers import StableDiffusionXLPipeline, FluxPipeline

t0 = time.time()
if MODEL == "flux":
    MODEL_ID = "black-forest-labs/FLUX.1-schnell"
    pipe = FluxPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16)
    pipe.enable_model_cpu_offload()  # needed below ~24 GB of GPU memory
else:
    MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
    pipe = StableDiffusionXLPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16, variant="fp16",
                                                     use_safetensors=True).to(DEVICE)
print(f"loaded {MODEL_ID} in {time.time() - t0:.0f}s")

for n, prompt in ROSTER.items():
    for seed in SEEDS:
        full = f"{prompt}. {SUFFIX}"
        g = torch.Generator(device="cpu").manual_seed(seed)
        t0 = time.time()
        if MODEL == "flux":
            img = pipe(full, height=1152, width=896, num_inference_steps=4, guidance_scale=0.0, generator=g).images[0]
        else:
            img = pipe(full, negative_prompt=NEGATIVE, height=1152, width=896, num_inference_steps=30,
                       guidance_scale=6.0, generator=g).images[0]
        path = f"{OUT}/avatars/avatar{n}_seed{seed}.png"
        img.save(path)
        log("avatar", path, avatar=n, seed=seed, model=MODEL_ID, prompt=full, gpu=GPU, seconds=round(time.time() - t0))
        print("saved", path)

del pipe
torch.cuda.empty_cache()"""))
cells.append(code("""# Contact sheet: look at every avatar, then pick the ones to keep.
from PIL import Image
from IPython.display import display
files = sorted(f for f in os.listdir(f"{OUT}/avatars") if f.endswith(".png"))
thumbs = [Image.open(f"{OUT}/avatars/{f}").resize((224, 288)) for f in files]
sheet = Image.new("RGB", (224 * 4, 288 * ((len(thumbs) + 3) // 4)), "white")
for i, t in enumerate(thumbs):
    sheet.paste(t, ((i % 4) * 224, (i // 4) * 288))
display(sheet)
print(files)"""))
cells.append(md("""**Before moving on:**
1. Keep the 4–6 best images and delete the rest from `avatars/`.
2. Note which file is the dry-run presenter. Avatar 1 is suggested.
3. Reverse-image-search each one you keep."""))

cells.append(md("""## 2. Voices

### 2a. The dry-run voiceover (English, Kokoro)
These are the script lines from `FluxMuse_Dry_Run.md`, split into the clips the edit needs. Kokoro has no South African English voice, so `bf_emma` (British) is the closest preset. Listen to several voices and note the choice."""))
cells.append(code("""import soundfile as sf
from kokoro import KPipeline

VOICE = "bf_emma"        # try also: "bf_isabella", "bm_george", "af_heart"
LINES = {
    "hook":  "Still answering DMs at eleven at night?",
    "proof": ("Send FluxMuse your product photos on WhatsApp and get a shop link back. Our assistant answers your "
              "customers in their language, day and night, and you get a WhatsApp alert for every order."),
    "offer": "It's one hundred and forty-nine rand a month. Sign up in South Africa now and your first two months are thirty percent off.",
    "cta":   "Tap the link and say hi. Thabo will set you up himself.",
}

kp = KPipeline(lang_code="b" if VOICE.startswith("b") else "a")
for name, text in LINES.items():
    t0 = time.time()
    chunks = [audio for _, _, audio in kp(text, voice=VOICE, speed=1.0)]
    audio = torch.cat([torch.as_tensor(c) for c in chunks]).numpy()
    path = f"{OUT}/audio/en_{VOICE}_{name}.wav"
    sf.write(path, audio, 24000)
    log("voice", path, model="hexgrad/Kokoro-82M", voice=VOICE, line=name, text=text,
        seconds=round(time.time() - t0), duration_s=round(len(audio) / 24000, 1))
    print(f"{path}  ({len(audio) / 24000:.1f}s)")

from IPython.display import Audio
Audio(f"{OUT}/audio/en_{VOICE}_hook.wav")"""))
cells.append(md("""Prices are written out in words ("one hundred and forty-nine rand") because text-to-speech often reads "R149" as "R one four nine". Check the brand name sounds like *FLUX-muse* every time.

### 2b. isiZulu and Sesotho voice **check** (internal only)
Meta MMS-TTS is **non-commercial** (CC-BY-NC 4.0). Use it only to give a fluent speaker something to rate on the sheet's **Voice check** tab, and **never in a published video**.

Paste translations by a fluent speaker; don't machine-translate. Leave a line empty to skip that language. If a model id fails to load, the language isn't available in MMS: record "not available"."""))
cells.append(code("""from transformers import VitsModel, AutoTokenizer

CHECK_TEXT = {
    "zul": "",   # isiZulu translation of the voice-check script (Production_Prompts.md §2), by a fluent speaker
    "sot": "",   # Sesotho translation, by a fluent speaker
}

for lang, text in CHECK_TEXT.items():
    if not text.strip():
        print(f"{lang}: no translation pasted, skipped")
        continue
    model_id = f"facebook/mms-tts-{lang}"
    try:
        tok = AutoTokenizer.from_pretrained(model_id)
        model = VitsModel.from_pretrained(model_id).to(DEVICE)
    except Exception as e:
        print(f"{lang}: {model_id} not available ({e.__class__.__name__}): record 'not available'")
        continue
    with torch.no_grad():
        wav = model(**tok(text, return_tensors="pt").to(DEVICE)).waveform[0].cpu().numpy()
    path = f"{OUT}/audio/check_mms_{lang}.wav"
    sf.write(path, wav, model.config.sampling_rate)
    log("voice_check", path, model=model_id, licence="CC-BY-NC-4.0 (internal check only)", text=text)
    print("saved", path)"""))

cells.append(md("""## 3. Talking clips (format A): SadTalker

These are the avatar's hook and call-to-action clips: one still portrait plus one audio file in, an MP4 of the face speaking out. The proof and offer lines play over product visuals instead, so they get no talking clip.

SadTalker is an older model, and its lip-sync is exactly what the test's **quality bar** is checking. Score each clip honestly on the **Videos** tab:
- lips visibly out of sync;
- distorted teeth, hands or face;
- the voice changing between the hook and the call to action.

It takes about 1–3 minutes per short clip on a T4.

**If install or inference fails:**
- An error about `torchvision.transforms.functional_tensor` is patched by the cell below. Re-run it.
- A numpy error: re-run the install cell. It pins a compatible numpy.
- Checkpoint download errors: the script fetches from GitHub releases and Hugging Face. Retry, or download the files listed in `SadTalker/scripts/download_models.sh` by hand into `SadTalker/checkpoints` and `SadTalker/gfpgan/weights`."""))
cells.append(code("""%cd /content
!test -d SadTalker || git clone -q https://github.com/OpenTalker/SadTalker.git
%cd /content/SadTalker
!pip -q install "numpy<2" face_alignment==1.3.5 imageio==2.19.3 imageio-ffmpeg librosa==0.10.1 \\
    resampy kornia==0.6.8 yacs==0.1.8 pydub safetensors basicsr facexlib gfpgan av
# basicsr imports a torchvision module that newer torchvision removed; point it at the new name.
!sed -i 's/torchvision.transforms.functional_tensor/torchvision.transforms.functional/' \\
    $(python -c "import basicsr, os; print(os.path.join(os.path.dirname(basicsr.__file__), 'data', 'degradations.py'))") || true
!test -f checkpoints/SadTalker_V0.0.2_256.safetensors || bash scripts/download_models.sh"""))
cells.append(code("""import glob, shutil, subprocess

PRESENTER = f"{OUT}/avatars/avatar1_seed11.png"   # the avatar you chose in step 1
CLIPS = {"hook": f"{OUT}/audio/en_{VOICE}_hook.wav", "cta": f"{OUT}/audio/en_{VOICE}_cta.wav"}

for name, audio_path in CLIPS.items():
    res = f"/content/sadtalker_out/{name}"
    shutil.rmtree(res, ignore_errors=True)
    t0 = time.time()
    cmd = ["python", "inference.py", "--driven_audio", audio_path, "--source_image", PRESENTER,
           "--result_dir", res, "--still", "--preprocess", "full", "--size", "512"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    mp4s = glob.glob(f"{res}/**/*.mp4", recursive=True)
    if r.returncode != 0 or not mp4s:
        print(r.stdout[-2000:], r.stderr[-3000:])
        raise RuntimeError(f"SadTalker failed on {name}: see the log above and the tips in the markdown cell")
    dest = f"{OUT}/clips/formatA_{name}.mp4"
    shutil.copy(mp4s[0], dest)
    log("talking_clip", dest, model="OpenTalker/SadTalker (256, still, full)", avatar=os.path.basename(PRESENTER),
        audio=os.path.basename(audio_path), gpu=GPU, seconds=round(time.time() - t0))
    print("saved", dest)

from IPython.display import Video
Video(f"{OUT}/clips/formatA_hook.mp4", embed=True, width=360)"""))
cells.append(md("""Optional: add `"--enhancer", "gfpgan"` to `cmd` for sharper faces. GFPGAN's code is Apache 2.0, but check its model weights' licence before publishing anything made with it, and log it in the manifest."""))

cells.append(md("""## 4. Package for editing
Zips everything with `manifest.json`. Upload the zip to the Claude session, together with:
- Thabo's two selfie clips for format C;
- the voice-check ratings from the fluent speakers."""))
cells.append(code("""manifest["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
manifest["gpu"] = GPU
json.dump(manifest, open(MANIFEST_PATH, "w"), indent=2)
shutil.make_archive("/content/fluxmuse_avatar_test", "zip", OUT)
print("/content/fluxmuse_avatar_test.zip", round(os.path.getsize("/content/fluxmuse_avatar_test.zip") / 1e6, 1), "MB")
try:
    from google.colab import files
    files.download("/content/fluxmuse_avatar_test.zip")
except ImportError:
    pass"""))

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {
    "accelerator": "GPU",
    "colab": {"provenance": [], "gpuType": "T4"},
    "kernelspec": {"name": "python3", "display_name": "Python 3"},
    "language_info": {"name": "python"},
}


def check_syntax(nb):
    """Every code cell must parse as Python once IPython-only lines (! and %) are blanked out."""
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        lines, cont = [], False
        for line in c.source.splitlines():
            shell = cont or line.lstrip().startswith(("!", "%"))
            cont = shell and line.rstrip().endswith("\\")
            lines.append("" if shell else line)
        ast.parse("\n".join(lines), filename=f"cell {i}")


check_syntax(nb)
nbf.validate(nb)
nbf.write(nb, OUT)
print("wrote", OUT, f"({len(cells)} cells, syntax + schema OK)")
