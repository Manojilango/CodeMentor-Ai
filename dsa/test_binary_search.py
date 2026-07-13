from binary_search import binary_search

def test_finds_existing_value():
    nums = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search(nums, 7) == 3

def test_value_not_in_array():
    nums = [1, 3, 5, 7, 9, 11, 13]
    assert binary_search(nums, 4) == -1

def test_empty_array():
    assert binary_search([], 5) == -1

def test_single_element_found():
    assert binary_search([5], 5) == 0

def test_single_element_not_found():
    assert binary_search([5], 3) == -1

def test_first_element():
    nums = [1, 3, 5, 7, 9]
    assert binary_search(nums, 1) == 0

def test_last_element():
    nums = [1, 3, 5, 7, 9]
    assert binary_search(nums, 9) == 4
