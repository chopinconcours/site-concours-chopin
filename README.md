# Site du Concours Chopin Étudiant

Site du concours Chopin étudiant EPFL/UNIL, UZH/ETH et UNIGE, publié avec GitHub Pages :
<https://chopinconcours.github.io/site-concours-chopin/> (branche `main`).

## Mettre à jour

- **Photos** : ajouter un dossier dans `assets/img/portfolio/fr/` et `assets/img/portfolio/en/`, l'inscrire dans
  le fichier `_order.txt` de chaque dossier (ordre d'affichage), puis lancer
  `python3 generate_galleries_fr.py` et `python3 generate_galleries_en.py`.
- **Menu, pied de page, titres** : modifier `tools/apply_layout.py`, puis lancer `python3 tools/apply_layout.py`.
- **Référencement (descriptions, sitemap)** : modifier `tools/apply_seo.py`, puis lancer `python3 tools/apply_seo.py`
  (toujours après `apply_layout.py`).
- **Calendrier** : voir `docs/CALENDAR.md`.
- Diagnostic du site (novembre 2026) : `docs/DIAGNOSTIC.md`.
