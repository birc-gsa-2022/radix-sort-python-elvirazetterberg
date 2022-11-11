"""Radix sorting module."""
from collections import OrderedDict, deque

def count_sort(x: str) -> str:
    """Count-sort the string x.

    >>> count_sort('abaab')
    'aaabb'
    >>> count_sort('')
    ''
    """

    count = {}
    for i in range(len(x)):
        if x[i] in count:
            count[x[i]].append(i)
        else:
            count[x[i]] = [i] # {'a':[2,3]} # should only count, not append.
    
    output = ''
    count = OrderedDict(sorted(count.items()))
    for k, v in count.items():
        # for i in v:
        #     print(x[i:])
        output += k*len(v)    

    return output

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
    if len(x) != len(idx):
        return []

    count = {}
    for i in idx:
        if x[i] in count:
            count[x[i]] += 1
        else:
            count[x[i]] = 1 # {'a': 1}

    count = OrderedDict(sorted(count.items()))
    offsets = {}
    v_prev = 0
    for k, v in count.items():
        offsets[k] = v_prev
        v_prev += v

    output = [0]*len(idx)
    for i in idx:
        key = x[i]
        output[offsets[key]] = i # change 0 to index according to offset
        offsets[key] += 1

    return output

def wrapped_idx(x, suf, col):
    """ Fill conceptual suffix end spaces by rotating x after sentinel """

    return [((i + col)%len(x))+1 for i in suf] # why +1?

def lsd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a least-significant digit radix sort.

    >>> lsd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> lsd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """
    x += '0'
    idx_0 = [i for i in range(len(x))]
    idx = wrapped_idx(x, idx_0, idx_0[-1])

    for i in idx:
        idx = [(m-1)%len(idx) for m in idx]
        idx = bucket_sort(x, idx)
    
    return idx 

def bucket_sort_msd(x: str, idx: list[int], col: int) -> tuple():
    """Bucket-sort the indices in idx using keys from the string x."""

    count = {}
    # loop through suffixes in idx and count the number of each letter in the column col
    focus_index = [(i+col) if i+col<len(x) else -1 for i in idx]
    for j in focus_index:
        if x[j] in count:
            count[x[j]] += 1
        else:
            count[x[j]] = 1 # {'a': 1}

    count = OrderedDict(sorted(count.items())) # lexicographical order
    offsets = {}
    v_prev = 0
    # cumulative sum of counts
    for k, v in count.items():
        offsets[k] = v_prev
        v_prev += v

    output = [0]*len(idx)
    # loop through idx and place indexes in the correct order in output
    for i in range(len(idx)):
        # insert keys according to offsets
        key = x[focus_index[i]] # get focus key letter

        output[offsets[key]] = idx[i] # output according to suffix
        offsets[key] += 1

    if output == idx:
        col += 1
        # next column
        return bucket_sort_msd(x, output, col)
    else:
        return output, count

def bucket_idx(idx, count): # this uses count from idx[col] which may be why it's incorrect
    res = []
    temp_v = 0
    for v in count.values():
        res.append(idx[temp_v:temp_v+v])
        temp_v += v

    return res

def msd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a most-significant digit radix sort.

    >>> msd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> msd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """

    stack = deque() # lifo
    x += '0'
    curr_idx = [i for i in range(len(x))]
    res = []

    while curr_idx != []:
        idx, count = bucket_sort_msd(x, curr_idx, 0)
        buckets = bucket_idx(idx, count)
        for b in reversed(buckets):
            stack.append(b)

        curr_idx = stack.pop()
        while len(curr_idx) == 1:
            res.append(curr_idx[0])

            if len(stack) == 0:
                curr_idx = []
                break
            # go into next bucket
            curr_idx = stack.pop()

    return res


def main():
    x = 'gtgatcctcg'
    sa = msd_radix_sort(x)
    for s in sa:
        print(x[s:])

if __name__ == '__main__':
    main()