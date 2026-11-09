"""Search-engine and social-sharing tags for every page, plus sitemap.xml.

Adds (or refreshes) in each page's <head>, between <!-- SEO:start --> and <!-- SEO:end -->:
meta description, canonical URL, FR/EN alternates (hreflang), Open Graph / Twitter tags and,
on some pages, schema.org structured data. Also makes the page title an <h1>.

Run from the repository root after apply_layout.py:

    python3 tools/apply_seo.py
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://chopinconcours.github.io/site-concours-chopin/"
IMAGE = BASE + "assets/img/og-image.jpg"
LINKEDIN = "https://www.linkedin.com/company/concours-chopin-epfl-unil/"

# French file -> (French description, English description). English file = same name with -en.
DESCRIPTIONS = {
    "index.html": (
        "Concours de piano Chopin pour les étudiants et alumni de l'UNIL/EPFL, de l'UZH/ETH et de l'UNIGE : inscriptions 2026-2027, concerts, photos et partenaires.",
        "Chopin piano competition for students and alumni of UNIL/EPFL, UZH/ETH and UNIGE: 2026-2027 registration, concerts, photos and partners."),
    "concours-2026-2027.html": (
        "Concours Chopin Étudiant 2026-2027 : règlement, dates (inscription jusqu'au 30 novembre 2026, Grande Finale le 24 mai 2027 à Lausanne) et inscription.",
        "Student Chopin Competition 2026-2027: rules, dates (registration until 30 November 2026, Grand Final on 24 May 2027 in Lausanne) and registration."),
    "alumni.html": (
        "Édition Alumni 2027 du Concours Chopin pour les anciens de l'UNIL/EPFL, de l'UZH/ETH et de l'UNIGE : règlement, vidéo avant le 30 septembre 2027.",
        "Chopin Competition Alumni Edition 2027 for alumni of UNIL/EPFL, UZH/ETH and UNIGE: rules, video by 30 September 2027, registration."),
    "prestations.html": (
        "L'association Concours Chopin Étudiant EPFL-UNIL : mission, résultats de l'édition 2025, concerts gratuits sur les campus et partenariats.",
        "The Student Chopin Competition EPFL-UNIL association: mission, 2025 results, free campus concerts and partnerships."),
    "calendrier.html": (
        "Calendrier du Concours Chopin Étudiant : dates clés 2026-2027, concerts et échéances du concours.",
        "Student Chopin Competition calendar: key dates 2026-2027, concerts and competition deadlines."),
    "newsletter.html": (
        "Inscrivez-vous à la newsletter du Concours Chopin Étudiant : concerts, évènements et actualités du concours.",
        "Sign up for the Student Chopin Competition newsletter: concerts, events and competition news."),
    "equipe.html": (
        "Le comité et les partenaires du Concours Chopin Étudiant : Société Frédéric Chopin Genève, Lavaux Classic, HEMU, Klavierhaus et d'autres.",
        "The committee and partners of the Student Chopin Competition: Société Frédéric Chopin Genève, Lavaux Classic, HEMU, Klavierhaus and more."),
    "contact.html": (
        "Contactez le Concours Chopin Étudiant EPFL-UNIL : questions, partenariats, sponsoring. chopin.concours@gmail.com",
        "Contact the Student Chopin Competition EPFL-UNIL: questions, partnerships, sponsorship. chopin.concours@gmail.com"),
}

ORGANIZATION = {
    "@type": "Organization",
    "name": "Concours Chopin Étudiant EPFL-UNIL",
    "alternateName": "Student Chopin Competition",
    "url": BASE,
    "logo": BASE + "assets/img/team/logo_CC.png",
    "email": "chopin.concours@gmail.com",
    "sameAs": [LINKEDIN],
}


def url_of(name: str) -> str:
    return BASE if name == "index.html" else BASE + name


def en_name(fr: str) -> str:
    return fr.replace(".html", "-en.html")


def structured_data(fr: str, lang: str) -> list:
    if fr == "index.html":
        return [dict({"@context": "https://schema.org"}, **ORGANIZATION)]
    if fr == "concours-2026-2027.html":
        page = fr if lang == "fr" else en_name(fr)
        return [{
            "@context": "https://schema.org",
            "@type": "Event",
            "name": "Grande Finale du Concours Chopin Étudiant 2026-2027" if lang == "fr"
                    else "Student Chopin Competition 2026-2027 Grand Final",
            "startDate": "2027-05-24",
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {"@type": "Place", "name": "Lausanne",
                         "address": {"@type": "PostalAddress", "addressLocality": "Lausanne", "addressCountry": "CH"}},
            "image": [IMAGE],
            "description": DESCRIPTIONS[fr][0 if lang == "fr" else 1],
            "organizer": ORGANIZATION,
            "url": url_of(page),
        }]
    return []


def seo_block(fr: str, lang: str, title: str) -> str:
    en = en_name(fr)
    page = fr if lang == "fr" else en
    desc = DESCRIPTIONS[fr][0 if lang == "fr" else 1]
    esc = lambda s: s.replace("&", "&amp;").replace('"', "&quot;")
    lines = [
        "<!-- SEO:start (generated by tools/apply_seo.py) -->",
        f'<meta name="description" content="{esc(desc)}" />',
        f'<link rel="canonical" href="{url_of(page)}" />',
        f'<link rel="alternate" hreflang="fr" href="{url_of(fr)}" />',
        f'<link rel="alternate" hreflang="en" href="{url_of(en)}" />',
        f'<link rel="alternate" hreflang="x-default" href="{url_of(fr)}" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="Concours Chopin Étudiant" />',
        f'<meta property="og:title" content="{esc(title)}" />',
        f'<meta property="og:description" content="{esc(desc)}" />',
        f'<meta property="og:url" content="{url_of(page)}" />',
        f'<meta property="og:image" content="{IMAGE}" />',
        '<meta property="og:image:width" content="1200" />',
        '<meta property="og:image:height" content="630" />',
        f'<meta property="og:locale" content="{"fr_CH" if lang == "fr" else "en_GB"}" />',
        '<meta name="twitter:card" content="summary_large_image" />',
    ]
    for data in structured_data(fr, lang):
        lines.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>")
    lines.append("<!-- SEO:end -->")
    return "\n  ".join(lines)


def apply(path: Path, fr: str, lang: str) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"\s*<!-- SEO:start.*?<!-- SEO:end -->", "", html, flags=re.S)
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
    html = html.replace("</title>", "</title>\n  " + seo_block(fr, lang, title), 1)
    # Page title as <h1> (same look: .h2 keeps the previous size)
    html = re.sub(r'<h2 class="section-heading text-uppercase">(.*?)</h2>',
                  r'<h1 class="section-heading text-uppercase h2">\1</h1>', html, count=1, flags=re.S)
    html = re.sub(r'<div class="masthead-heading text-uppercase">(.*?)</div>',
                  r'<h1 class="masthead-heading text-uppercase">\1</h1>', html, count=1, flags=re.S)
    path.write_text(html, encoding="utf-8")


def sitemap() -> None:
    today = date.today().isoformat()
    entries = []
    for fr in DESCRIPTIONS:
        for page in (fr, en_name(fr)):
            entries.append(
                "  <url>\n"
                f"    <loc>{url_of(page)}</loc>\n"
                f"    <lastmod>{today}</lastmod>\n"
                f'    <xhtml:link rel="alternate" hreflang="fr" href="{url_of(fr)}" />\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{url_of(en_name(fr))}" />\n'
                "  </url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries) + "\n</urlset>\n", encoding="utf-8")


def main() -> None:
    for fr in DESCRIPTIONS:
        for lang, name in (("fr", fr), ("en", en_name(fr))):
            apply(ROOT / name, fr, lang)
            print("updated", name)
    sitemap()
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
