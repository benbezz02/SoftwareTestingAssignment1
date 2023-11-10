from src.weather import weather


def test_isColdTemperature14():
    assert weather.isCold(14) == True


def test_isColdTemperature15():
    assert weather.isCold(15) == True


def test_isColdTemperature16():
    assert weather.isCold(16) == False


def test_isRainyPrecipitation0():
    assert weather.isRainy(0) == False


def test_isRainyPrecipitation1():
    assert weather.isRainy(1) == True
