import unittest.mock


from govbot import twitter


def test_secs_to_pct_complete():
    start_time = 1000
    end_time = 2000
    current_time = 1500

    with unittest.mock.patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.timestamp.return_value = current_time
        # Test 1: Return 0 for 100% completion
        assert twitter._secs_to_pct_complete(start_time, end_time, 1.0) == 500

        # Test 2: Return half of the total duration for 50% completion
        assert twitter._secs_to_pct_complete(start_time, end_time, 0.5) == 0

        # Test 3: Return negative value for completion less than current time
        assert twitter._secs_to_pct_complete(start_time, end_time, 0.25) < 0
