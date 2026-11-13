# 2027 Japan Spring Trip

Itinerary dashboard for a trip to Japan in the first two weeks of March 2027, planned around a wedding in Osaka on Sunday, March 7 at 11:00.

Live page: https://bobbydigitaldev.com/Japan2027/

## Workflow

- `index.html` holds the page, styles and scripts. It reads three generated data files: `places.js` (places from the videos), `routes.js` (three road trip options) and `hotels.js` (hotel picks and totals). Each has a `?v=` value in its script tag; bump it when the file changes so browsers do not use a stale copy.
- Confirmed plans live in the `plans` object in the script at the bottom of `index.html`. Days without an entry show as open.
- `tools/build_routes.py` builds `routes.js` from OSRM route data. `tools/build_hotels.py <research/hotels folder> hotels.js` builds `hotels.js` from the research JSON files (one per stop) plus `tools/hotel_photos.json`. Totals are summed by the script, never typed. Research files are in `research/` (hotels, cars), route and place source data in `data/`, the checker is `tools/check_research.py` and the collection rules are in `docs/RESEARCH-PROTOCOL.md`. Run `python3 tools/check_research.py` after adding research files. The repo is the working copy; the trip folder on Bobby's computer mirrors it.
- The map stays directly below the road trip options. New sections go after the map.
- Push to `main` and GitHub Pages redeploys.

## Status log

- 2026-11-12: Dashboard started. Two-week calendar (Sun Feb 28 to Sat Mar 13, Sunday start) with the wedding day and the Osaka hotel stay (Mar 6 to 8). Repo created and published with GitHub Pages.
- 2026-11-12: Added a password prompt to the page. It is cosmetic only: the check runs in the browser and the page content is still in the public source, so it deters casual visitors but is not real protection. The browser remembers a correct entry.
- 2026-11-13: Independent code review, then fixes: the map was empty after the first password entry (now resizes on unlock); the printed map was cropped (map size is set before the print layout starts, so the PDF shows the whole route); Route A hid its own Kyoto stops; place-type chips fell out of sync after a place link; costs table now marks cells that reuse a lower pick; "how well checked" text now comes from the data; Route C pop-ups show both nights; Matsuyama no longer widens the default map view; removed test screenshots from the repo.
- 2026-11-13: Hotel photos: all 53 hotels now have a photo (35 added; 41 show the building or entrance, the other 12 show the first gallery image with a label saying what it shows). Photos come from each hotel's own gallery folder on hotels.com.
