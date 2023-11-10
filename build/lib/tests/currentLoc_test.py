from src.currentLoc import currentLoc
import pytest
from unittest.mock import Mock, patch
import requests

coldMessage = "It is cold so you should wear warm clothing.\n"
warmMessage = "It is warm so you should wear light clothing.\n"
rainMessage = "It is currently raining so you do need an umbrella.\n\n"
norainMessage = "It is not raining so you don't need an umbrella.\n\n"

currentLoc_instance = currentLoc()


@patch("requests.get")
def test_getGeoLocationDataSuccess(mock_requests):
    # Setup
    with patch.object(currentLoc, "getIPAddress", autospec=True) as mock_getIP:
        mock_getIP.return_value = "127.0.0.1"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"current": {"temp_c": 20, "precip_mm": 5}}
        mock_requests.return_value = mock_response

        # Exercise
        temperature, precipitation = currentLoc.getGeoLocationData()

    assert temperature == 20
    assert precipitation == 5


@patch.object(currentLoc, "getIPAddress", autospec=True)
def test_getGeoLocationDataIPFailure(mock_getip):
    mock_getip.return_value = None

    # Exercise
    temperature, precipitation = currentLoc.getGeoLocationData()

    assert temperature == None
    assert precipitation == None


@patch("requests.get")
def test_getGeoLocationDataWeatherAPIStatusCodeFailure(mock_requests):
    # Setup
    with patch.object(currentLoc, "getIPAddress", autospec=True) as mock_getIP:
        mock_getIP.return_value = "127.0.0.1"

        mock_response = Mock()
        mock_response.status_code = 100
        mock_requests.return_value = mock_response

        # Exercise
        temperature, precipitation = currentLoc.getGeoLocationData()

    assert temperature == None
    assert precipitation == None


@patch("requests.get")
def test_getGeoLocationDataWeatherAPIRequestFailure(mock_requests, capsys):
    # Setup
    with patch.object(currentLoc, "getIPAddress", autospec=True) as mock_getIP:
        mock_getIP.return_value = "127.0.0.1"

        mock_requests.side_effect = requests.exceptions.RequestException(
            "Test Exception"
        )

        # Exercise
        temperature, precipitation = currentLoc.getGeoLocationData()

    assert capsys.readouterr().out == "Error with WeatherAPI: Test Exception Exiting\n"
    assert temperature == None
    assert precipitation == None


@patch("requests.get")
def test_getIPAddressSuccess(mock_requests):
    # Setup
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ip": "127.0.0.1"}
    mock_requests.return_value = mock_response

    # Exercise
    ip = currentLoc.getIPAddress()

    # Assert
    assert ip == "127.0.0.1"


@patch("requests.get", autospec=True)
def test_getIPAddressStatusCodeFailure(mock_requests):
    # Setup
    mock_response = Mock()
    mock_response.status_code = 100
    mock_requests.return_value = mock_response

    with patch.object(currentLoc, "getIPAddressBackup", autospec=True) as mock_backup:
        mock_backup.return_value = "127.0.0.2"

        # Exercise
        ip = currentLoc.getIPAddress()

    # Assert
    assert ip == "127.0.0.2"


@patch("requests.get", autospec=True)
def test_getIPAddressRequestsFailure(mock_requests, capsys):
    # Setup
    mock_requests.side_effect = requests.exceptions.RequestException("Test Exception")

    with patch.object(currentLoc, "getIPAddressBackup", autospec=True) as mock_backup:
        mock_backup.return_value = "127.0.0.2"

        # Exercise
        ip = currentLoc.getIPAddress()

    # Assert
    assert (
        capsys.readouterr().out
        == "Error with IP Info: Test Exception Moving to IP-API\n"
    )
    assert ip == "127.0.0.2"


@patch("requests.get")
def test_getIPAddressBackupSuccess(mock_requests):
    # Setup
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"query": "127.0.0.1"}
    mock_requests.return_value = mock_response

    # Exercise
    ip = currentLoc.getIPAddressBackup()

    # Assert
    assert ip == "127.0.0.1"


@patch("requests.get")
def test_getIPAddressBackupStatusCodeFailure(mock_requests):
    # Setup
    mock_response = Mock()
    mock_response.status_code = 100
    mock_requests.return_value = mock_response

    # Exercise
    ip = currentLoc.getIPAddressBackup()

    # Assert
    assert ip == None


@patch("requests.get")
def test_getIPAddressBackupRequestFailure(mock_requests, capsys):
    # Setup
    mock_requests.side_effect = requests.exceptions.RequestException("Test Exception")

    # Exercise
    ip = currentLoc.getIPAddressBackup()

    # Assert
    assert capsys.readouterr().out == "Error with IP-API: Test Exception Exiting\n"
    assert ip == None


@pytest.mark.parametrize(
    "temp, prec, output",
    [
        (12, 0, coldMessage + norainMessage),
        (12, 1, coldMessage + rainMessage),
        (16, 0, warmMessage + norainMessage),
        (16, 1, warmMessage + rainMessage),
    ],
)
def test_printMessage(temp, prec, output, capsys):
    # Exercise
    currentLoc.printMessage(temp, prec)

    # Assert
    assert capsys.readouterr().out == output
