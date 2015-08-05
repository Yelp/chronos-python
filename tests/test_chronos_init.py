import json

import mock

import chronos


def test_graph():
    client = chronos.ChronosClient(hostname="localhost")
    fake_call_output = (
        "node,testjob-parent,failure,queued\n"
        "node,testjob-child,fresh,idle\n"
        "link,testjob-parent,testjob-child\n"
    )
    with mock.patch.object(client, "_call", spec=True, return_value=fake_call_output) as mock_call:
        actual = client.graph()
    mock_call.assert_called_once_with("/scheduler/graph/csv", "GET")
    assert actual == fake_call_output.splitlines()


def test_check_accepts_json():
    client = chronos.ChronosClient(hostname="localhost")
    fake_response = mock.Mock()
    fake_response.status = 200
    fake_content = '{ "foo": "bar" }'
    actual = client._check(fake_response, fake_content)
    assert actual == json.loads(fake_content)


def test_check_returns_raw_response_when_not_json():
    client = chronos.ChronosClient(hostname="localhost")
    fake_response = mock.Mock()
    fake_response.status = 401
    fake_content = "UNAUTHORIZED"
    actual = client._check(fake_response, fake_content)
    assert actual == fake_content
