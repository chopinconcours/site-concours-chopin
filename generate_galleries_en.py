import os, json, time

BASE = r"assets/img/portfolio/en"   # <-- ton dossier racine

MEDIA_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', '.webm', '.ogg')

def folder_timestamp(path: str) -> float:
    """Renvoie un timestamp pour trier le dossier.
    Prend le max(mtime) des fichiers médias qu'il contient; à défaut, mtime du dossier."""
    file_times = []
    try:
        for name in os.listdir(path):
            fp = os.path.join(path, name)
            if os.path.isfile(fp) and name.lower().endswith(MEDIA_EXTS):
                try:
                    file_times.append(os.path.getmtime(fp))
                except OSError:
                    pass
    except FileNotFoundError:
        return 0.0
    if file_times:
        return max(file_times)
    # fallback: mtime du dossier (ou ctime si tu préfères sur Windows)
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0

def list_media_sorted(folder: str):
    """Liste des fichiers médias triés du plus récent au plus ancien (mtime)."""
    items = []
    for name in os.listdir(folder):
        if not name.lower().endswith(MEDIA_EXTS):
            continue
        full = os.path.join(folder, name)
        if os.path.isfile(full):
            try:
                items.append((name, os.path.getmtime(full)))
            except OSError:
                pass
    # tri descendant (plus récent d'abord)
    items.sort(key=lambda x: x[1], reverse=True)
    return [name for name, _ in items]

def main():
    # collecter les sous-dossiers
    folders = []
    for sub in os.listdir(BASE):
        full = os.path.join(BASE, sub)
        if os.path.isdir(full):
            ts = folder_timestamp(full)
            folders.append((sub, full, ts))
    # trier dossiers: plus récent -> plus ancien
    folders.sort(key=lambda x: x[2], reverse=True)

    media = {}
    order = []
    for sub, full, _ in folders:
        media[sub] = list_media_sorted(full)
        # si dossier vide, on ne l'ajoute pas
        if media[sub]:
            order.append(sub)
        else:
            # si tu veux garder aussi les vides, commente la ligne suivante
            media.pop(sub, None)

    out_path = "media2.js"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("// auto-généré: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("const mediaGalleries = ")
        json.dump(media, f, ensure_ascii=False)
        f.write(";\nconst mediaOrder = ")
        json.dump(order, f, ensure_ascii=False)
        f.write(";\n")
    print(f"Écrit {out_path} avec {len(order)} galeries.")

if __name__ == "__main__":
    main()
