# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_

import string
import random

from radix import (
    count_sort,
    bucket_sort,
    lsd_radix_sort,
    msd_radix_sort
)


def test_count_sort() -> None:
    """Tests count_sort()."""
    assert count_sort("abaab") == "aaabb"
    assert count_sort("mississippi") == "iiiimppssss"


def test_bucket_sort() -> None:
    """Tests bucket_sort()."""
    assert bucket_sort("abaab", [0, 1, 2, 3, 4]) == [0, 2, 3, 1, 4]
    assert bucket_sort("abaab", [4, 3, 2, 1, 0]) == [3, 2, 0, 4, 1]

    assert bucket_sort(
        "mississippi",
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ) == [1, 4, 7, 10, 0, 8, 9, 2, 3, 5, 6]
    assert bucket_sort(
        "mississippi",
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ) == [10, 7, 4, 1, 0, 9, 8, 6, 5, 3, 2]


def check_suffix_array(x: str, sa: list[int]) -> None:
    """Check that the suffix array sa is sorted."""
    for i in range(1, len(sa)):
        assert x[sa[i-1]:] < x[sa[i]:]


def random_string(n: int, alpha: str = string.ascii_uppercase) -> str:
    """Create a random string."""
    return ''.join(random.choices(alpha, k=n))


def test_lsd_radix_sort() -> None:
    """Tests lsd_radix_sort()."""
    for _ in range(10):
        x = random_string(10, "acgt")
        sa = lsd_radix_sort(x)
        check_suffix_array(x, sa)


def test_msd_radix_sort() -> None:
    """Tests msd_radix_sort()."""
    for _ in range(10):
        x = random_string(10, "acgt")
        sa = msd_radix_sort(x)
        check_suffix_array(x, sa)
