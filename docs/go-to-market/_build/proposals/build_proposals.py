"""Rebuild the FluxMuse proposal templates (Word) into docs/go-to-market/03_Proposal_Templates/.

Usage (python-docx + Pillow required):
    python docs/go-to-market/_build/proposals/build_proposals.py
Then run qa_proposals.py (structure + forbidden-claims checks) and, optionally, preview_proposals.py.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from solo import build_solo  # noqa: E402
from sme import build_sme  # noqa: E402
from agency import build_agency  # noqa: E402
from campaign import build_campaign  # noqa: E402
from fmdoc import GTM, ASSETS  # noqa: E402

OUT = GTM / "03_Proposal_Templates"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    marker = ASSETS / ".revision-v3-done"
    jobs = [
        ("FluxMuse_Proposal_Solo_Entrepreneur.docx", lambda p: build_solo(p)),
        ("FluxMuse_Proposal_SME_Growth.docx", build_sme),
        ("FluxMuse_Proposal_Agency_Partner.docx", build_agency),
        ("FluxMuse_Proposal_Brand_Campaign.docx", build_campaign),
        ("FluxMuse_Proposal_Sample_Braiding_Studio.docx", lambda p: build_solo(p, sample=True)),
    ]
    manifest = {"assets_revision_v3_marker": marker.exists(), "files": {}}
    for name, fn in jobs:
        d = fn(OUT / name)
        manifest["files"][name] = sorted(set(d.images_used))
        print(f"built {name}: {len(d.images_used)} figures")
    (HERE / "build_manifest.json").write_text(json.dumps(manifest, indent=2))
    print("v3 asset marker present:", marker.exists())


if __name__ == "__main__":
    main()
