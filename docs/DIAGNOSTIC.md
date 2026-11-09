# Website diagnosis – 9 November 2026

Site: <https://chopinconcours.github.io/site-concours-chopin/> (GitHub Pages, repository
`chopinconcours/site-concours-chopin`, published from the `main` branch).

## Repository state found

- The live site is the `main` branch. The local branch `gregoire` was one commit ahead
  ("prestations -> association", never merged). This work is on a new branch `site-update-2026`,
  built on `gregoire`.
- The folder `~/Downloads/Site-Concours-Chopin` (repo `gregprechac/Site-Concours-Chopin`) is an older copy
  of the site. It is not the published site.

## Problems found

| # | Severity | Problem | Status |
|---|---|---|---|
| 1 | Critical | The calendar showed `louis.elhani@gmail.com`, a **personal calendar** of the former developer (job interviews, internship meetings), publicly on the site. | Fixed: now points to `chopin.concours@gmail.com` (still needs to be made public, see `CALENDAR.md`) |
| 2 | High | Contact page showed a fake e-mail (`contact@projetpiano.com`) and phone (`+33 0 00 00 00 00`) left over from a template. | Fixed |
| 3 | High | Contact and newsletter forms sent nothing (form-service token `API_TOKEN` never set). | Fixed: forms open the visitor's mail app, pre-filled to chopin.concours@gmail.com |
| 4 | High | Team page listed invented people (Clara Dupont, Mehdi Bencheikh, Sophie Martin) with missing photos. | Replaced by the committee named in the 2025-2026 sponsoring dossier |
| 5 | High | Association page contained only placeholders (`[Texte sur l'association…]`). | Proposed texts written from the sponsoring dossier and the Drive's event forms |
| 6 | High | No page for the 2026-2027 competition or the 2027 Alumni Edition, no registration links. | Added both pages (FR + EN) with the official forms and rules |
| 7 | Medium | Only 2 partners shown (Klavierhaus, Musikplattform) out of the 10 on the official banner in the Drive. | All 10 added on the Team & Partners page |
| 8 | Medium | English pages partly in French (`lang="fr"`, French titles, "Découvrez les temps forts…", French team roles). | Fixed |
| 9 | Medium | Footer said "© Agence Piano 2025" (template leftover) on most pages. | Fixed |
| 10 | Medium | No events since November 2025 in the galleries. | Added: semi-finals March 2026, Grand Final 9 May 2026, concert 29 October 2026 |
| 11 | Medium | Gallery order depended on file dates (wrong order; photos listed backwards). | Fixed: `_order.txt` in each portfolio folder sets the order; photos sorted by name |
| 12 | Low | Mobile menu closed when tapping "Infos diverses", so its sub-pages were unreachable on phones. | Fixed in `js/scripts.js` |
| 13 | Low | Calendar time zone `Europe/Lausanne` does not exist. | Changed to `Europe/Zurich` |
| 14 | Low | Menu overflowed between 992 and 1300 px wide. | Fixed in `css/styles.css` |

## Still to do (needs a decision or an account)

1. **Make the calendar public** with the chopin.concours@gmail.com account and, ideally, create the
   association's own Google API key (steps in `docs/CALENDAR.md`). Until then the calendar shows a warning
   and only the "Key dates" list.
2. **Committee:** the names come from the 2025-2026 dossier, with no roles or photos. Update them for 2026-2027.
3. **Partner links:** only Klavierhaus has a link (the only one already on the site). Add the others' websites
   once you've confirmed them.
4. **AGEPoly:** a 2026 sponsoring contract is in the Drive, but AGEPoly is not on the official banner and
   there is no logo file, so it was not added.
5. **Form typo:** the "Concert 3rd of December" Google Form says "3rd of **October**" in its description.
6. **Large files:** two videos are 36 MB each (`8 novembre 2025, finale Lavaux Classic.`), and every
   gallery file is stored twice (`portfolio/fr` and `portfolio/en`, 114 MB in total). Consider hosting videos
   on YouTube and sharing one image folder between both languages.
7. **Newsletter:** sign-ups now arrive by e-mail; the Drive has a `Newsletter` sheet to record them in.
8. Merge `site-update-2026` into `main` to publish.

## Sources used (Google Drive, chopin.concours@gmail.com)

- `2026-2027/Chopin Piano Competition 2026-2027: Rules` and `… 2027 Alumni Edition: Rules`
- `2026-2027/Chopin Piano Competition 2026-2027` and `… 2027 - Alumni edition` (registration forms, both open)
- `2_Sponsoring/Concours_Chopin_Dossier_Sponsoring_2025_2026.pdf` (association texts, committee, 2025 results)
- `2_Sponsoring/Chopin_Finale_9mai2026_VIP_et_Sponsors.pdf` (date and venue of the 2026 Grand Final)
- `Images  charte graphique/Banniere_generale_sponsors_partenaires.png` and `Logos sponsors et partenaires/`
- Concert forms in `CCE/` and `2026-2027/` (dates, venues, programmes)
- Photos: `Photos 2026/Selection Tim`, `2026-2027/Concert-2026-10-29/Selection`,
  `Videos/Videos 2025-2026/Second round Lausanne/photos`
