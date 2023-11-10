from src.futureLoc import futureLoc
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import requests

infoMessage = "On the 10/25/23 at MLA airport: \n"
coldMessage = "It will be cold so you should wear warm clothing.\n"
warmMessage = "It will be warm so you should wear light clothing.\n"
rainMessage = "It is likely to rain so you do need an umbrella.\n\n"
norainMessage = "It is likely to not rain so you don't need an umbrella.\n\n"


@patch("builtins.input", side_effect=["MLA", datetime.today().strftime("%Y-%m-%d")])
def test_getFututreInfoValidInputs(mock_input):
    # Exercise
    airport_out, date_out = futureLoc.getFutureInfo()

    # Assert
    assert airport_out == "MLA"
    assert date_out.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")


@patch(
    "builtins.input",
    side_effect=[
        "123",
        "airport",
        "MLA",
        "2023-10-25",
        "2024-10-26",
        datetime.today().strftime("%Y-%m-%d"),
    ],
)
def test_getFututreInfoInValidInputs(mock_input):
    # Exercise
    airport_out, date_out = futureLoc.getFutureInfo()

    # Assert
    assert airport_out == "MLA"
    assert date_out.strftime("%Y-%m-%d") == datetime.today().strftime("%Y-%m-%d")


@patch("requests.get")
def test_getFutureLocDataSuccess(mock_requests):
    # Setup
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "forecast": {
            "forecastday": {0: {"day": {"avgtemp_c": 12, "totalprecip_mm": 0}}}
        }
    }
    mock_requests.return_value = mock_response

    # Exercise
    temp, prec = futureLoc.getFutureLocData(
        "MLA", datetime.today().strftime("%Y-%m-%d")
    )

    # Assert
    assert temp == 12
    assert prec == 0


@patch("requests.get")
def test_getFutureLocDataStatusCodeFailure(mock_requests):
    # Setup
    mock_response = Mock()
    mock_response.status_code = 100
    mock_requests.return_value = mock_response

    # Exercise
    temp, prec = futureLoc.getFutureLocData(
        "MLA", datetime.today().strftime("%Y-%m-%d")
    )

    # Assert
    assert temp == None
    assert prec == None


@patch("requests.get")
def test_getFutureLocDataRequestFailure(mock_requests, capsys):
    # Setup
    mock_requests.side_effect = requests.exceptions.RequestException("Test Exception")

    # Exercise
    temp, prec = futureLoc.getFutureLocData(
        "MLA", datetime.today().strftime("%Y-%m-%d")
    )

    # Assert
    assert capsys.readouterr().out == "Error with WeatherAPI: Test Exception Exiting\n"
    assert temp == None
    assert prec == None


@pytest.mark.parametrize(
    "loc, date, temp, prec, output",
    [
        (
            "MLA",
            datetime(2023, 10, 25),
            12,
            0,
            infoMessage + coldMessage + norainMessage,
        ),
        ("MLA", datetime(2023, 10, 25), 12, 1, infoMessage + coldMessage + rainMessage),
        (
            "MLA",
            datetime(2023, 10, 25),
            16,
            0,
            infoMessage + warmMessage + norainMessage,
        ),
        ("MLA", datetime(2023, 10, 25), 16, 1, infoMessage + warmMessage + rainMessage),
    ],
)
def test_printMessage(loc, date, temp, prec, output, capsys):
    # Exercise
    futureLoc.printMessage(loc, date, temp, prec)

    # Assert
    assert capsys.readouterr().out == output
