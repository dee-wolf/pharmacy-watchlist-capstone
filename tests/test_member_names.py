import pytest
from src.generators.member_names import generate_member_names

def test_generate_member_names():
    result = generate_member_names()
    assert len(result) == 1000

def test_generate_member_names_custom_num():
    result = generate_member_names(num_members=25)
    assert len(result) == 25

def test_generate_member_names_seed_reproducibility():
    result1 = generate_member_names(num_members=25, seed=69)
    result2 = generate_member_names(num_members=25, seed=69)
    assert list(result1) == list(result2)

def test_generate_member_names_unique_names():
    result = generate_member_names()
    assert len(result) == len(set(result))

def test_generate_member_names_num_mem_type_error():
    with pytest.raises(TypeError):
        generate_member_names(num_members="1000")

def test_generate_member_names_num_mem_value_error():
    with pytest.raises(ValueError):
        generate_member_names(num_members=-10)

def test_generate_member_names_num_mem_zero_error():
    with pytest.raises(ValueError):
        generate_member_names(num_members=0)

def test_generate_member_names_seed_bool():
    with pytest.raises(TypeError):
        generate_member_names(seed=True)

def test_generate_member_names_seed_string():
    with pytest.raises(TypeError):
        generate_member_names(seed="42")

def test_generate_member_names_max_names():
    with pytest.raises(ValueError):
        generate_member_names(num_members=2101)
