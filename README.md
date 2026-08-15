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

## Deploying to GitHub Pages

1. Create a new repository on GitHub.
2. Copy `index.html` and `.nojekyll` into it and push to `main`.
3. In the repository, go to **Settings → Pages**.
4. Under **Build and deployment**, set **Source** to *Deploy from a branch*, pick `main` and the `/ (root)` folder, then **Save**.
5. Wait a minute or two. Your board will be at `https://<your-username>.github.io/<repo-name>/`.

`.nojekyll` tells GitHub to serve the files as-is rather than running them through Jekyll. Nothing here needs Jekyll, and it avoids surprises if a file is ever added whose name starts with an underscore.

To share a specific roster, load the players you want and copy the URL from the address bar — it will look like:

```
https://you.github.io/osrs-group-stats/?p=zezima&p=some%20other%20name
```

### Other hosts

Any static host works, since this is one self-contained file. Netlify, Cloudflare Pages, Vercel, or dragging the file onto [Netlify Drop](https://app.netlify.com/drop) all serve it without configuration.

## Dependencies

**Nothing to install.** No npm, no build step, no bundler, no framework. `index.html` contains all the HTML, CSS and JavaScript. You can open it directly from your filesystem and it will work.

At runtime it talks to two third-party services over the network:

| Service | Used for | Notes |
|---|---|---|
| [Wise Old Man API](https://docs.wiseoldman.net/) v2 | Player levels, XP, combat level, last-updated time | Public, no API key needed for this usage |
| [OSRS Wiki](https://oldschool.runescape.wiki) | The 24 skill icons | Hotlinked images; if one fails to load the box hides the icon and still shows the levels |

Because both are fetched from the browser, the page needs an internet connection to show anything. There is no server component and no database.

### About the Wise Old Man API

- `GET /v2/players/{username}` reads a player's stored snapshot
- `POST /v2/players/{username}` asks Wise Old Man to re-read that player from the official hiscores — this is what **Update all stats** does, and what registers a player who has never been tracked
- Each account has a **60 second cooldown** between updates. Pressing the button again inside that window is handled: those players keep their existing numbers and the status line says so
- Requests are spaced 400 ms apart to stay within the unauthenticated rate limit
- Heavy or automated use should send an API key and a user agent; see their docs. This page does neither, which is fine for a handful of people refreshing occasionally

## Configuration

Everything adjustable sits near the top of the `<script>` block in `index.html`:

```js
const MAX_PLAYERS = 12;

// Optional. Loaded when the URL has no ?p= values, e.g. ["zezima","woox"]
const DEFAULTS = [];
```

`DEFAULTS` ships empty, so the bare link opens on an empty board and you build the roster from the input. If you would rather it always open on the same accounts, put their usernames in the array — quoted, comma separated, spaces kept as they appear in game:

```js
const DEFAULTS = ["first name", "second name", "third name"];
```

Either way, a URL with `?p=` values always wins over `DEFAULTS`, so a shared link opens on the roster it carries.

The colours are CSS custom properties in `:root`. `--amber`, `--ink` and `--cream` control the page chrome; `--lvl` and the `--stone-*` values control the in-game panels.

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
