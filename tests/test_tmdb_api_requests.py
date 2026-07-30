"""Small regression tests for TMDb list request helpers.

These run outside Kodi by extracting just the helper functions under test.
"""
import ast
import pathlib
import sys
import types
import unittest


SOURCE = pathlib.Path(__file__).parents[1] / 'resources' / 'lib' / 'tmdb_api.py'
ENTRY_SOURCE = pathlib.Path(__file__).parents[1] / 'resources' / 'lib' / 'entry.py'
ROUTER_SOURCE = pathlib.Path(__file__).parents[1] / 'resources' / 'lib' / 'router.py'
SERVICE_SOURCE = pathlib.Path(__file__).parents[1] / 'resources' / 'lib' / 'service.py'
SCRAPER_SOURCE = pathlib.Path(__file__).parents[1] / 'resources' / 'lib' / 'scraper.py'


def extract_function(source, name, namespace):
    tree = ast.parse(source.read_text(encoding='utf-8'))
    node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
    module = ast.Module(body=[node], type_ignores=[])
    exec(compile(module, str(source), 'exec'), namespace)
    return namespace[name]


def load_helpers(session):
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    wanted = {'get_dates', 'get_tmdb_movies_standard', '_tmdb_get'}
    module = ast.Module(
        body=[node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted],
        type_ignores=[],
    )

    config = types.ModuleType('resources.lib.config')
    config.get_headers = lambda: {'User-Agent': 'test'}
    config.get_session = lambda: session
    sys.modules['resources'] = types.ModuleType('resources')
    sys.modules['resources.lib'] = types.ModuleType('resources.lib')
    sys.modules['resources.lib.config'] = config

    logs = []
    namespace = {
        'BASE_URL': 'https://api.themoviedb.org/3',
        'API_KEY': 'key',
        'LANG': 'en-US',
        'datetime': __import__('datetime'),
        'xbmc': types.SimpleNamespace(LOGERROR=4),
        'log': lambda message, level: logs.append((message, level)),
    }
    exec(compile(module, str(SOURCE), 'exec'), namespace)
    return namespace, logs


class FakeResponse:
    def __init__(self, status_code=200, text=''):
        self.status_code = status_code
        self.text = text


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.response


class TmdbRequestTests(unittest.TestCase):
    def test_unknown_movie_action_does_not_make_a_default_request(self):
        session = FakeSession(FakeResponse())
        helpers, logs = load_helpers(session)

        self.assertIsNone(helpers['get_tmdb_movies_standard']('not-a-real-action', 1))
        self.assertEqual(session.calls, [])
        self.assertIn('No API route registered', logs[0][0])

    def test_list_requests_use_shared_retrying_session_and_headers(self):
        session = FakeSession(FakeResponse())
        helpers, _ = load_helpers(session)

        result = helpers['get_tmdb_movies_standard']('tmdb_movies_popular', 2)

        self.assertIs(result, session.response)
        args, kwargs = session.calls[0]
        self.assertIn('/movie/popular?', args[0])
        self.assertEqual(kwargs['headers'], {'User-Agent': 'test'})
        self.assertEqual(kwargs['timeout'], 15)

    def test_http_errors_are_returned_as_a_clean_empty_result(self):
        session = FakeSession(FakeResponse(503, 'temporarily unavailable'))
        helpers, logs = load_helpers(session)

        self.assertIsNone(helpers['_tmdb_get']('https://example.test', 'popular'))
        self.assertIn('API 503', logs[0][0])

    def test_v4_requests_use_the_user_token_not_the_application_token(self):
        calls = []

        class Requests:
            @staticmethod
            def get(url, **kwargs):
                calls.append((url, kwargs))
                return FakeResponse()

        response = FakeResponse()
        response.json = lambda: {'results': []}
        Requests.get = staticmethod(lambda url, **kwargs: (calls.append((url, kwargs)) or response))
        namespace = {
            'get_tmdb_v4_token': lambda: 'user-access-token',
            'TMDB_V4_BASE_URL': 'https://api.themoviedb.org/4',
            'requests': Requests,
            'xbmc': types.SimpleNamespace(LOGERROR=4, LOGWARNING=2),
            'log': lambda *_: None,
        }
        request = extract_function(SOURCE, 'tmdb_v4_request', namespace)

        self.assertEqual(request('/account/1/lists'), {'results': []})
        self.assertEqual(calls[0][1]['headers']['Authorization'], 'Bearer user-access-token')

    def test_malformed_warmup_timestamp_does_not_break_menu_navigation(self):
        class Window:
            def getProperty(self, _):
                return 'not-a-number'

        warmup_is_due = extract_function(ENTRY_SOURCE, '_warmup_is_due', {})
        self.assertTrue(warmup_is_due(Window(), 'tmdb_last_warmup_movie', 1000.0))

    def test_entrypoints_import_the_packaged_entry_module(self):
        self.assertIn('from resources.lib.entry import run_plugin', ROUTER_SOURCE.read_text(encoding='utf-8'))
        self.assertIn('from resources.lib.entry import run_service', SERVICE_SOURCE.read_text(encoding='utf-8'))

    def test_disabled_debrid_providers_are_not_selected(self):
        source = SCRAPER_SOURCE.read_text(encoding='utf-8')
        self.assertGreaterEqual(source.count("pid in debrid_providers and is_enabled == 'true'"), 2)


if __name__ == '__main__':
    unittest.main()
