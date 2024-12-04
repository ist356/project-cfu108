import pytest
from datetime import datetime
import time
from code.grab import fetch_stock_data
from code.parse import parse_stock_data

@pytest.fixture
def valid_dates():
    """Fixture to provide valid start and end times for testing."""
    start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2024-12-01", "%Y-%m-%d")
    start_time = int(time.mktime(start_date.timetuple()))
    end_time = int(time.mktime(end_date.timetuple()))
    return start_time, end_time

@pytest.fixture
def mock_api_response():
    """Fixture to provide a mock API response for testing."""
    return {
        "chart": {
            "result": [
                {
                    "timestamp": [1717387200, 1717473600],
                    "indicators": {
                        "quote": [
                            {"close": [150.0, 152.0]}
                        ]
                    }
                }
            ]
        }
    }

def test_fetch_stock_data(valid_dates):
    """Test the fetch_stock_data function."""
    start_time, end_time = valid_dates
    data = fetch_stock_data("AAPL", start_time, end_time)
    assert "chart" in data, "API response missing 'chart' key"
    assert "result" in data["chart"], "API response missing 'result' key"

def test_parse_stock_data(mock_api_response):
    """Test the parse_stock_data function."""
    df = parse_stock_data(mock_api_response)
    assert not df.empty, "Parsed DataFrame is empty"
    assert "Date" in df.columns, "'Date' column is missing"
    assert "Close" in df.columns, "'Close' column is missing"
    assert len(df) == 2, "Parsed DataFrame has incorrect number of rows"
    assert df['Close'][0] == 150.0, "First close price is incorrect"

def test_invalid_fetch_stock_data():
    """Test fetch_stock_data with invalid inputs."""
    with pytest.raises(Exception) as excinfo:
        fetch_stock_data("INVALID", 0, 0)
    assert "Failed to fetch data" in str(excinfo.value), "Invalid symbol not handled correctly"
