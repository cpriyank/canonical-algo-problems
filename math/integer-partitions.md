# Integer partitions

A "partition" is a way of representing a given integer as a sum of zero or
more positive integers, e.g. the partitions of 4 are 1+1+1+1, 1+1+2, 2+2,
1+3, and 4. This recipe uses simple generators recursively to produce
a stream of all partitions of its argument. Each partition is represented as
a sorted list of the numbers to be summed, e.g. `[1,1,1,1], [1,1,2], [2,2], [1,3], [4].`

This function is due to [David Eppstein](http://code.activestate.com/recipes/218332-generator-for-integer-partitions/)

If you have a partition of n, you can reduce it to a partition of n-1 in
a canonical way by subtracting one from the smallest item in the partition.
E.g. 1+2+3 => 2+3, 2+4 => 1+4. This algorithm reverses the process: for each
partition p of n-1, it finds the partitions of n that would be reduced to
p by this process. Therefore, each partition of n is output exactly once, at
the step when the partition of n-1 to which it reduces is considered.

```python
def partitions(n):
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return

    # modify partitions of n-1 to form partitions of n
    for part in partitions(n - 1):
        yield [1] + part
        if part and (len(part) < 2 or part[1] > part[0]):
            yield [part[0] + 1] + part[1:]

# In [6]: for p in partitions(5):
#    ...:     print(p)
#    ...:
#    ...:
# [1, 1, 1, 1, 1]
# [1, 1, 1, 2]
# [1, 2, 2]
# [1, 1, 3]
# [2, 3]
# [1, 4]
# [5]

# Reverse order variation due to George Yoshida
def partitions_rev(n):
    # reverse order
    if n == 0:
        yield []
        return

    for part in partitions_rev(n - 1):
        yield part + [1]
        if part and (len(part) < 2 or part[-2] > part[-1]):
            yield part[:-1] + [part[-1] + 1]

# In [5]: for p in partitions_rev(5):
#    ...:     print(p)
#    ...:
# [1, 1, 1, 1, 1]
# [2, 1, 1, 1]
# [2, 2, 1]
# [3, 1, 1]
# [3, 2]
# [4, 1]
# [5]
```

Another variation in the same activestate thread due to Tim Peters:

Sometimes I do need speed, and then a multiset representation allows several
efficiences, such as O(1) time per iteration (not just amortized O(1)), and
compactness (the largest data structure constructed takes O(sqrt(N)) space;
the important part of that is there's so much less the partition _consumer_
needs to examine each time -- something to remember next time you find your
code endlessly crawling over long strings of ones):

note: see especially how he creates multisets using sorted list of keys and
a dict of values

```python
def gen_partitions_ms(n):
    """Generate all partitions of integer n (>= 0).

    Each partition is represented as a multiset, i.e. a dictionary
    mapping an integer to the number of copies of that integer in
    the partition.  For example, the partitions of 4 are {4: 1},
    {3: 1, 1: 1}, {2: 2}, {2: 1, 1: 2}, and {1: 4}.  In general,
    sum(k * v for k, v in a_partition.iteritems()) == n, and
    len(a_partition) is never larger than about sqrt(2*n).

    Note that the _same_ dictionary object is returned each time.
    This is for speed:  generating each partition goes quickly,
    taking constant time independent of n.
    """

    if n < 0:
        raise ValueError("n must be >= 0")

    if n == 0:
        yield {}
        return

    ms = {n: 1}
    keys = [n]  # ms.keys(), from largest to smallest
    yield ms

    while keys != [1]:
        # Reuse any 1's.
        if keys[-1] == 1:
            del keys[-1]
            reuse = ms.pop(1)
        else:
            reuse = 0

        # Let i be the smallest key larger than 1.  Reuse one
        # instance of i.
        i = keys[-1]
        newcount = ms[i] = ms[i] - 1
        reuse += i
        if newcount == 0:
            del keys[-1], ms[i]

        # Break the remainder into pieces of size i-1.
        i -= 1
        q, r = divmod(reuse, i)
        ms[i] = q
        keys.append(i)
        if r:
            ms[r] = 1
            keys.append(r)

        yield ms
```

An approach by user [skovorodkin](https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning)

```python
def partitions_so(n, I=1):
    yield (n,)
    for i in range(I, n//2 + 1):
        for p in partitions_so(n-i, i):
            yield (i,) + p
```

Finally, the most efficient algorithm by [Jerome Kelleher for his PhD thesis](http://jeromekelleher.net/tag/integer-partitions.html)

## Iterative Algorithm

Lets take a look at one algorithm to generate all ascending compositions.
This algorithm is written as a Python generator, which is a very neat way of
writing combinatorial generation algorithms.

```python
def rule_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    a[1] = n
    while k != 0:
        x = a[k - 1] + 1
        y = a[k] - 1
        k -= 1
        while x <= y:
            a[k] = x
            y -= x
            k += 1
        a[k] = x + y
        yield a[:k + 1]
```

Although this algorithm is very simple, it is also very efficient. It is
Constant Amortised Time, which means that the average computation per
partition that is output is constant.

We can prove this fairly easily by looking at the two while loops and the
variable k.

Since the yield operator is called exactly once for every
iteration of the outer while loop, we know that it must iterate exactly p(n)
times (where p(n) is the number of partitions of n. Therefore, we know
that there must be exactly p(n) decrement operations on k (since k -= 1 is
only called in the outer loop). Then, since k is initially 1 and the
algorithm terminates when k is 0, we know that there must be p(n) - 1
increment operations on k. Since the only increment operations occur in the
inner while loop, we know that this loop gets executed exactly p(n) - 1
times, and so the total running time of the algorithm is proportional to
p(n). In other words, the algorithm is constant amortised time.

## Most Efficient Algorithm

If it's speed you're looking for, here is the most efficient known algorithm
to generate all partitions of a positive integer.

```python
def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]
```

This algorithm is a modification of the algorithm above. It gains its extra
efficiency by using some structure of the set of ascending compositions to
make many transitions more efficient. Consider, for example, the following of
partitions of 10:

```
1 + 1 + 2 + 6
1 + 1 + 3 + 5
1 + 1 + 4 + 4
```

These transitions can be made very efficiently, since all we need to do is to
add one to the second last part and subtract one from the last part.