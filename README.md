# TMDb Movies (Kodi Addon)

Fork of **TMDb Movies** by Angelitto ([angelitto2005/repository.angelitto](https://github.com/angelitto2005/repository.angelitto)), kept in sync with upstream plus extra bug fixes (see `changelog.txt`).

Kodi video addon for browsing movies and TV shows via TMDb, with streams from 20+ HTTP sites, AIO Streams and Stremio addons (Torrentio, MediaFusion, Comet, Meteor, StremThru, Usenet), debrid clouds, and P2P via TorrServer. Optional Trakt / Simkl / MDBList / TMDb account integration.

> This addon is a search front end. It does not host any content.

---

## Install (from the repository — recommended)

Install through the addon repository, **not** from a raw source zip. The repository installs every dependency automatically and keeps the addon updated.

Tested by upstream on **Kodi 20 Nexus, 21 Omega and 22 Piers** (Windows, macOS, Linux, Android, LibreELEC/CoreELEC, Fire TV). Kodi 19 Matrix may work but is not tested.

### 1. Allow unknown sources
**Settings → System → Add-ons → Unknown sources → On** (confirm the warning).

### 2. Add the repository source
**Settings → File manager → Add source → `<None>`** and type exactly:
```
https://avinashiitd.github.io/plugin.video.tmdbmovies/
```
Name it `tmdbmovies` and press **OK**.

### 3. Install the repository
**Settings → Add-ons → Install from zip file → `tmdbmovies` → `repository.avinashiitd-1.0.0.zip`**
Wait for *"TMDb Movies Repository – Add-on installed"*.

### 4. Install TMDb Movies
**Settings → Add-ons → Install from repository → TMDb Movies Repository → Video add-ons → TMDb Movies → Install**.
Kodi shows the list of dependencies it will install – press **OK**.

The addon now appears under **Add-ons → Video add-ons**, and updates arrive automatically.

### What gets installed automatically

| Dependency | Comes from |
|---|---|
| `script.module.resolveurl` (+ `six`, `kodi-six`, `pyqrcode`) | ResolveURL repository (included in our repository's sources) |
| `script.module.requests` | Official Kodi repository |
| `inputstream.adaptive` | Official Kodi repository |

**Exception – desktop Linux** (Ubuntu/Debian/Fedora/Arch Kodi packages): `inputstream.adaptive` is a system package there. Install it before step 4, then enable it under **Add-ons → My add-ons → VideoPlayer InputStream → InputStream Adaptive**:
```bash
sudo apt install kodi-inputstream-adaptive      # Debian / Ubuntu
sudo dnf install kodi-inputstream-adaptive      # Fedora (RPM Fusion)
sudo pacman -S kodi-addon-inputstream-adaptive  # Arch
```
LibreELEC, CoreELEC, Windows, macOS and Android need nothing extra.

### Optional companions

| For | Install |
|---|---|
| Trailers | The default trailer player is *TMDbM Trailers*, which is not included here. Either install **YouTube** from the official Kodi repository and set **Settings → Menu → Play trailers with → YouTube Plugin**, or install *TMDbM Trailers* from the Angelitto repository. |
| P2P sources | A running [TorrServer](https://github.com/YouROK/TorrServer) (default `127.0.0.1:8090`). |

> **Don't also install TMDb Movies from the Angelitto repository.** Kodi always picks the highest version across repositories, so the next upstream release would replace this fork. If that already happened: uninstall TMDb Movies, then reinstall it from *TMDb Movies Repository*.

---

## First-time setup

Browsing works immediately. **Playing** needs at least one source. Open the addon settings (long-press / right-click TMDb Movies → *Settings*):

1. **HTTP Providers** – free sites, on by default; toggle individual sites here.
2. **AIO Streams** – choose an instance, configure it on that instance's website, then paste your **UUID** and **password**.
3. **Stremio** (Torrentio, MediaFusion, Comet, Meteor, StremThru, Usenet, custom) – enable a provider, open its *Configure* page in a browser, connect your debrid service, then paste the generated **`manifest.json` URL**.
4. **P2P Providers** – point it at your TorrServer; private trackers (FileList, SpeedApp, SeedPool) need your own credentials.
5. **Accounts** (optional) – *Connect Trakt* shows a code / QR to enter at trakt.tv/activate. Simkl, TMDb and MDBList can be connected here too.
6. **My Debrid Cloud** (optional) – Real-Debrid, TorBox, Premiumize, Offcloud cloud browsing.
7. **General → Language** – default `enro` (English + Romanian); set `en` for English-only plots and artwork. **Subtitles → Languages** defaults to `ro`; change to e.g. `en`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Source shows no files in step 3 | Check the URL ends with `/` and has no typos; open it in a browser – it must list `repository.avinashiitd-1.0.0.zip`. |
| *"Dependencies not met"* / *"Could not connect to repository"* | Check internet access, then **Add-ons → My add-ons → Add-on repository → TMDb Movies Repository → Update** and retry. On desktop Linux, install `inputstream.adaptive` as above. |
| Stream starts with no video / playback error | Make sure **InputStream Adaptive** is installed **and enabled**. |
| *"No sources found"* | Configure a provider (see [First-time setup](#first-time-setup)); raise **HTTP Providers → Max source wait time**. |
| Stale or wrong results | **Maintenance → Delete All Cache**, or long-press an item → clear sources cache. |
| Addon reverted to upstream version | See the note under [Optional companions](#optional-companions). |
| Anything else | Keep **Maintenance → Enable Detailed Logging** on (default), reproduce the problem, use **Upload Kodi Log to Pastebin**, and open an issue with the link. |

Kodi log locations: Windows `%APPDATA%\Kodi\kodi.log` · Linux `~/.kodi/temp/kodi.log` · macOS `~/Library/Logs/kodi.log` · Android `Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log`.

---

## For maintainers

The Kodi repository is built and published by GitHub Actions (`.github/workflows/publish-kodi-repo.yml`) on every push to `main`:

- `kodi-repo/build.py` zips the addon (tracked files only; `.github/`, `kodi-repo/` and `README.md` are excluded) and the repository addon, then writes `zips/addons.xml`, `addons.xml.md5` and an `index.html` into `_site/`, which is deployed to GitHub Pages.
- `kodi-repo/repository.avinashiitd/addon.xml` points Kodi at this site **and** at the ResolveURL repository, so the `script.module.resolveurl` dependency always resolves.
- **One-time setup:** repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
- **Releasing:** bump `version` in `addon.xml` (and add a `changelog.txt` entry), then merge to `main`. Kodi only offers the update when the version increases. Fork releases add a fourth number to the upstream version (e.g. `1.1.310.1`) so they rank above that upstream release.
- **Local build:** `python3 kodi-repo/build.py` (output in `_site/`).

Upstream source: https://github.com/angelitto2005/repository.angelitto/tree/main/all/plugin.video.tmdbmovies
