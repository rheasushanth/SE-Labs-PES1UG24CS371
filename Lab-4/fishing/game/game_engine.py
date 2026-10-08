"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Starter version: the hook casts and retracts automatically in a
continuous loop - there's no player control over casting yet (that's
Task 3), only one fish type exists (Task 2 adds more), and there's no
round timer (Task 4). Catch detection also has a known bug (see
game/catch.py) that Task 1 asks you to fix.
"""

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_SECONDS = 30
FPS = 60

class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            Fish(x=100, y=180, speed=1.5, width=24, height=12, point_value=5, color=(150, 200, 120)),
            Fish(x=400, y=280, speed=-1.5, width=24, height=12, point_value=5, color=(150, 200, 120)),
            Fish(x=250, y=330, speed=2.5, width=36, height=18, point_value=15, color=(80, 180, 220)),
            Fish(x=300, y=400, speed=-4, width=54, height=26, point_value=40, color=(220, 120, 60)),
        ]
        self.hooked_fish = None
        self.score = 0
        self.frames_left = ROUND_SECONDS * FPS
        self.game_over = False

    def try_cast(self):
        if not self.game_over and self.hook.state == IDLE and self.hooked_fish is None:
            self.hook.start_cast()

    def update(self):
        if self.game_over:
            return
        self.frames_left -= 1
        if self.frames_left <= 0:
            self.frames_left = 0
            self.game_over = True
            return        

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        seconds_left = (self.frames_left + FPS - 1) // FPS
        renderer.draw_text(surface, font, f"Time: {seconds_left}", (10, 40))
        if self.game_over:
            renderer.draw_banner(surface, font, f"Time's up! Final Score: {self.score}")
