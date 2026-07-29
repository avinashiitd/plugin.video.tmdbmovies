"""Small regression tests for TMDb list request helpers.

These run outside Kodi by extracting just the helper functions under test.
"""
import ast
import pathlib
import sys
import types
import unittest


SOURCE = pathlib.Path(__file__).parents[1] / 'resources' / 'lib' / 'tmdb_api.py'


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


if __name__ == '__main__':
    unittest.main()
