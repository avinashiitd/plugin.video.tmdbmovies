# TMDb Movies (Kodi Addon)

Fork of the **TMDb Movies** addon from [angelitto2005/repository.angelitto](https://github.com/angelitto2005/repository.angelitto).
Original author: Angelitto.

Kodi video addon for browsing movies and TV shows via TMDb, with stream support through providers such as AIO Streams, Torrentio, MediaFusion, Comet, Meteor, debrid services, and P2P via TorrServer. Optional Trakt, TMDb account and MDBList integration.

> This addon is a search front end. It does not host any content, and most sources need your own provider configuration (see [First-time setup](#first-time-setup)).

---

## Requirements

| Item | Notes |
|---|---|
| Kodi 19 (Matrix) or newer | Kodi 20 Nexus / 21 Omega are recommended. Kodi 18 and older are **not** supported (Python 2). |
| `script.module.requests` | In the official Kodi repository, installed automatically. |
| `inputstream.adaptive` | In the official Kodi repository on Windows, macOS, Android and LibreELEC/CoreELEC. On desktop Linux it is a system package (see below). |
| `script.module.resolveurl` | **Not** in the official Kodi repository. You must add a repository that provides it **before** installing this addon, otherwise Kodi reports *"Dependencies not met"*. |

---

## Installation

### Step 1 – Allow unknown sources

1. Kodi → **Settings** (gear icon) → **System** → **Add-ons**.
2. Turn on **Unknown sources** and confirm the warning.

### Step 2 – Install the dependencies Kodi cannot find on its own

**ResolveURL** (required):
Install a repository that hosts `script.module.resolveurl` — for example the upstream [Angelitto repository](https://github.com/angelitto2005/repository.angelitto) or the official [ResolveURL](https://github.com/Gujal00/ResolveURL) repository — then:
**Add-ons → Install from repository → *that repository* → Program add-ons → ResolveURL → Install**.

**InputStream Adaptive** on desktop Linux (Ubuntu/Debian with the Kodi PPA, Fedora, Arch …):
```bash
sudo apt install kodi-inputstream-adaptive      # Debian / Ubuntu
sudo dnf install kodi-inputstream-adaptive      # Fedora (RPM Fusion)
sudo pacman -S kodi-addon-inputstream-adaptive  # Arch
```
Then in Kodi: **Add-ons → My add-ons → VideoPlayer InputStream → InputStream Adaptive → Enable**.
On every other platform Kodi installs it automatically.

### Step 3 – Build the zip

Kodi requires the zip to contain **one top-level folder named exactly `plugin.video.tmdbmovies`**.
GitHub's green *Code → Download ZIP* button creates a folder like `plugin.video.tmdbmovies-main`, which Kodi rejects with *"Invalid structure"* or *"Failed to install"*. Build the zip one of these ways instead:

**With git (Linux / macOS / Windows Git Bash):**
```bash
git clone https://github.com/avinashiitd/plugin.video.tmdbmovies.git
cd plugin.video.tmdbmovies
git archive --format=zip --prefix=plugin.video.tmdbmovies/ -o ../plugin.video.tmdbmovies.zip HEAD
```

**Without git:**
1. Download the ZIP from GitHub and extract it.
2. Rename the extracted folder to `plugin.video.tmdbmovies` (it must contain `addon.xml` directly inside it).
3. Right-click that folder → *Compress / Send to → Compressed (zipped) folder*.
4. Confirm that opening the zip shows `plugin.video.tmdbmovies/addon.xml`, not `addon.xml` at the root and not a second nested folder.

### Step 4 – Install from zip

1. Copy `plugin.video.tmdbmovies.zip` to a location Kodi can browse (USB stick, Downloads folder, network share).
2. Kodi → **Add-ons** → open-box icon (top left) → **Install from zip file**.
3. Select the zip. Wait for *"TMDb Movies – Add-on installed"*.
4. The addon appears under **Add-ons → Video add-ons**.

### Alternative – manual copy (developers)

Copy or symlink the repository folder (named `plugin.video.tmdbmovies`) into Kodi's addons directory, then restart Kodi and enable it under **Add-ons → My add-ons → Video add-ons**.

| Platform | Addons directory |
|---|---|
| Windows | `%APPDATA%\Kodi\addons\` |
| Linux | `~/.kodi/addons/` |
| macOS | `~/Library/Application Support/Kodi/addons/` |
| Android | `Android/data/org.xbmc.kodi/files/.kodi/addons/` |
| LibreELEC / CoreELEC | `/storage/.kodi/addons/` |

Dependencies are **not** installed automatically with this method; install them first (Step 2, plus `script.module.requests` from the official repository).

### Updating

Build a new zip from the latest code and use **Install from zip file** again; Kodi upgrades in place and keeps your settings. Settings and caches live in `userdata/addon_data/plugin.video.tmdbmovies/`.

---

## First-time setup

Browsing (TMDb lists, search, info dialogs) works immediately. **Playing** something requires at least one source provider. Open the addon settings (select the addon → *Configure*, or long-press/right-click → *Settings*):

1. **AIO Streams** tab – enabled by default. Pick an instance, configure it on that instance's website, and paste your **UUID** and **password** into the matching fields. Without them, AIO Streams returns no results.
2. **Debrid Sources** tab (Torrentio, MediaFusion, Comet, Meteor, custom) – enable a provider, open its *Configure URL* in a browser, set up your debrid service there, then paste the generated **`manifest.json` URL** into the addon.
3. **P2P Providers** tab (optional) – needs a running [TorrServer](https://github.com/YouROK/TorrServer) (default `127.0.0.1:8090`). Private trackers (FileList, SpeedApp) need your own credentials/passkey.
4. **HTTP Providers** tab – free HTTP scrapers; toggle them on or off individually.
5. **Accounts** tab (optional):
   - *Connect Trakt* – shows a code; enter it at trakt.tv/activate. Enables watched sync, Next Episodes, lists and ratings.
   - *Connect TMDb* – enables TMDb watchlist/favorites/lists.
   - *MDBList API Key* – get a free key at mdblist.com to use MDBList lists.
6. **Subtitles** tab (optional) – enable subtitle search and set languages (default `ro`; change to e.g. `en`).
7. **General → Plot** – the default language is `enro` (English + Romanian). Set it to `en` for English-only plots and artwork.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| *"Dependencies not met"* / *"Could not connect to repository"* | ResolveURL or InputStream Adaptive is missing – do Step 2 first. |
| *"Invalid structure"* / *"Failed to install"* from zip | The zip root is wrong – rebuild it as in Step 3. |
| Addon doesn't appear in Video add-ons after manual copy | The folder must be named exactly `plugin.video.tmdbmovies`; restart Kodi and check **My add-ons → Video add-ons** (it may be disabled). |
| *"No sources found"* | No provider is configured – see [First-time setup](#first-time-setup). Try increasing **HTTP Providers → Max source wait time**. |
| Stale or wrong results | **Maintenance → Delete All Cache**, or long-press an item → clear sources cache. |
| Stream plays with no video / errors on start | Make sure InputStream Adaptive is installed **and enabled**. |
| Anything else | Make sure **Maintenance → Enable Detailed Logging** is on (it is by default), reproduce the problem, then use **Upload Kodi Log** and open an issue with the link. The log lines are prefixed with the addon name. |

Kodi log locations: Windows `%APPDATA%\Kodi\kodi.log`, Linux `~/.kodi/temp/kodi.log`, macOS `~/Library/Logs/kodi.log`, Android `Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log`.

---

## Upstream

Source extracted from: https://github.com/angelitto2005/repository.angelitto/tree/main/all/plugin.video.tmdbmovies
