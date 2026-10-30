# Issues Found — shuttle_system.py

| # | Issue | Type | Tool / Code | Line(s) | Severity | Description | Fix Approach |
|---|-------|------|-------------|---------|----------|-------------|--------------|
| 1 | Bare `except: pass` | Security / Bug | Bandit B110, Pylint W0702, Flake8 E722 | 29-30 | Medium | Catches *every* error (even KeyboardInterrupt) and silently ignores it, hiding the R3 `"full"` TypeError and any divide-by-zero. | Removed the try/except; `average_load` now returns `None` for routes with no trips and `underused_routes` skips them. Bad data is rejected at input instead. |
| 2 | Insecure random generator | Security | Bandit B311 | 35 | Low | `random.choice` is a predictable pseudo-random generator, flagged by Bandit as unsuitable for anything security-related. | Replaced with `secrets.choice`. |
| 3 | Mutable default argument | Bug | Pylint W0102 | 11 | Medium | `logs=[]` is created once and shared by every call, so log entries pile up across unrelated calls. | Default changed to `None` and a new list is created inside the function. |
| 4 | Files opened without `with` / encoding | Bug / Resource leak | Pylint R1732, W1514 | 39, 42 | Medium | Second `open()` is never closed (file handle leak); no encoding means behaviour depends on the OS. | Used `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| 5 | `global` statement | Design | Pylint W0603 | 38 | Low | Rebinding the global `routes` inside a function makes the state hard to follow. | Updated the existing dict in place with `routes.clear()` + `routes.update()`, so no `global` is needed. |
| 6 | Invalid passenger data accepted | Logic bug (not flagged by tools) | — | 49-50 | High | `-6` and `"full"` are stored as trip counts. `"full"` makes `sum()` crash, and `-6` corrupts the R2 average. | `add_trip_log` validates the count (must be a non-negative int) and raises; `main` uses `safe_log` to report rejected trips. |
| 7 | Crash after route removed / unknown route | Logic bug (not flagged by tools) | — | 55-58 | High | R3 is deleted and then `average_load("R3")` raises `KeyError`; typing an unknown route at the prompt also crashes. Empty routes cause `ZeroDivisionError`. | `average_load` uses `routes.get()` and returns `None`; `main` checks `choice in routes` before using it; `remove_route` uses `pop(..., None)`. |
| 8 | Bad function name & unused argument | Style | Pylint C0103, W0613 | 33 | Low | `assignDriver` isn't snake_case and its `route_id` parameter is never used. | Renamed to `assign_driver()` and removed the unused parameter. |
| 9 | Old-style `%` formatting | Style | Pylint C0209 | 13 | Low | `%` formatting is harder to read than an f-string. | Converted to an f-string. |
| 10 | Missing docstrings | Style | Pylint C0114, C0116 | 1, 11-45 | Low | Module and functions have no documentation. | Added a module docstring and one per function. |
| 11 | Missing blank lines (PEP 8) | Style | Flake8 E302, E305 | 11-60 | Low | Functions need 2 blank lines between them. | Added 2 blank lines before each top-level definition. |
| 12 | Line too long | Style | Flake8 E501 | 13 | Low | Line is 82 chars (limit 79). | Wrapped / rewrote the line. |
| 13 | Code runs on import | Design | — | 60 | Low | `main()` runs even when the file is imported. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25 / 10 (18 messages) | **10.00 / 10** |
| Bandit | 2 issues (Low: B110, B311) | **0 issues** |
| Flake8 | 10 issues | **0 issues** |
