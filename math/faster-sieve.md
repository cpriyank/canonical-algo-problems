# Computes an infinite sequence of primes using simple generators.

A Python dictionary is used to mark multiples of the generated primes, according to the Sieve of Eratosthenes.

```python
# Sieve of Eratosthenes
# David Eppstein, UC Irvine, 28 Feb 2002
# Slightly modified by Priyank Chaudhary to use defaultdict

from __future__ import generators
from collections import defaultdict

def eratosthenes():
	'''Yields the sequence of prime numbers via the Sieve of Eratosthenes.'''
	prime_factors = defaultdict(list)  # map composite integers to primes witnessing their compositeness
	q = 2   # first integer to test for primality
	while True:
		if q not in prime_factors:
			yield q        # not marked composite, must be prime
			prime_factors[q*q] = [q]   # first multiple of q not already marked
		else:
			for prime in prime_factors[q]: # move each witness to its next multiple
				prime_factors[prime+q].append(prime)
			del prime_factors [q]       # no longer need D[q], free memory
		q += 1
```
