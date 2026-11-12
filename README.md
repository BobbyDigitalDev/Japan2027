# 2027 Japan Spring Trip

Itinerary dashboard for a trip to Japan in the first two weeks of March 2027, planned around a wedding in Osaka on Sunday, March 7 at 11:00.

Live page: https://bobbydigitaldev.com/Japan2027/

## Workflow

- `index.html` is the whole dashboard (single file, no build step).
- Confirmed plans live in the `plans` object in the script at the bottom of `index.html`. Days without an entry show as open.
- Push to `main` and GitHub Pages redeploys.

## Status log

- 2026-11-12: Dashboard started. Two-week calendar (Sun Feb 28 to Sat Mar 13, Sunday start) with the wedding day and the Osaka hotel stay (Mar 6 to 8). Repo created and published with GitHub Pages.
- 2026-11-12: Added a password prompt to the page. It is cosmetic only: the check runs in the browser and the page content is still in the public source, so it deters casual visitors but is not real protection. The browser remembers a correct entry.
