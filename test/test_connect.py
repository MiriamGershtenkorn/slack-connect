import pytest
from unittest.mock import MagicMock
from slack_sdk.errors import SlackApiError


def test_list_connections_success(monkeypatch, capsys):
    mock_client = MagicMock()

    mock_client.users_list.return_value = {
        "members": [
            {"name": "user1", "id": "U1"},
            {"name": "user2", "id": "U2"},
        ]
    }

    mock_client.conversations_list.return_value = {
        "channels": [
            {"name": "general", "id": "C1"},
            {"name": "random", "id": "C2"},
        ]
    }

    mock_client.api_test.return_value = {"ok": True}

    monkeypatch.setattr("src.connect.client", mock_client)

    from src.connect import list_connections
    list_connections()

    captured = capsys.readouterr().out

    assert "user1" in captured
    assert "general" in captured
    assert "API Test Response" in captured


def test_list_connections_slack_error(monkeypatch, capsys):
    mock_client = MagicMock()

    error = SlackApiError(
        message="error",
        response={"error": "invalid_auth"}
    )

    mock_client.users_list.side_effect = error

    monkeypatch.setattr("src.connect.client", mock_client)

    from src.connect import list_connections
    list_connections()

    captured = capsys.readouterr().out
    assert "invalid_auth" in captured
