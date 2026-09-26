# TMDb Movies (Kodi Addon)

Fork of the **TMDb Movies** addon from [angelitto2005/repository.angelitto](https://github.com/angelitto2005/repository.angelitto).

Original author: Angelitto

## About

Kodi video addon for browsing movies and TV shows via TMDb, with HTTP stream support through providers like AIO Streams, Torrentio, MediaFusion, Comet, Meteor, and other debrid/streaming services.

## Requirements

- Kodi 19+ (Python 3)
- `script.module.requests`
- `script.module.resolveurl`
- `inputstream.adaptive`

## Install

1. Download the latest `plugin.video.tmdbmovies-<version>.zip` from the [Releases page](https://github.com/avinashiitd/plugin.video.tmdbmovies/releases/latest).
2. In Kodi, go to *Settings → Add-ons → Install from zip file* and select the downloaded zip.
   (Enable *Unknown sources* under *Settings → System → Add-ons* first if prompted.)
3. Install the dependencies listed above if Kodi does not resolve them automatically.

Releases are built automatically by GitHub Actions whenever the version in `addon.xml` changes on `main`.

## Upstream

Source extracted from: https://github.com/angelitto2005/repository.angelitto/tree/main/all/plugin.video.tmdbmovies
