# How the site calendar works

The pages `calendrier.html` (FR) and `calendrier-en.html` (EN) contain two things:

1. **A "Key dates" list** written directly in the HTML. Edit it by hand in both files when dates change.
2. **A monthly calendar** (FullCalendar library) that reads events live from a **public Google Calendar**.
   Nobody edits the website to add an event: you add it in Google Calendar, and it appears on the site
   within a few minutes.

The two settings live in `js/calendar-config.js`:

| Setting | Current value | Meaning |
|---|---|---|
| `calendarId` | `chopin.concours@gmail.com` | Which Google Calendar is shown |
| `apiKey` | key created by the previous developer | Google Cloud key allowed to read public calendars |

> Until 9 Nov 2026 the site showed the calendar `louis.elhani@gmail.com`, a personal calendar
> (interviews, internship meetings). It has been replaced by the association's calendar.

## One-time setup (with the chopin.concours@gmail.com account)

1. Open <https://calendar.google.com> signed in as **chopin.concours@gmail.com**.
2. Recommended: create a dedicated calendar: left column, **Other calendars → + → Create new calendar**,
   name it e.g. "Concours Chopin – public". (Using the main calendar also works, but then every event in it
   becomes public.)
3. Open that calendar's **Settings and sharing**:
   - **Access permissions for events** → tick **Make available to public** → "See all event details".
   - **Integrate calendar** → copy the **Calendar ID** (for a dedicated calendar it ends in
     `@group.calendar.google.com`; for the main calendar it is `chopin.concours@gmail.com`).
4. Put that ID in `js/calendar-config.js` as `calendarId`, commit and push.
5. API key: the current key belongs to the previous developer's Google Cloud project and can stop working
   at any time. To own it:
   - <https://console.cloud.google.com> (as chopin.concours@gmail.com) → create a project.
   - **APIs & Services → Library** → enable **Google Calendar API**.
   - **APIs & Services → Credentials → Create credentials → API key**.
   - Restrict it: **Application restrictions → Websites** → add
     `https://chopinconcours.github.io/*`; **API restrictions** → Google Calendar API only.
   - Replace `apiKey` in `js/calendar-config.js`.

If the calendar cannot be loaded (calendar not public, wrong ID, invalid key), the page shows a yellow
message and the "Key dates" list stays visible.

## Adding an event (every time)

In Google Calendar, in the public calendar chosen above, create the event:

- **Title**: short and clear, e.g. `Concert – Ensemble Dyade (HEMU)` or `Concours – deadline vidéos`.
- **Date / time**: tick "All day" for deadlines; otherwise set start and end times (Swiss time).
- **Location**: room and campus, e.g. `POL-164, UNIL`.
- **Description**: programme, price, and the booking link if there is one.
- Save. The event is visible on the site after a short delay (refresh the page).

Clicking an event on the site opens it in Google Calendar in a new tab.

Tip: put each event in French or in English consistently. The calendar shows the same events on the FR and EN
pages; only the interface (month names, buttons) changes language.
