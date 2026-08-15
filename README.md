# OSRS Group Stats

A single-page stats board for a group of Old School RuneScape accounts, laid out like the in-game skills tab. Add any player by username, and the roster is stored in the URL so the link you copy opens the same board for everyone else.

Works for any set of accounts — an ironman group, a clan's core members, or just you and a friend.

## What it does

- Shows each player's 24 skills in a pixel-exact reproduction of the in-game skills tab — the client's own stone, chrome, icons and engraved diagonals, with the levels set in the face the interface actually draws them with
- **Add a player** by username; **×** on any card removes them
- The roster lives in the query string (`?p=name&p=name`), so **Copy link** produces a shareable board
- **Update all stats** asks Wise Old Man to re-read the official hiscores for every player on the board
- A summary strip across the top: combined total level, combined XP, highest combat level, and the single highest skill level with who holds it
- **Best in group** under each card: the skills where that player holds the roster's highest level, with ties marked

## Dependencies

Nothing to install — no npm, no build step, no framework. The only runtime dependency is the [Wise Old Man API](https://docs.wiseoldman.net/), which supplies every level, XP total and combat level on the board, so the page needs an internet connection to show anything. Everything else is served from the repo: the panel artwork in `assets/` and the fonts in `fonts/`. Nothing is hotlinked.

## The panel artwork

`assets/skills-card.png`, `assets/skill-icons.png` and `assets/osrs-frame.png` are cut from one capture of the client's skills tab, `tools/Skills_tab.png`. `tools/build-assets.py` does the cutting and can be re-run to rebuild all three:

```
python3 -m pip install Pillow
cd tools && python3 build-assets.py
```

It separates the sprite into tile interior, engraved diagonal and chrome by asking which pixels ever show bare stone across all 24 tiles, lifts each icon out with a flood fill from the tile edges — grey icon pixels can land exactly on a stone colour, so anything the background cannot reach is kept — and redraws the stone as fresh noise over the sprite's own eight-colour ramp, since copying the literal pixels prints one patch into every tile and ghosts whichever icon used to cover it. The extra bars above and below the grid are the total-level bar repeated.

The result is verifiably exact: rendered at 1× against the source sprite, all 24 tiles match pixel for pixel on both icons and level numbers, as does the total-level readout.

## Known limitations

- **Current and maximum levels always match.** The hiscores report your real level only — they have no way to know you are boosted or drained, so both numbers in each box come from the same value.
- **Stats are only as fresh as the last update.** Wise Old Man caches a snapshot; it does not poll the hiscores continuously. If nobody has updated an account recently the numbers can be days old. The card footer shows how stale each one is. Installing the [Wise Old Man RuneLite plugin](https://runelite.net/plugin-hub/show/wom-utils) uploads automatically on logout and keeps this current.
- **Quest completion is not shown.** No public API exposes it; the hiscores carry total quest points and nothing else.
- **No in-game Group Ironman group lookup.** Jagex's group hiscores page is HTML with no CORS headers, so a static page in a browser cannot read it. Doing this would need a small server-side proxy.
- **Everyone who opens the link hits the API from their own browser.** If several people mash the update button at once you may hit the rate limit. Agreeing that one person refreshes avoids it.

## Credits

The skills tab capture the panel artwork is cut from comes from the [Old School RuneScape Wiki](https://oldschool.runescape.wiki), available under [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/). Stats come from [Wise Old Man](https://wiseoldman.net), an open-source community project.

The typefaces are the game client's own, extracted by [RuneStar/fonts](https://github.com/RuneStar/fonts) and released under CC0. Plain 11 is the face the interface draws with — its digits advance 6px, which is exactly the spacing measured off the sprite — so the levels and the total use it, and the page furniture uses Plain 12, Bold 12 and Quill. All four are drawn on a 16-unit em (32 for Quill), so the stylesheet keeps text at whole multiples of those sizes and scales whole cards rather than changing type size; at any other size the glyphs land off the pixel grid and go soft.

Centring is done in script rather than by `text-align`. The client places a text box on a whole pixel and rounds half of an odd width downwards; leaving it to CSS puts odd-width readouts — a lone `2`, a lone `0` — one pixel off from where the sprite has them.

`assets/bg2.jpg` is the stone-and-vines panel from the Old School RuneScape website, and `assets/gim-crest.png` is the Group Ironman helm badge from Jagex's support site, saved into the repo rather than hotlinked. Unlike the fonts, neither carries an open licence — both are Jagex artwork, reused here on the same fan-project footing as the rest of the page. The masthead keeps a drawn SVG helm behind the badge, which uncovers itself if the image ever fails to load.

This is an unofficial fan project with no connection to Jagex. RuneScape and Old School RuneScape are trademarks of Jagex Limited.

## Licence

The code in this repository is MIT licensed — see `LICENSE`. That covers the code only, not the icons, fonts, background or any other third-party content it bundles.
