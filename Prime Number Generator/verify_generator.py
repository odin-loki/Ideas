#!/usr/bin/env python3
"""
verify_generator.py
═══════════════════

End-to-end correctness and performance audit of the prime generator across
many scales.  At each scale we:

  1. Generate N primes starting from a fixed offset.
  2. Verify every output is a true prime via sympy.isprime() (independent
     reference implementation).
  3. Verify every output is the *next* prime after the previous output
     (no skips), via sympy.nextprime() — only for small/medium scales
     where this is tractable.
  4. Measure mean prime gap and compare to the PNT expectation ln(n).
  5. Time per prime.

Outputs:
    verify_generator.json
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
from sympy import isprime, nextprime

from prime_generator import MetaPatternPrimeGenerator


SCALES = [
    ("tiny",        2,                  50,  True),
    ("small",       100,                50,  True),
    ("small-mid",   1_000,              50,  True),
    ("medium",      10_000,             50,  True),
    ("medium-hi",   100_000,            50,  True),
    ("large",       1_000_000,          30,  True),
    ("large-hi",    10_000_000,         20,  False),
    ("very-large",  100_000_000,        15,  False),
    ("xl",          1_000_000_000,      10,  False),
    ("xxl",         10**12,             6,   False),
]


def audit(gen, label, start, count, verify_no_skip):
    t0 = time.perf_counter()
    primes = gen.generate_n_primes(start, count)
    elapsed = time.perf_counter() - t0

    all_prime = all(isprime(int(p)) for p in primes)

    no_skip = None
    skipped_examples = []
    if verify_no_skip:
        no_skip = True
        prev = int(start) - 1  # nextprime(0) = 2 in sympy, which is what we want
        for p in primes:
            true_next = int(nextprime(prev))
            if int(p) != true_next:
                no_skip = False
                if len(skipped_examples) < 5:
                    skipped_examples.append({
                        "after": prev,
                        "true_next": true_next,
                        "got": int(p),
                    })
            prev = int(p)

    arr = np.asarray([int(p) for p in primes], dtype=np.int64)
    gaps = np.diff(arr) if len(arr) >= 2 else np.array([0])
    expected_gap = math.log(int(start))

    return {
        "label": label,
        "start": int(start),
        "count": count,
        "elapsed_sec": elapsed,
        "ms_per_prime": 1000.0 * elapsed / max(count, 1),
        "all_prime": bool(all_prime),
        "no_skip": no_skip,
        "skipped_examples": skipped_examples,
        "first_5_primes": [int(p) for p in primes[:5]],
        "last_5_primes": [int(p) for p in primes[-5:]],
        "mean_gap": float(np.mean(gaps)) if len(gaps) > 0 else None,
        "expected_gap_ln_n": expected_gap,
        "min_gap": int(np.min(gaps)) if len(gaps) > 0 else None,
        "max_gap": int(np.max(gaps)) if len(gaps) > 0 else None,
    }


if __name__ == "__main__":
    np.random.seed(42)
    gen = MetaPatternPrimeGenerator()

    print(f"{'label':>12s}  {'start':>15s}  {'count':>5s}  "
          f"{'all_prime':>9s}  {'no_skip':>7s}  "
          f"{'mean_gap':>10s}  {'ln(n)':>10s}  "
          f"{'ms/prime':>10s}")
    print("-" * 105)

    results = []
    for label, start, count, verify_no_skip in SCALES:
        r = audit(gen, label, start, count, verify_no_skip)
        results.append(r)
        no_skip_str = ("yes" if r["no_skip"] else "NO!") if r["no_skip"] is not None else "skip"
        print(f"{r['label']:>12s}  {r['start']:>15,d}  {r['count']:>5d}  "
              f"{('yes' if r['all_prime'] else 'NO!'):>9s}  "
              f"{no_skip_str:>7s}  "
              f"{(r['mean_gap'] or 0):>10.2f}  {r['expected_gap_ln_n']:>10.2f}  "
              f"{r['ms_per_prime']:>10.3f}")

        if r["no_skip"] is False:
            print(f"               ! skipped-prime examples: {r['skipped_examples']}")

    out = {"scales": results}
    Path("verify_generator.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print()
    print(f"Wrote verify_generator.json")

    n_correct = sum(1 for r in results if r["all_prime"])
    n_no_skip = sum(1 for r in results if r["no_skip"] is True)
    n_skip_checks = sum(1 for r in results if r["no_skip"] is not None)
    print(f"All-prime checks: {n_correct} / {len(results)} scales")
    print(f"No-skip checks:   {n_no_skip} / {n_skip_checks} scales (where verifiable)")
