from pathlib import Path
import sys
import xbmc

addon_root = str(Path(__file__).parent.parent.parent)
if addon_root not in sys.path:
    sys.path.insert(0, addon_root)

if __name__ == '__main__':
    # Kodi can execute this file with either the addon root or this directory
    # on sys.path.  The package import works reliably in both cases.
    from resources.lib.entry import run_plugin
    run_plugin()
    # RLI fix: prevent stale interpreter when container changes to another addon
    try:
        plugin_name = xbmc.getInfoLabel('Container.PluginName') or ''
        if plugin_name and 'tmdbmovies' not in plugin_name.lower():
            raise SystemExit()
    except SystemExit:
        raise
    except:
        pass
