#!/usr/bin/env python3
"""Validate bundled OpenAPI documents; optionally probe public endpoints.

Run: python3 validate.py          (offline checks only)
     python3 validate.py --live   (also sends public API requests)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
URL = 'https://api.chucknorris.io'


def offline() -> None:
    data = json.loads((HERE / 'openapi.json').read_text(encoding='utf-8'))
    assert data['openapi'] == '3.1.0'
    assert data['servers'][0]['url'] == URL
    expected = {'/jokes/random', '/jokes/categories', '/jokes/search'}
    assert set(data['paths']) == expected
    for path in expected:
        op = data['paths'][path]['get']
        assert 'operationId' in op and 'responses' in op and '200' in op['responses']
        assert 'content' in op['responses']['200']
    assert data['components']['schemas']['Joke']['properties']['value']['type'] == 'string'
    refs = []
    def walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == '$ref':
                    refs.append(value)
                else:
                    walk(value)
        elif isinstance(obj, list):
            for entry in obj:
                walk(entry)
    walk(data)
    for ref in refs:
        assert ref.startswith('#/components/schemas/')
        assert ref.split('/')[-1] in data['components']['schemas']
    params = data['paths']['/jokes/search']['get']['parameters']
    assert any(x['name'] == 'query' and x['required'] and x['in'] == 'query' for x in params)
    try:
        import yaml  # optional PyYAML package
    except ImportError:
        print('YAML comparison skipped (optional dependency PyYAML is not installed).')
    else:
        yml = yaml.safe_load((HERE / 'openapi.yaml').read_text(encoding='utf-8'))
        assert yml == data, 'YAML and JSON specification versions have diverged'
        print('YAML/JSON equivalence: PASS')
    print('OpenAPI structural checks: PASS')


def get_json(path: str):
    req = Request(URL + path, headers={'Accept': 'application/json', 'User-Agent': 'Scalar-Academic-Demo/1.0'})
    with urlopen(req, timeout=12) as response:
        assert response.status == 200, (path, response.status)
        data = json.load(response)
        print(f'GET {path}: HTTP {response.status}')
        return data


def live() -> None:
    categories = get_json('/jokes/categories')
    assert isinstance(categories, list) and 'dev' in categories
    joke = get_json('/jokes/random?category=dev')
    assert isinstance(joke, dict) and isinstance(joke['value'], str) and joke['id']
    matches = get_json('/jokes/search?query=computer')
    assert isinstance(matches['total'], int) and isinstance(matches['result'], list)
    print('Live endpoint shape checks: PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true', help='also test live external API endpoints')
    args = parser.parse_args()
    offline()
    if args.live:
        try:
            live()
        except Exception as exc:
            raise SystemExit(f'Live API check unavailable/failed: {exc}') from exc
