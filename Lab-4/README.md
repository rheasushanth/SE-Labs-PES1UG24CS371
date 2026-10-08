# Fishing Lab

## Submission Details

| | |
|---|---|
| **Name** | Rhea Sushanth |
| **SRN** | PES1UG24CS371 |
| **Lab** | Lab 4 - VibeCoding |
| **LLM chat link** | https://claude.ai/share/b4b4d8b8-45ad-48de-ad29-02ba8489a772 |
| **Recordings** | https://drive.google.com/drive/folders/1MHPiFwwvwwwqZTMeMqhBriLKgTkAxDMN?usp=sharing |

---

This project is a single-topic Fishing-lite game using **Pygame**. It
introduces students to timed casting mechanics, overlap-based catch
detection, and stateful entity variety, using a small, readable
object-oriented codebase.

---

## What's Provided

A working Fishing game with:

- A boat and hook - the hook casts downward and retracts back to the
  surface on its own, in a continuous loop
- Fish that swim back and forth across the pond at fixed depths and
  wrap around the screen edges
- A hook that snags a fish on contact - the fish rides up attached to
  the hook and is only actually caught (scored, removed from the pond)
  once the hook fully returns to the surface
- A running score display

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.



---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the game:

```
python main.py
```

**Controls:**
- **SPACE** - cast the hook (only when the hook is idle at the surface)
- **R** - start a new round after time is up

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix the catch-detection bug

> A fish is supposed to be caught only when the hook actually overlaps
> it. In the current build, `check_catch` (in `game/catch.py`) only
> compares the hook's depth to the fish's depth, within a fixed
> 10-pixel tolerance - it never compares horizontal position at all.
> That means a fish can register as caught while it's still far off to
> one side of the screen, just because the hook happens to be passing
> through its depth. Fix the check so it's based on the hook and fish
> actually overlapping, not just being at a similar depth.

**What I did:** `check_catch` now uses the existing `get_rect()`
methods and checks `hook.get_rect().colliderect(fish.get_rect())`, so
a fish is caught only when the hook and fish actually overlap, not just
when they are at a similar depth.

### Task 2: Implement multiple fish types

> Introduce at least two fish types that differ in movement speed and
> point value (for example, a slow low-value fish and a fast
> high-value one). Give each type its own look (color and/or size) so
> they're visually distinguishable, and make sure the correct point
> value is awarded when each type is caught.

**What I did:** Added three fish types in `GameEngine`:

| Type   | Speed        | Size   | Points | Color  |
|--------|--------------|--------|--------|--------|
| Minnow | Slow (1.5)   | Small  | 5      | Green  |
| Trout  | Medium (2.5) | Medium | 15     | Blue   |
| Tuna   | Fast (4)     | Big    | 40     | Orange |

Each fish's `point_value` is added to the score when it is landed at
the surface.

### Task 3: Implement player-controlled casting

> Change the hook so the player decides when it casts, instead of it
> looping automatically. Pressing a key should start a cast if the
> hook is currently idle; it should then travel down and return on its
> own (already handled) once it reaches maximum depth or catches a
> fish. A new cast should not be able to interrupt one that's already
> in progress.

**What I did:** Removed the auto-cast from `GameEngine.update()` and
added a `try_cast()` method that starts a cast only when the hook is
`IDLE` and no fish is still being reeled in. In `main.py`, a
`KEYDOWN` event for `K_SPACE` calls `try_cast()`, so pressing SPACE
during a cast does nothing.

### Task 4: Implement a 30-second round timer

> Add a 30-second countdown for the round. Display the remaining time
> on screen. Once it reaches zero, no further catches should be
> possible, the round should end, and the final score should be shown
> clearly. Provide a way to start a new round with the score and timer
> both reset.

**What I did:** Added a 30-second timer (counted in frames at 60 FPS)
shown on screen under the score. When it reaches 0, `update()` stops
running, so no more casts or catches happen, and a
"Time's up! Final Score: X" banner is shown. Pressing **R** after the
round ends calls a new `reset()` method, which restores the fish, hook,
score and timer for a fresh round.

---

## Expected Behavior

- A fish is only caught when the hook genuinely overlaps it - not just
  when it's at a similar depth anywhere on screen.
- A caught fish visibly rides up on the hook as it retracts; the score
  only increases once it's fully back at the surface.
- Different fish types are visually distinguishable and award the
  correct point value.
- Once casting is player-controlled, pressing the cast key while the
  hook is already out should do nothing - it should not interrupt or
  restart the current cast.
- The round lasts exactly 30 seconds. Once time runs out, no further
  catches should be possible, and the final score should be shown
  clearly.

---

## Folder Structure

```
fishing/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── hook.py
│   ├── fish.py
│   ├── catch.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

- [x] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [x] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [x] The Chat/LLM used page link, with the complete chat history
