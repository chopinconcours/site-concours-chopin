"""Apply the shared navigation bar, footer, <html lang> and <title> to every page.

Each page keeps its own body content; only the blocks below are rewritten.
Run from the repository root after adding or renaming a page:

    python3 tools/apply_layout.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (French file, English file, French title, English title)
PAGES = [
    ("index.html", "index-en.html", "Accueil - Concours Chopin Étudiant", "Home - Student Chopin Competition"),
    ("concours-2026-2027.html", "concours-2026-2027-en.html", "Concours 2026-2027 - Concours Chopin Étudiant", "Competition 2026-2027 - Student Chopin Competition"),
    ("alumni.html", "alumni-en.html", "Édition Alumni 2027 - Concours Chopin Étudiant", "Alumni Edition 2027 - Student Chopin Competition"),
    ("prestations.html", "prestations-en.html", "Association - Concours Chopin Étudiant", "Association - Student Chopin Competition"),
    ("calendrier.html", "calendrier-en.html", "Calendrier - Concours Chopin Étudiant", "Calendar - Student Chopin Competition"),
    ("newsletter.html", "newsletter-en.html", "Newsletter - Concours Chopin Étudiant", "Newsletter - Student Chopin Competition"),
    ("equipe.html", "equipe-en.html", "Équipe & Partenaires - Concours Chopin Étudiant", "Team & Partners - Student Chopin Competition"),
    ("contact.html", "contact-en.html", "Contact - Concours Chopin Étudiant", "Contact - Student Chopin Competition"),
]

LABELS = {
    "fr": {
        "index": "Accueil", "concours-2026-2027": "Concours 2026-2027", "alumni": "Alumni 2027",
        "prestations": "Association", "calendrier": "Calendrier", "more": "Infos",
        "newsletter": "Newsletter", "equipe": "Équipe & Partenaires", "contact": "Contact",
        "partners": "Nos partenaires", "rights": "© Concours Chopin Étudiant EPFL-UNIL 2026",
    },
    "en": {
        "index": "Home", "concours-2026-2027": "Competition 2026-2027", "alumni": "Alumni 2027",
        "prestations": "Association", "calendrier": "Calendar", "more": "More",
        "newsletter": "Newsletter", "equipe": "Team & Partners", "contact": "Contact",
        "partners": "Our partners", "rights": "© Student Chopin Competition EPFL-UNIL 2026",
    },
}


def href(base: str, lang: str) -> str:
    return f"{base}.html" if lang == "fr" else f"{base}-en.html"


def nav(lang: str, fr_file: str, en_file: str) -> str:
    L = LABELS[lang]
    item = lambda b: f'          <li class="nav-item"><a class="nav-link" href="{href(b, lang)}">{L[b]}</a></li>'
    return f"""<nav class="navbar navbar-expand-lg navbar-dark fixed-top" id="mainNav">
    <div class="container">
      <a class="navbar-brand" href="{href('index', lang)}">
        <img src="assets/img/team/logo_CC.png" alt="{L['index']}" style="height: 80px;" />
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive"
        aria-controls="navbarResponsive" aria-expanded="false" aria-label="Menu">
        Menu <i class="fas fa-bars ms-1"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav text-uppercase ms-auto py-4 py-lg-0">
{item('index')}
{item("concours-2026-2027")}
{item('alumni')}
{item('prestations')}
{item('calendrier')}
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownInfos" role="button"
              data-bs-toggle="dropdown" aria-expanded="false">{L['more']}</a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownInfos">
              <li><a class="dropdown-item" href="{href('newsletter', lang)}">{L['newsletter']}</a></li>
              <li><a class="dropdown-item" href="{href('equipe', lang)}">{L['equipe']}</a></li>
            </ul>
          </li>
{item('contact')}
          <li class="nav-item d-flex align-items-center">
            <a class="nav-link" href="{fr_file}" lang="fr" style="padding-right: 5px;">FR</a>
            <span class="nav-link px-0">|</span>
            <a class="nav-link" href="{en_file}" lang="en" style="padding-left: 5px;">EN</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>"""


def footer(lang: str) -> str:
    L = LABELS[lang]
    return f"""<footer class="footer py-4 bg-light">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 d-flex align-items-center justify-content-center justify-content-md-start">
          <a href="{href('equipe', lang)}" class="text-decoration-none">{L['partners']}</a>
          <a class="btn btn-dark btn-social mx-3" href="https://www.linkedin.com/company/concours-chopin-epfl-unil/"
            target="_blank" rel="noopener" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
          <a href="mailto:chopin.concours@gmail.com" class="text-decoration-none">chopin.concours@gmail.com</a>
        </div>
        <div class="col-md-6 text-center text-md-end mt-3 mt-md-0">
          <span>{L['rights']}</span>
        </div>
      </div>
    </div>
  </footer>"""


def apply(path: Path, lang: str, title: str, fr_file: str, en_file: str) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'<html lang="[^"]*">', f'<html lang="{lang}">', html, count=1)
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html, n_nav = re.subn(r"<nav\b.*?</nav>", nav(lang, fr_file, en_file), html, count=1, flags=re.S)
    html, n_foot = re.subn(r"<footer\b.*?</footer>", footer(lang), html, count=1, flags=re.S)
    if not (n_nav and n_foot):
        raise SystemExit(f"{path.name}: nav or footer block not found")
    path.write_text(html, encoding="utf-8")


def main() -> None:
    for fr_file, en_file, fr_title, en_title in PAGES:
        for lang, name, title in (("fr", fr_file, fr_title), ("en", en_file, en_title)):
            p = ROOT / name
            if p.exists():
                apply(p, lang, title, fr_file, en_file)
                print("updated", name)
            else:
                print("MISSING", name)


if __name__ == "__main__":
    main()
