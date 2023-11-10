import main
from unittest.mock import Mock, patch
from datetime import datetime


@patch("builtins.input", side_effect=["1", "3"])
def test_consoleUIInput1Success(mock_input):
    # Setup
    with patch.object(
        main.currentLoc, "getGeoLocationData", autospec=True
    ) as mock_getData:
        mock_getData.return_value = (25, 0)

        # Exercise
        mainReturn = main.main()

    # Assert
    assert mainReturn == 0


@patch("builtins.input", side_effect=["1"])
def test_consoleUIInput1Failure(mock_input):
    # Setup
    with patch.object(
        main.currentLoc, "getGeoLocationData", autospec=True
    ) as mock_getData:
        mock_getData.return_value = (None, None)

        # Exercise
        mainReturn = main.main()

    # Assert
    assert mainReturn == 1


@patch("builtins.input", side_effect=["2", "3"])
def test_consoleUIInput2Success(mock_input):
    # Setup
    with patch.object(main.futureLoc, "getFutureInfo", autospec=True) as mock_getInfo:
        mock_getInfo.return_value = ("MLA", datetime(2023, 10, 25))

        with patch.object(
            main.futureLoc, "getFutureLocData", autospec=True
        ) as mock_getData:
            mock_getData.return_value = (25, 0)

            # Exercise
            mainReturn = main.main()

    # Assert
    assert mainReturn == 0


@patch("builtins.input", side_effect=["2"])
def test_consoleUIInput2Failure(mock_input):
    # Setup
    with patch.object(main.futureLoc, "getFutureInfo", autospec=True) as mock_getInfo:
        mock_getInfo.return_value = ("MLA", datetime(2023, 10, 25))

        with patch.object(
            main.futureLoc, "getFutureLocData", autospec=True
        ) as mock_getData:
            mock_getData.return_value = (None, None)

            # Exercise
            mainReturn = main.main()

    # Assert
    assert mainReturn == 2


@patch("builtins.input", side_effect=["3"])
def test_consoleUIInput3(mock_input, capsys):
    # Exercise
    mainReturn = main.main()

    # Assert
    assert capsys.readouterr().out[-25:] == "Exiting the programme...\n"
    assert mainReturn == 0


@patch(
    "builtins.input",
    side_effect=[
        "123",
        "0",
        "4",
        "testing",
        "3",
    ],
)
def test_consoleUIInvalidInput(mock_input):
    # Exercise
    mainReturn = main.main()

    # Assert
    assert mainReturn == 0
