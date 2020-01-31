import pytest
from cache import LRUCache, CacheInitializationError


def test_raises_exception_on_non_int_args():
    with pytest.raises(CacheInitializationError):
        LRUCache(1.5)


def test_raises_exception_on_invalid_int_args():
    with pytest.raises(CacheInitializationError):
        LRUCache(0)


def test_create_cache():
    cache = LRUCache(1)
    assert cache.nmemb == 1 and len(cache.members) == 0


@pytest.fixture
def two_element_cache():
    cache = LRUCache(2)
    cache[0] = "foo"
    cache[1] = "bar"
    return cache


def test_cache_getitem(two_element_cache):
    assert two_element_cache[0] == "foo" and two_element_cache[1] == "bar"


def test_cache_setitem(two_element_cache):
    two_element_cache[0] = "baz"
    two_element_cache[1] = "qux"
    assert two_element_cache[0] == "baz" and two_element_cache[1] == "qux"


def test_getting_non_member_raises_exception(two_element_cache):
    with pytest.raises(KeyError):
        two_element_cache[2]


@pytest.fixture
def four_element_cache():
    cache = LRUCache(4)
    cache["a"] = 1
    cache["b"] = 2
    cache["c"] = 3
    cache["d"] = 4
    return cache


def test_new_members_replace_old_ones_when_full(four_element_cache):
    four_element_cache["e"] = 5
    assert len(four_element_cache.members) == 4
    assert four_element_cache["e"] == 5
    assert four_element_cache["b"] == 2


def test_lru_item_gets_evicted_first(four_element_cache):
    four_element_cache["e"] = 5
    with pytest.raises(KeyError):
        four_element_cache["a"]


def test_last_fetched_item_is_evicted_last(four_element_cache):
    _ = four_element_cache["c"]
    four_element_cache["e"] = 5
    four_element_cache["f"] = 6
    four_element_cache["g"] = 7
    assert four_element_cache["c"] == 3


def test_last_set_item_is_evicted_last(four_element_cache):
    four_element_cache["b"] = 4
    four_element_cache["e"] = 5
    four_element_cache["f"] = 6
    four_element_cache["g"] = 7
    assert four_element_cache["b"] == 4
