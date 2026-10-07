import json
import os
import time

import pandas as pd
import requests

BASE_URL = "https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/annonces-commerciales/records"
FICHIER_FINAL = "Data/raw/bodacc.parquet"
DOSSIER_TRANCHES = "Data/raw/tranches"
CHECKPOINT_FILE = "Data/raw/bodacc_checkpoint.json"
os.makedirs(DOSSIER_TRANCHES, exist_ok=True)

if os.path.exists(FICHIER_FINAL):
    print(
        "✓ Fichier final déjà présent. Supprime-le pour forcer un nouveau téléchargement."
    )
    exit()

# Génération automatique des tranches hebdomadaires 2020 → août 2026
tranches = []
semaines = pd.date_range(start="2020-01-01", end="2026-08-28", freq="W-MON")
for debut in semaines:
    fin = debut + pd.Timedelta(days=6)
    tranches.append((debut.strftime("%Y-%m-%d"), fin.strftime("%Y-%m-%d")))

# Chargement du checkpoint
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r") as f:
        checkpoint = json.load(f)
    derniere_tranche = checkpoint["derniere_tranche"]
    idx_reprise = (
        next((i for i, t in enumerate(tranches) if t[0] == derniere_tranche), 0) + 1
    )
    print(f"♻️ Reprise depuis {derniere_tranche}")
else:
    idx_reprise = 0
    print("🆕 Démarrage from scratch")


def fetch_tranche(date_debut, date_fin):
    records = []
    offset = 0
    while True:
        params = {
            "where": f"familleavis_lib='Procédures collectives' AND dateparution >= '{date_debut}' AND dateparution <= '{date_fin}'",
            "order_by": "dateparution asc",
            "limit": 100,
            "offset": offset,
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"  Erreur {response.status_code} à offset {offset}")
            break
        data = response.json()
        batch = data.get("results", [])
        if not batch:
            break
        records.extend(batch)
        offset += 100
        time.sleep(0.2)
    return records


def extraire_rows(records):
    rows = []
    for record in records:
        registre = record.get("registre", [])
        siren = registre[0].replace(" ", "") if registre else None
        jugement_raw = record.get("jugement", None)
        jugement = json.loads(jugement_raw) if jugement_raw else {}
        rows.append(
            {
                "siren": siren,
                "date_parution": record.get("dateparution"),
                "type_procedure": record.get("familleavis_lib"),
                "nature_jugement": jugement.get("nature", None),
                "date_jugement": jugement.get("date", None),
                "denomination": record.get("commercant", None),
                "departement": record.get("numerodepartement", None),
                "ville": record.get("ville", None),
                "tribunal": record.get("tribunal", None),
            }
        )
    return rows


# Boucle principale
for date_debut, date_fin in tranches[idx_reprise:]:
    fichier_tranche = os.path.join(DOSSIER_TRANCHES, f"{date_debut}.parquet")

    # Si la tranche existe déjà sur disque, on saute
    if os.path.exists(fichier_tranche):
        print(f"⏭️ Déjà téléchargé : {date_debut}")
        continue

    print(f"Téléchargement {date_debut} → {date_fin}...", end=" ")
    batch = fetch_tranche(date_debut, date_fin)

    if batch:
        rows = extraire_rows(batch)
        df_tranche = pd.DataFrame(rows)
        df_tranche.to_parquet(fichier_tranche, index=False)

    print(f"{len(batch)} annonces")

    # Checkpoint léger : juste la date
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"derniere_tranche": date_debut}, f)

    time.sleep(0.5)

# Concaténation finale
print("\n🔗 Concaténation des tranches...")
fichiers = sorted(
    [
        os.path.join(DOSSIER_TRANCHES, f)
        for f in os.listdir(DOSSIER_TRANCHES)
        if f.endswith(".parquet")
    ]
)
df_bodacc = pd.concat([pd.read_parquet(f) for f in fichiers], ignore_index=True)
df_bodacc.to_parquet(FICHIER_FINAL, index=False)
print(f"✓ Fichier final sauvegardé : {FICHIER_FINAL} ({len(df_bodacc):,} lignes)")

# Nettoyage
os.remove(CHECKPOINT_FILE)
print("✓ Checkpoint supprimé")
