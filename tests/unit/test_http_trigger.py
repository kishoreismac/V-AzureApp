import json
import pytest

import azure.functions as func

from function_app import http_trigger


def make_request(query=None, body=None):
    """
    Helper to create an HttpRequest for Azure Functions Python.
    """
    query = query or {}
    body_bytes = b""
    if body is not None:
        body_bytes = json.dumps(body).encode("utf-8")

    return func.HttpRequest(
        method="GET",
        url="http://localhost/api/http_trigger",
        headers={},
        params=query,
        route_params={},
        body=body_bytes,
    )


def test_returns_hello_when_name_in_query():
    req = make_request(query={"name": "Vaishnavi"})
    resp = http_trigger(req)

    assert resp.status_code == 200
    assert resp.get_body().decode() == "Hello, Vaishnavi. This HTTP triggered function successfully."


def test_returns_hello_when_name_in_json_body():
    req = make_request(body={"name": "Kishore"})
    resp = http_trigger(req)

    assert resp.status_code == 200
    assert resp.get_body().decode() == "Hello, Kishore. This HTTP triggered function executed successfully."


def test_returns_default_message_when_name_missing_and_invalid_json():
    # invalid JSON -> get_json() raises ValueError
    req = func.HttpRequest(
        method="GET",
        url="http://localhost/api/http_trigger",
        headers={},
        params={},
        route_params={},
        body=b"not-json",
    )
    resp = http_trigger(req)

    assert resp.status_code == 200
    assert "Pass a name in the query string" in resp.get_body().decode()
