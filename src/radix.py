"""Radix sorting module."""


def count_sort(x: str) -> str:
    """Count-sort the string x.

    >>> count_sort('abaab')
    'aaabb'
    >>> count_sort('')
    ''
    """
    return ""


def bucket_sort(x: str, idx: list[int]) -> list[int]:
    """Bucket-sort the indices in idx using keys from the string x.

    Must have len(x) == len(idx).

    >>> bucket_sort('abaab', [0, 1, 2, 3, 4])
    [0, 2, 3, 1, 4]
    >>> bucket_sort('abaab', [4, 3, 2, 1, 0])
    [3, 2, 0, 4, 1]
    >>> bucket_sort('', [])
    []
    """
    return []


def lsd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a least-significant digit radix sort.

    >>> lsd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> lsd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """
    return []


def msd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a most-significant digit radix sort.

    >>> msd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> msd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """
    return []
