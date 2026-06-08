"""
Windows-compatible local downloader for GenoMatic1000 PMP22 target data.
No bash, wget, tabix or samtools required.

Run:
    py fetch_pmp22_ensembl_snapshot.py
or:
    python fetch_pmp22_ensembl_snapshot.py

Outputs JSON files into ./ensembl_pmp22_snapshot/
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OUT_DIR = Path("ensembl_pmp22_snapshot")
OUT_DIR.mkdir(exist_ok=True)

REQUESTS = {
    "pmp22_lookup_expand.json": "https://rest.ensembl.org/lookup/id/ENSG00000109099?expand=1;content-type=application/json",
    "pmp22_region_core_overlap.json": "https://rest.ensembl.org/overlap/region/human/17:15229773-15272292?feature=gene;feature=transcript;feature=exon;content-type=application/json",
    "pmp22_region_structural_variation_overlap.json": "https://rest.ensembl.org/overlap/region/human/17:15229773-15272292?feature=structural_variation;content-type=application/json",
}


def fetch_json(url: str, retries: int = 3, sleep_seconds: float = 1.0) -> object:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "GenoMatic1000/0.1 local PMP22 snapshot downloader",
    }
    request = Request(url, headers=headers, method="GET")

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(sleep_seconds * attempt)

    raise RuntimeError(f"Failed to fetch {url!r}: {last_error}")


def main() -> None:
    metadata = {
        "target": "PMP22 / ENSG00000109099",
        "assembly": "GRCh38/hg38",
        "region": "17:15229773-15272292",
        "source": "Ensembl REST",
        "files": [],
    }

    for filename, url in REQUESTS.items():
        print(f"Fetching: {url}")
        data = fetch_json(url)
        out_path = OUT_DIR / filename
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        metadata["files"].append({"filename": filename, "url": url})
        print(f"Saved: {out_path}")

    (OUT_DIR / "snapshot_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Done. Snapshot directory: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
