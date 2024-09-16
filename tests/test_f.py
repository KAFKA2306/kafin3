import pytest
from unittest.mock import patch
import streamlit as st
from src.frontend.streamlit_app import run_analysis

@pytest.mark.parametrize("query,expected", [
    ("GAFA Stock Performance YTD", "GAFA Stock Performance"),
    ("USD/JPY vs Nikkei 225 Correlation", "USD/JPY"),
])
def test_run_analysis(query, expected):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"message": expected}
        result = run_analysis(query)
        assert expected in result

@pytest.mark.parametrize("query", ["", None])
def test_invalid_query(query):
    with pytest.raises(ValueError):
        run_analysis(query)

# 他のテストケースを追加...
