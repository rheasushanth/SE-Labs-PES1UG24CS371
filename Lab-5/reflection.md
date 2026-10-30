# Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues (missing blank lines, a long line) and the Pylint naming / docstring messages. They are mechanical: the tool tells you the exact line and what is wrong. Swapping `random.choice` for `secrets.choice` was also a one-line change. The hardest was the bare `except: pass`. Simply naming an exception type would have silenced the tools, but the real problem was that bad data (`"full"`, `-6`) was getting into the trip lists in the first place. Fixing it properly meant adding validation in `add_trip_log` and making `average_load` handle empty or missing routes. The `global routes` warning also needed a bit of thought, since I had to update the dict in place rather than reassign it.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit's B311 warning on `random.choice` is close to a false positive here. Picking which driver gets a route is not a security or cryptographic task, so a predictable generator is not a real risk. I still switched to `secrets.choice` because it costs nothing and clears the report, but in a real project this could reasonably be marked `# nosec`. Pylint's missing-docstring messages are also low value on very short, self-explanatory functions. On the other side, the tools missed real bugs: none of them flagged the negative passenger count, the `"full"` string, or the `KeyError` from looking up R3 after it was removed. I only found those by running the program.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint automatically in a pre-commit hook so style problems never reach the repository, and run all three tools (including Bandit) in a CI pipeline such as GitHub Actions on every push and pull request. The build could fail if the Pylint score drops below a threshold (e.g. 9.5) or if Bandit reports any Medium/High issue. I would also enable the linters in my editor (VS Code) so issues show up while I type, and keep a shared config file (`.pylintrc`, `.flake8`) so the whole team uses the same rules.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 6.25 to 10.00, and Bandit and Flake8 now report zero issues. More importantly, the program no longer crashes: before, it ended with a `KeyError` for R3, and typing an unknown route also crashed it. Invalid inputs like `-6` and `"full"` are now rejected with a clear message instead of silently corrupting the averages (R2's average was being pulled down by the negative count). Files are closed properly, the log list no longer leaks between calls, and every function has a docstring and a clear name, so the code is easier to read and safer to change.
