# OSRS Group Stats

A single-page stats board for a group of Old School RuneScape accounts, laid out like the in-game skills tab. Add any player by username, and the roster is stored in the URL so the link you copy opens the same board for everyone else.

Works for any set of accounts — an ironman group, a clan's core members, or just you and a friend.

## What it does

- Shows each player's 24 skills in the in-game three-column layout, with the levels, the diagonal split and the total level bar
- **Add a player** by username; **×** on any card removes them
- The roster lives in the query string (`?p=name&p=name`), so **Copy link** produces a shareable board
- **Update all stats** asks Wise Old Man to re-read the official hiscores for every player on the board
- A summary strip across the top: combined total level, combined XP, highest combat level, and the single highest skill level with who holds it
- **Best in group** under each card: the skills where that player holds the roster's highest level, with ties marked

## Dependencies

Nothing to install — no npm, no build step, no framework. The only runtime dependency is the [Wise Old Man API](https://docs.wiseoldman.net/), which supplies every level, XP total and combat level on the board, so the page needs an internet connection to show anything. Skill icons are stored in `icons/` rather than fetched from the wiki.

## Known limitations

- **Current and maximum levels always match.** The hiscores report your real level only — they have no way to know you are boosted or drained, so both numbers in each box come from the same value.
- **Stats are only as fresh as the last update.** Wise Old Man caches a snapshot; it does not poll the hiscores continuously. If nobody has updated an account recently the numbers can be days old. The card footer shows how stale each one is. Installing the [Wise Old Man RuneLite plugin](https://runelite.net/plugin-hub/show/wom-utils) uploads automatically on logout and keeps this current.
- **Quest completion is not shown.** No public API exposes it; the hiscores carry total quest points and nothing else.
- **No in-game Group Ironman group lookup.** Jagex's group hiscores page is HTML with no CORS headers, so a static page in a browser cannot read it. Doing this would need a small server-side proxy.
- **Everyone who opens the link hits the API from their own browser.** If several people mash the update button at once you may hit the rate limit. Agreeing that one person refreshes avoids it.

## Credits

Skill icons come from the [Old School RuneScape Wiki](https://oldschool.runescape.wiki), available under [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/). Stats come from [Wise Old Man](https://wiseoldman.net), an open-source community project.

This is an unofficial fan project with no connection to Jagex. RuneScape and Old School RuneScape are trademarks of Jagex Limited.

## Licence

The code in this repository is MIT licensed — see `LICENSE`. That covers the code only, not the icons or any other third-party content it links to.
