import os

import pandas as pd
import requests

# ── 1. URL stable du fichier Parquet Sirene ───────────────────────────────────
URL_SIRENE = (
    "https://www.data.gouv.fr/api/1/datasets/r/350182c9-148a-46e0-8389-76c2ec1374a3"
)
FICHIER_LOCAL = "Data/raw/sirene.parquet"

# ── 2. Téléchargement ────────────────────────────────────────────────────────
os.makedirs("Data/raw", exist_ok=True)

if not os.path.exists(FICHIER_LOCAL):
    print("Téléchargement du fichier Sirene (~672 Mo)...")
    with requests.get(URL_SIRENE, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(FICHIER_LOCAL, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r  {pct:.1f}%", end="", flush=True)
    print(f"\n✓ Fichier téléchargé : {FICHIER_LOCAL}")
else:
    print(f"Fichier déjà présent : {FICHIER_LOCAL}")

# ── 3. Vérification brute ────────────────────────────────────────────────────
print("Lecture du fichier Parquet...")
df_sirene = pd.read_parquet(FICHIER_LOCAL)
print(f"Lignes : {len(df_sirene):,}")
print(f"Colonnes : {list(df_sirene.columns)}")
print(df_sirene.head(3))
