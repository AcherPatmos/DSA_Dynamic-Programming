# DSA Dynamic Programming: Non-Adjacent Sponsors (Question 3)

Twelve sponsors are listed in a fixed order, and each one offers a pledge. You may accept any of them, with one restriction: you can't accept two sponsors who are next to each other in the list, because neighbours are competitors and will not both sign. The order can't be changed. The question is the largest total you can raise, and which sponsors it comes from.

`main.py` answers this with a **dynamic-programming table** and compares it against a **greedy baseline**, first on the two supplied lists and then on large generated lists to measure running time.

**Result on the main list:** the table finds **91**, from sponsors **1, 3, 5, 8, 10 and 12**. Greedy finds **61**, from sponsors 2, 5, 8 and 11, which is 30 less.

The full working, including the hand-computed tables, the traceback and the analysis, is in the project report (`DSA_Summative_Project_Report_Patmos_Acher_Mpakaniye.pdf`).

## Project structure

```
DSA_Dynamic Programming/
├── main.py                     # DP table, greedy baseline, correctness check and timing
├── Q3_sequence_main.csv        # the 12-sponsor list from the question
└── Q3_sequence_selfcheck.csv   # a 5-sponsor list with a known answer of 17
```

## Requirements

- Python 3.6 or newer. The project was developed with Python 3.14.
- No external packages. The program uses only the standard library (`csv`, `random`, `sys`, `time`, `math`).

## How to run

```bash
git clone https://github.com/AcherPatmos/DSA_Dynamic-Programming.git
cd DSA_Dynamic-Programming
python main.py
```

To run it on other lists, pass the CSV files on the command line. The first is used as the main list and the second as the self-check list:

```bash
python main.py path/to/main.csv path/to/selfcheck.csv
```

The default filenames are relative paths. Python looks for them in the folder your terminal is in, not the folder where `main.py` sits. If you get a `FileNotFoundError`, `cd` into the project folder first, or pass full paths. PyCharm runs the script from the project folder by default, so it works there without changes.

The full run takes around a minute, mostly spent on the 1-million and 4-million-sponsor timing lists.

## CSV format

```
position,sponsor,pledge
1,Sponsor 1,15
2,Sponsor 2,16
3,Sponsor 3,14
```

The program reads only the `position` and `pledge` columns and ignores `sponsor`. Rows can appear in any order, because the loader sorts them by `position`. Both columns must hold whole numbers, and the header names must match exactly.

## How it works

### Dynamic-programming table

`dp[i]` is the largest total you can raise using only the first `i` sponsors. For each sponsor `i` there are two choices:

- **Skip** sponsor `i`: the best total stays at `dp[i−1]`.
- **Take** sponsor `i`: you gain their pledge, but sponsor `i−1` is now off limits, so the rest comes from `dp[i−2]`.

```
dp[i] = max(dp[i−1], dp[i−2] + pledge[i])
dp[0] = 0          (no sponsors considered yet)
dp[1] = pledge[1]  (one sponsor: take them)
```

The table is filled left to right, so both earlier cells are always ready. The answer is the last cell, `dp[n]`. For the main list, the table is:

```
[0, 15, 16, 29, 29, 45, 45, 54, 55, 59, 72, 78, 91]
```

**Traceback** (`trace_back`) recovers which sponsors were chosen. Starting at `dp[n]`: if `dp[i]` equals `dp[i−1]`, sponsor `i` was skipped, so step back one. Otherwise sponsor `i` was taken, so jump back two.

### Greedy baseline

`solve_greedy` sorts the sponsors from largest pledge to smallest, breaking ties by earliest position. It then walks that order, accepting each sponsor who is still in the running and permanently ruling out their neighbours. Sorting once gives the same order as repeatedly searching for the largest remaining pledge, but faster.

Greedy fails on the main list because it takes sponsor 11 (19), which permanently rules out sponsors 10 (17) and 12 (19). Those two together are worth more than sponsor 11 alone.

## Output

**Correctness.** For each list, the program prints the DP total and chosen sponsors, the greedy total and chosen sponsors, and the gap between them. It then prints the DP table for the main list.

| List | DP table | Greedy | Gap |
|---|---|---|---|
| Self-check (5 sponsors) | 17, sponsors 2, 5 | 17, sponsors 2, 5 | 0 |
| Main (12 sponsors) | 91, sponsors 1, 3, 5, 8, 10, 12 | 61, sponsors 2, 5, 8, 11 | 30 |

The self-check list is the case where greedy matches the table: it takes 9 and then 8, and neither pick rules out a sponsor the best answer needed.

**Running time.** The program times both methods on the 12-sponsor list, then on random lists of 1,000 to 4,000,000 sponsors. The random generator uses a fixed seed (42), so the lists are the same on every run. Each time is the **fastest** of several runs, because other programs on the machine can only slow a run down. The fastest run is the one least disturbed.

| Column | Meaning |
|---|---|
| `n` | Number of sponsors in the list |
| `dp` | Fastest time for the DP table method, in seconds |
| `greedy` | Fastest time for greedy, in seconds |
| `dp/n (ns)` | DP time per sponsor, in nanoseconds. It stays roughly flat if DP is O(n) |
| `gr/(n log n) (ns)` | Greedy time divided by n × log₂(n), in nanoseconds. It stays roughly flat if greedy is O(n log n) |

## Complexity

| Method | Time | Memory |
|---|---|---|
| DP table + traceback | O(n): n + 1 cells, one comparison and one addition each | O(n), because the traceback needs the whole table |
| Greedy | O(n log n) for the sort, plus an O(n) walk | O(n) |
| Greedy without sorting | O(n²): each round rescans the whole list for the largest remaining pledge | O(n) |

## Measured results

| n | Table (s) | Greedy (s) | Table per item (ns) | Greedy per n·log₂n (ns) |
|---|---|---|---|---|
| 12 (main list) | 2.6 × 10⁻⁶ | 4.0 × 10⁻⁶ | – | – |
| 1,000 | 2.0 × 10⁻⁴ | 4.8 × 10⁻⁴ | 202.0 | 48.1 |
| 10,000 | 2.2 × 10⁻³ | 6.8 × 10⁻³ | 223.7 | 51.5 |
| 100,000 | 2.4 × 10⁻² | 0.11 | 244.4 | 67.0 |
| 1,000,000 | 0.31 | 2.15 | 313.4 | 107.7 |
| 4,000,000 | 1.28 | 11.39 | 320.4 | 129.9 |

The per-item columns don't hold steady. The table's cost per item rises by about 60% from 1,000 to 4 million sponsors, and greedy's rises about 2.7 times. Big-O treats every step as costing the same. In practice, large lists no longer fit in the processor's cache, so more steps wait on slower main memory.

The measurements do agree on which method scales better. Greedy is about 2.4 times slower than the table at 1,000 sponsors, and about 9 times slower at 4 million. That widening gap is what greedy's extra log n factor predicts.

## Limitations

- **Ties.** When several selections share the best total, the table returns only one. Because the code prefers "skip" on a tie, it favours selections that end earlier in the list.
- **Circular lists.** Only a straight line is handled. If the first and last sponsors were also neighbours, you would need two runs: one without the first sponsor and one without the last.
- **Memory.** The table uses memory proportional to n because of the traceback. If only the total were needed, two variables would be enough.
- **Negative pledges.** The table handles them correctly, since skipping is always allowed. Greedy doesn't: once only negative pledges remain, it keeps accepting them and lowers the total.
- **Input checking.** The loader assumes a well-formed CSV with whole-number pledges and one row per position. It doesn't check for gaps or duplicate positions.
- **Timing scope.** All timings come from one Python version on one machine. A compiled language would give much smaller absolute times, and possibly a different gap between the two methods.
