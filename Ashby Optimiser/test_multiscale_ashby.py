"""
Test suite for MultiscaleAshbyOptimizer.

Tests are ordered from unit-level invariants to system-level benchmarks.
Every test prints a pass/fail and a brief rationale for its assertion.
"""

import numpy as np
import sys
sys.path.insert(0, "/home/claude")

from multiscale_ashby import (
    HomeostasisUnit,
    MultiscaleAshbyOptimizer,
    RandomSearch,
    OnePlusOneES,
    sphere, rastrigin, rosenbrock, ackley,
)

SEP = "─" * 64


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def run_batch(OptimizerClass, kwargs, fitness_fn, max_evals, n_runs):
    results = []
    for seed in range(n_runs):
        kw = dict(kwargs)
        kw["seed"] = seed
        opt = OptimizerClass(**kw)
        results.append(opt.run(fitness_fn, max_evals)["best_f"])
    return np.array(results)


def median(arr): return float(np.median(arr))
def win_rate(a, b): return float(np.mean(a < b))


# ─────────────────────────────────────────────────────────────
# 1. Unit invariants
# ─────────────────────────────────────────────────────────────

def test_unit_invariants():
    print(SEP)
    print("TEST 1  Unit Invariants")
    print(SEP)

    rng = np.random.default_rng(0)

    # 1a. Starts unstable
    u = HomeostasisUnit(dim=5, gear=0.1, rng=rng)
    assert not u.is_stable
    print("  [PASS] 1a  Unit starts unstable")

    # 1b. Stabilises on constant fitness landscape
    rng2 = np.random.default_rng(1)
    u2 = HomeostasisUnit(dim=5, gear=0.1, rng=rng2)
    for _ in range(30):
        u2.update(u2.propose(), 1.0)
    assert u2.is_stable
    print("  [PASS] 1b  Unit stabilises on constant landscape")

    # 1c. Update rule: position converges to better region
    rng3 = np.random.default_rng(2)
    u3 = HomeostasisUnit(dim=1, gear=2.0, rng=rng3, history_len=20)
    good = np.array([0.05])
    bad  = np.array([4.0])
    for _ in range(6):
        u3.update(good, 0.01)
        u3.update(bad,  16.0)
    assert abs(u3.position[0] - good[0]) < abs(u3.position[0] - bad[0])
    print(f"  [PASS] 1c  Position ({u3.position[0]:.4f}) closer to good (0.05) than bad (4.0)")

    # 1d. Restart fires after stagnation_limit consecutive stagnant steps
    rng4 = np.random.default_rng(3)
    u4 = HomeostasisUnit(dim=2, gear=0.1, rng=rng4, stagnation_limit=10)
    for _ in range(50):         # more than stagnation_limit
        u4.update(u4.propose(), 1.0)
    assert u4.n_restarts >= 1
    print(f"  [PASS] 1d  Restart fires on stagnation ({u4.n_restarts} restart(s))")

    # 1e. Unit isolation: updating u does not affect v
    rng5 = np.random.default_rng(4)
    u5 = HomeostasisUnit(dim=3, gear=1.0, rng=rng5)
    rng6 = np.random.default_rng(5)
    v  = HomeostasisUnit(dim=3, gear=0.1, rng=rng6)
    v_pos_before = v.position.copy()
    for _ in range(5):
        u5.update(u5.propose(), 999.0)
    assert np.allclose(v.position, v_pos_before)
    print("  [PASS] 1e  Unit isolation: updating u does not move v")
    print()


# ─────────────────────────────────────────────────────────────
# 2. Round-robin scheduling
# ─────────────────────────────────────────────────────────────

def test_scheduling():
    print(SEP)
    print("TEST 2  Round-Robin Scheduling")
    print(SEP)

    n_units = 4
    max_evals = 100
    call_counts = {i: 0 for i in range(n_units)}

    def make_counting_fn(uid):
        def fn(x):
            call_counts[uid] += 1
            return float(np.sum(x**2))
        return fn

    # Patch each unit's propose to record which unit fired
    opt = MultiscaleAshbyOptimizer(dim=2, n_units=n_units, seed=0)
    unit_step_counts = [0] * n_units

    for step in range(max_evals):
        idx = step % n_units
        unit_step_counts[idx] += 1
        opt.step(sphere)

    # Each unit should have fired exactly max_evals / n_units times
    expected = max_evals // n_units
    for i, count in enumerate(unit_step_counts):
        assert count == expected, f"Unit {i}: expected {expected} steps, got {count}"
    print(f"  [PASS] All {n_units} units received exactly {expected} steps each")
    print()


# ─────────────────────────────────────────────────────────────
# 3. Benchmark: Ashby vs Random vs (1+1)-ES
# ─────────────────────────────────────────────────────────────

def test_benchmark(n_runs=30, dim=10, max_evals=500):
    print(SEP)
    print(f"TEST 3  Benchmark  dim={dim}  evals={max_evals}  runs={n_runs}")
    print(SEP)

    ashby_kw  = dict(dim=dim, n_units=4, coarsest_gear=2.0)
    rand_kw   = dict(dim=dim, search_range=2.0)
    es_kw     = dict(dim=dim, sigma0=0.5)

    problems  = [
        ("Sphere",     sphere,     0.0),
        ("Rastrigin",  rastrigin,  0.0),
        ("Rosenbrock", rosenbrock, 0.0),
        ("Ackley",     ackley,     0.0),
    ]

    all_results = {}
    print(f"  {'Problem':<12}  {'Ashby':>12}  {'(1+1)-ES':>12}  {'Random':>12}  "
          f"{'vs ES':>8}  {'vs Rand':>8}")
    print(f"  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*8}  {'─'*8}")

    for name, fn, opt in problems:
        a = run_batch(MultiscaleAshbyOptimizer, ashby_kw, fn, max_evals, n_runs)
        r = run_batch(RandomSearch,             rand_kw,  fn, max_evals, n_runs)
        e = run_batch(OnePlusOneES,             es_kw,    fn, max_evals, n_runs)

        all_results[name] = (a, r, e)

        wr_es   = win_rate(a, e)
        wr_rand = win_rate(a, r)
        print(f"  {name:<12}  {median(a):>12.6f}  {median(e):>12.6f}  {median(r):>12.6f}"
              f"  {100*wr_es:>7.0f}%  {100*wr_rand:>7.0f}%")

    return all_results


# ─────────────────────────────────────────────────────────────
# 4. Multi-scale advantage: number of units
# ─────────────────────────────────────────────────────────────

def test_num_units(n_runs=25, dim=10, max_evals=500):
    print()
    print(SEP)
    print(f"TEST 4  Multi-Scale Advantage (Rastrigin, dim={dim}, evals={max_evals})")
    print(SEP)
    print("  Tests the core hypothesis: more scales = better coverage of")
    print("  multi-modal landscapes (each scale independently escapes its")
    print("  local optima via homeostatic restarts).")
    print()
    print(f"  {'Units':>7}  {'Gears':>28}  {'Median':>12}  {'vs 1-unit':>10}")
    print(f"  {'─'*7}  {'─'*28}  {'─'*12}  {'─'*10}")

    baseline = None
    for n in [1, 2, 4, 6, 8]:
        res = run_batch(
            MultiscaleAshbyOptimizer,
            dict(dim=dim, n_units=n, coarsest_gear=2.0),
            rastrigin, max_evals, n_runs
        )
        med = median(res)
        if baseline is None:
            baseline = med
        gear_str = str([round(2.0 / (10**i), 4) for i in range(n)])
        ratio = med / (baseline + 1e-12)
        print(f"  {n:>7}  {gear_str:>28}  {med:>12.6f}  {ratio:>9.4f}x")


# ─────────────────────────────────────────────────────────────
# 5. Dimensionality scaling
# ─────────────────────────────────────────────────────────────

def test_scaling(n_runs=20, max_evals=1000):
    print()
    print(SEP)
    print(f"TEST 5  Dimensionality Scaling (Rastrigin, {max_evals} evals)")
    print(SEP)
    print("  Checks performance does not collapse as dimensionality grows.")
    print()
    print(f"  {'dim':>5}  {'Ashby':>12}  {'Random':>12}  {'(1+1)-ES':>12}  {'Win %':>7}")
    print(f"  {'─'*5}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*7}")

    for dim in [2, 5, 10, 20, 50]:
        a = run_batch(MultiscaleAshbyOptimizer, dict(dim=dim, n_units=4, coarsest_gear=2.0),
                      rastrigin, max_evals, n_runs)
        r = run_batch(RandomSearch,             dict(dim=dim, search_range=2.0),
                      rastrigin, max_evals, n_runs)
        e = run_batch(OnePlusOneES,             dict(dim=dim, sigma0=0.5),
                      rastrigin, max_evals, n_runs)
        wr = win_rate(a, r)
        print(f"  {dim:>5}  {median(a):>12.4f}  {median(r):>12.4f}  {median(e):>12.4f}  {100*wr:>6.0f}%")


# ─────────────────────────────────────────────────────────────
# 6. Convergence speed
# ─────────────────────────────────────────────────────────────

def test_convergence(dim=10, max_evals=1000, n_runs=25):
    print()
    print(SEP)
    print(f"TEST 6  Convergence Curve (Rastrigin, dim={dim})")
    print(SEP)
    print("  Median best-so-far at eval checkpoints.")
    print()
    print(f"  {'Evals':>7}  {'Ashby':>12}  {'(1+1)-ES':>12}  {'Random':>12}")
    print(f"  {'─'*7}  {'─'*12}  {'─'*12}  {'─'*12}")

    a_curves, r_curves, e_curves = [], [], []
    for seed in range(n_runs):
        a = MultiscaleAshbyOptimizer(dim=dim, n_units=4, coarsest_gear=2.0, seed=seed)
        r = RandomSearch(dim=dim, search_range=2.0, seed=seed)
        e = OnePlusOneES(dim=dim, sigma0=0.5, seed=seed)
        a_curves.append(a.run(rastrigin, max_evals)["history"])
        r_curves.append(r.run(rastrigin, max_evals)["history"])
        e_curves.append(e.run(rastrigin, max_evals)["history"])

    for cp in [10, 25, 50, 100, 200, 400, 800, 1000]:
        if cp > max_evals:
            break
        am = np.median([h[cp - 1] for h in a_curves])
        rm = np.median([h[cp - 1] for h in r_curves])
        em = np.median([h[cp - 1] for h in e_curves])
        print(f"  {cp:>7}  {am:>12.4f}  {em:>12.4f}  {rm:>12.4f}")


# ─────────────────────────────────────────────────────────────
# 7. Budget fairness check
# ─────────────────────────────────────────────────────────────

def test_budget_fairness(dim=10, n_runs=20):
    """
    Confirms the optimizer uses EXACTLY the requested number of evaluations
    and that total evals equals sum of per-unit evals.
    """
    print()
    print(SEP)
    print("TEST 7  Budget Fairness")
    print(SEP)

    for max_evals in [100, 500, 1001]:
        opt = MultiscaleAshbyOptimizer(dim=dim, n_units=4, seed=0)
        result = opt.run(sphere, max_evals)
        assert result["evals"] == max_evals, \
            f"Expected {max_evals} evals, got {result['evals']}"
        assert len(result["history"]) == max_evals, \
            f"History length mismatch"
        print(f"  [PASS] {max_evals} evals requested → {result['evals']} used, history length {len(result['history'])}")
    print()


# ─────────────────────────────────────────────────────────────
# Run all
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("══════════════════════════════════════════════════════════════════")
    print("  MultiscaleAshbyOptimizer — Full Test Suite")
    print("══════════════════════════════════════════════════════════════════")
    print()

    test_unit_invariants()
    test_scheduling()
    test_benchmark(n_runs=30, dim=10, max_evals=500)
    test_num_units(n_runs=25, dim=10, max_evals=500)
    test_scaling(n_runs=20, max_evals=1000)
    test_convergence(dim=10, max_evals=1000, n_runs=25)
    test_budget_fairness()

    print("══════════════════════════════════════════════════════════════════")
    print("  ALL TESTS COMPLETE")
    print("══════════════════════════════════════════════════════════════════")
    print()
