import pandas as pd
import pytest
from src.generators.watchlist import generate_watchlist

def test_watchlist_generator():
    with pytest.raises(TypeError):
        generate_watchlist(True)

def test_watchlist_generator_participating_count_type():
    with pytest.raises(TypeError):
        generate_watchlist(participating_count=False)

def test_watchlist_generator_seed_type():
    with pytest.raises(TypeError):
        generate_watchlist(seed="42")

def test_watchlist_reporting_month_type():
    with pytest.raises(TypeError):
        generate_watchlist(reporting_month=112026)
