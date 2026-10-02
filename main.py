# Q3 non-adjacent sponsors: dynamic-programming table vs greedy baseline
import csv
import random
import sys
import time


# Reads a CSV file, sorts its rows by the "position" column, and
# returns just the pledge amounts as a list of integers in that order
def load_pledges(path):
    with open(path, newline="") as f:
        rows = sorted(csv.DictReader(f), key=lambda r: int(r["position"]))
    return [int(r["pledge"]) for r in rows]


# Builds a table where each cell holds the best total from the first i sponsors,
# choosing at each step whether skipping or taking the new sponsor pays more
def dp_table(pledges):
    # dp[i] = largest total from the first i sponsors
    n = len(pledges)
    dp = [0] * (n + 1)                  # dp[0] = 0: base case
    if n >= 1:
        dp[1] = pledges[0]              # one sponsor: take them
    for i in range(2, n + 1):           # left to right: dp[i-1], dp[i-2] already filled
        skip = dp[i - 1]
        take = dp[i - 2] + pledges[i - 1]
        dp[i] = skip if skip >= take else take
    return dp


# Walks the finished table backwards to work out which sponsors were actually chosen,
# returning their positions (counting from 1)
def trace_back(dp, pledges):
    # Walk back from dp[n]: jump two after a take, one after a skip
    chosen, i = [], len(pledges)
    while i >= 1:
        if i == 1 or dp[i] != dp[i - 1]:    # dp[i] didn't come from skipping i
            chosen.append(i)
            i -= 2
        else:
            i -= 1
    return sorted(chosen)


# Runs the DP method end to end: builds the table, then returns the best total (last cell)
# together with the chosen positions
def solve_dp(pledges):
    dp = dp_table(pledges)
    return dp[-1], trace_back(dp, pledges)


# greedy method
# pledge still available and rules out its neighbours; fast, but can miss the true best total
def solve_greedy(pledges):

    # Repeatedly accept the largest remaining pledge whose neighbours are not accepted
    # A neighbour of an accepted sponsor is out permanently
    # Ties go to the earlier position
    # Sorting once gives the same order as repeated max

    n = len(pledges)
    status = [0] * n                    # 0 = in the running, 1 = accepted, 2 = out
    order = sorted(range(n), key=lambda i: (-pledges[i], i))
    total, chosen = 0, []
    for i in order:
        if status[i] != 0:
            continue
        status[i] = 1
        total += pledges[i]
        chosen.append(i + 1)
        if i > 0 and status[i - 1] == 0:
            status[i - 1] = 2
        if i < n - 1 and status[i + 1] == 0:
            status[i + 1] = 2
    return total, sorted(chosen)


#  Timing
# Runs a function on the same data several times and returns the fastest run in seconds,
# so the comparison is as fair as possible.
def time_it(fn, data, repeats):
    # returns the run least disturbed by the machine's background activities
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(data)
        best = min(best, time.perf_counter() - t0)
    return best


# Entry point: loads the two CSV files (from the command line or default names), t
# then checks correctness, tests tricky and random cases, and times both methods.
def main():
    main_list = load_pledges(sys.argv[1] if len(sys.argv) > 1 else "Q3_sequence_main.csv")
    check_list = load_pledges(sys.argv[2] if len(sys.argv) > 2 else "Q3_sequence_selfcheck.csv")

    # proof that my algorithm works
    print("== Correctness ==")
    for name, p in (("selfcheck", check_list), ("main", main_list)):
        dt, dc = solve_dp(p)
        gt, gc = solve_greedy(p)
        print(f"{name:9s} dp={dt} {dc}  greedy={gt} {gc}  gap={dt - gt}")
    print("dp table (main):", dp_table(main_list))

    print("\n== Running time (best of repeats, seconds) ==")
    rng = random.Random(42)  # fixed seed so the generated timing lists are the same every run
    print(f"{'n':>9} {'dp':>12} {'greedy':>12} {'dp/n (ns)':>10} {'gr/(n log n) (ns)':>18}")
    import math
    print(f"{12:>9} {time_it(solve_dp, main_list, 2000):12.3e} "
          f"{time_it(solve_greedy, main_list, 2000):12.3e}   (supplied list)")
    for n in (1_000, 10_000, 100_000, 1_000_000, 4_000_000):
        p = [rng.randint(1, 10 ** 6) for _ in range(n)]
        reps = 20 if n <= 100_000 else 3
        td, tg = time_it(solve_dp, p, reps), time_it(solve_greedy, p, reps)
        print(f"{n:>9} {td:12.3e} {tg:12.3e} {td / n * 1e9:10.1f} "
              f"{tg / (n * math.log2(n)) * 1e9:18.2f}")


# Runs main() only when this file is executed directly, not when it's imported by another file.
if __name__ == "__main__":
    main()