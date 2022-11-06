# Radix sorting suffix arrays

In this exercise we will implement radix sorting of all suffixes of a string, with the radix sort going both right-to-left, or least-significant digit (LSD) first, and left-to-right, or most-significant digit (MSD) first. Either approach needs a bucket sort as a sub-component, though, so the first exercise concerns that.

## Bucket sorting a string

Sorting a string means arranging the letters in the string into sorted order. So, for example, if we have the string `x = abaab`, then sorting it should give us the string `aaabb`. Something like that is particularly easy, since we can handle it with a [*count sort*](https://en.wikipedia.org/wiki/Counting_sort).

**Exercise:** Our warm-up exercises is to implement a function, `count_sort(x)` that gives us the characters in `x` back in sorted order.

A count sort reduces all the information in the input to just the keys, in this case the letters in the string, but for a radix sort it won't quite suffice. We will need to rearrange the suffixes of `x`, where the suffixes are represented as indices into the string. If we have the suffixes

```
x[0:] = abaab
x[1:] = baab
x[2:] = aab
x[3:] = ab
x[4:] = b
```

and you get the string `aaabb` back, you don't know which of the three a-suffixes comes first, second, or third, and we need that information.

Instead of thinking of `x` just as a string, we need to think of it as the indices `0, 1, ..., len(x)-1` where each index `i` has a key, `key(i) = x[i]`, which is the letter at that index. We don't want to sort the letters in `x`; we want to sort the indices with respect to the keys.

Furthermore, we want the sort to be stable, or at least we need that property for the least-significant digit radix sort, and this means that if we have two values in the input with the same key, then the value that comes first will also come first in the output.

**Exercise:** You should implement a function, `bucket_sort(x, idx)`, that returns the indices in `idx` stable-sorted with respect to the keys in `x`. If we take the indices in the order they appear in `x`, so `idx = [0, 1, 2, 3, 4]`, then we want the output `[0, 2, 3, 1, 4]`. At these indices we still get the sorted string `aaabb`, but we now know that index `0` comes before indices `2` and `3`, with the same key, because it came before them in the inmput. Index `1` also came before `2` and `3`, of course, but it has a higher key, so it follows them, but comes before index `4` with the same key, since index `1` came before `4`.

If the input indices had been `[2, 3, 4, 1, 0]` instead, then we would have the output `[2, 3, 0, 4, 1]`, which would still be the same sequence of keys, `aaabb`, but the letters would be from different indices in `x`.

(You don't have to use the indices `0, 1, ..., len(x)-1` for this to work, but that is what we have when we sort the suffixes, so we will stick to that).

The easiest way to implement this kind of bucket sort, but by no means the only, is a variant called [histogram sort](https://en.wikipedia.org/wiki/Bucket_sort#Histogram_sort). First, scan through `x` and count how often you see each character. You already did that with `count_sort(x)` so that should be simple enough. Put those counts in a table or array. For `x = abaab` you have three `a`s and two `b`s, so the table could look like `[a: 3, b: 2]`.

Now, compute the cummulative sun of the table, i.e., make a new table where for key `k` you have the number of letters with keys `k'` smaller than `k`. With our example `x`, `a` is the smallest key so there are no elements with a smaller key, and therefore `a` should map to zero, `[a: 0, ...]`. The keys smaller than `b` are `a` (there is only one here) and there are three occurrences of `a`, so `b` should map to three, `[a: 0, b: 3]`.

Call this table the "buckets" `buckets = [a: 0, b: 3]`.

Use this new table as offsets into the output. A key is mapped to the offset where the bucket for that key starts. For `x = abaab` we have

```
a: 0 -> out[0]
        out[1]
        out[2]
b: 3 -> out[3]
        out[4]
```

Now, run through your input indices, say `i` in `[0, 1, 2, 3, 4]`, get the key for the index `key(i) = x[i]` and then get the bucket for that key: `buckets[x[i]]`. That is the offset in the output where you want to put index `i`.

For `i = 0` and the buckets table from above, we have the key `x[0] = a` so we need to put `i = 0` at index `buckets[a] = 0`.

```
a: 0 -> out[0] = 0
        out[1]
        out[2]
b: 3 -> out[3]
        out[4]
```

Now that we have used this slot in the output, we update the `buckets` table to reflect this by incrementing `buckets[a] += 1`.

```
        out[0] = 0
a: 1 -> out[1]
        out[2]
b: 3 -> out[3]
        out[4]
```

The next index we encounter, if we run through the indices in order, is `i = 1`. Here the key is `key(1) = x[1] = b` and `buckets[b] = 3`, so we insert index `1` there, and increment the bucket pointer to reflect this.

```
        out[0] = 0
a: 1 -> out[1]
        out[2]
        out[3] = 1
b: 3 -> out[4]
```

Then we get to index `2` with key `a` so we insert index `2` at index `bucket[a]` and update the bucket counter.

```
        out[0] = 0
        out[1] = 2
a: 1 -> out[2]
        out[3] = 1
b: 3 -> out[4]
```

If you continue this through all the indices you end up with this

```
        out[0] = 0
        out[1] = 2
        out[2] = 3
a: 3 -> out[3] = 1
        out[4] = 4
b: 5 -> 
```

where the indices are (stable) sorted with respect to their keys.



## Indexing into suffixes

Radix sort is all about sorting one column at a time, using a bucket sort, but what does a "column" mean, when all the suffixes have different lengths? Let's say you have the string `x = abaab` and you want to make a suffix array out of it (or rather, a suffix array of `abaab$` because we will always make suffix arrays that include the sentinel, whether it is explictitly part of `x` or not). The suffixes of x are

```
x[0:] = abaab
x[1:] = baab
x[2:] = aab
x[3:] = ab
x[4:] = b
x[5:] =
```

or, if you prefer to have the sentinel explicitly:

```
x[0:] = abaab$
x[1:] = baab$
x[2:] = aab$
x[3:] = ab$
x[4:] = b$
x[5:] = $
```

If you, for example, look at column 2, you have

```
x[0+2] = ..a..
x[1+2] = ..a.
x[2+2] = ..b
x[3+2] = ..
x[4+2] = .
x[5+2] =
```

where the last three have us index ouf of bounds (or last two if we explicitly include the sentinel, in which case `x[3+2] = $`).

How do we get keys for the bucket sort, when not all rows will immidiately have them?

We want some kind of function `key(suf,col)` that gives us the key for suffix `suf` for column `col`. When there is a letter at that row and column, we want that, of course, so if `suf + col < len(x)`, we want `x[suf+col]`. The question is, what should `key(suf,col)` return if `suf + col >= len(x)`?

There are two straight-forward solutions to this: 1) padding with sentinels, or 2) rotating `x`.

If we are padding, we implicitly assume that all the columns have length `n` because the suffixes are padded with the sentinel at the end:

```
x[0:] = abaab
x[1:] = baab$
x[2:] = aab$$
x[3:] = ab$$$
x[4:] = b$$$$
x[5:] = $$$$$
```

(There is no sentinel in the first row here, because we don't need it for this trick to work, but you could add it if you want to. I'll leave that as an exercise).

We don't need to ever create these strings (although we could within the O(n²) time we need for radix sorting anyway); we can handle it implicitly with the `key(suf,col)` function:

```
key(x, suf, col) = 
    if   suf + col < len(x) 
    then x[suf+col] 
    else '$'
```

(where you probably want to use zero instead of the character `$`).

The rotation approach is simply noticing that if you have the sentinel in your string, then the suffixes

```
x[0:] = abaab$
x[1:] = baab$
x[2:] = aab$
x[3:] = ab$
x[4:] = b$
x[5:] = $
```

will be sorted the same as the corresponding rotatoins

```
x[0:] + $ + x[:0] = abaab$
x[1:] + $ + x[:1] = baab$a
x[2:] + $ + x[:2] = aab$ab
x[3:] + $ + x[:3] = ab$aba
x[4:] + $ + x[:4] = b$abaa
x[5:] + $ + x[:5] = $abaab
```

If you compare any two suffixes, you will never need to scan past the unique sentinel, and if you reach a sentinel the shorter string is considered smaller as the sentinel is considered smaller than any other character.

So, if `x' = x$` is the string with the sentinel added--it might be the string you started out with in the first place--then you can index into it but wrap around the length of `x'`.

```
  .---- col 2
  v
abaab$ ; suf = 0, col = 2, (suf + col) mod 6 = 2: ab[a]ab$
baab$a ; suf = 1, col = 2, (suf + col) mod 6 = 3: aba[a]b$
aab$ab ; suf = 2, col = 2, (suf + col) mod 6 = 4: abaa[b]$
ab$aba ; suf = 3, col = 2, (suf + col) mod 6 = 5: abaab[$]
b$abaa ; suf = 4, col = 2, (suf + col) mod 6 = 0: [a]baab$
$abaab ; suf = 5, col = 2, (suf + col) mod 6 = 1: a[b]aab$
```

Your `key` function could then look like this:

```
key(x, suf, col) =
    x'[(suf + col) mod len(x')]
```

One approach isn't better than the other, and you can pick your favorite, but the first avoids creating a new string by appending the sentinel, in cases where you don't already have it.

## Least-significant digit first radix sort

To sort our suffixes from right to left, there really isn't much more to it. You iteratively bucket-sort the suffix indices, starting with the last column in your input (which is either `len(x)-1` or `len(x)` depending on whether you choose to explicitly add a sentinel to `x` and use the padding or rotation trick). E.g. it could look somewhat like this:

```
lsd_radix_sort(x) =
    idx = [0, 1, ..., len(x) - 1]
    for col in [len(x) - 1, ..., 1, 0]:
       idx = bucket_sort idx with respect to column col
    return idx
```

**Exercise:** Implement the function `lsd_radix_sort(x)` that returns the sorted suffix indices of `x`.

## Most-significant digit first radix sort

If you want to do the same thing, but going through the columns from left to right (`col in [0, 1, ..., len(x) - 1]`) you might be able to terminate early, if you can see that all the rows are sorted, but you can no longer sort entire columns at a time.

Imagine that we start with

```
x[0:] = abaab
x[1:] = baab$
x[2:] = aab$$
x[3:] = ab$$$
x[4:] = b$$$$
x[5:] = $$$$$
```

and sort the rows according to the first column

```
x[5:] = $$$$$
x[0:] = abaab
x[2:] = aab$$
x[3:] = ab$$$
x[1:] = baab$
x[4:] = b$$$$
```

So far so good, but now sort the rows with respect to the second column:

```
x[5:] = $$$$$
x[4:] = b$$$$
x[2:] = aab$$
x[1:] = baab$
x[0:] = abaab
x[3:] = ab$$$
```

Now we have messed up the order we got the rows in when sorting the first column.

Instead, you need sort within ever more separated buckets. After the first column, we have a bucket for each letter:

```
$: x[5:] = $$$$$

a: x[0:] = abaab
   x[2:] = aab$$
   x[3:] = ab$$$

b: x[1:] = baab$
   x[4:] = b$$$$
```

and you need to sort within these buckets to preserve the first order

```
$: $: x[5:] = $$$$$
   a:
   b:

a: $:
   a: x[2:] = aab$$
   b: x[0:] = abaab
      x[3:] = ab$$$

b: $: x[4:] = b$$$$
   a:
   b: x[1:] = baab$
```

and from here, you need to split the new buckets into even smaller segments.

The benefit of this approach is that you can terminate a recursion when a bucket is empty or contain a single element, the drawback is that you have more book keeping to do.

**Exercise:** Implement the function `msd_radix_sort(x)` that returns the sorted suffix indices of `x`.

You can implement this using recursion, but in a real application, you might not have sufficint stack space to handle long sequences, so it is better to avoid direct recursion and to use an explicit stack.
