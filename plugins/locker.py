# Auto team locker.
#
# Teams are locked if:
# 1) the game is started 
# 2) the game has progressed to 2 rounds from the round limit (to prevent last round inbalancing)
#
# Teams are unlocked if:
# 1) at any point in time teams are unequal in size
# 2) when there's enough specators to make equal sized teams. <- this is overruled by the round limit locking
#
 

import minqlbot
import time
import threading

class locker(minqlbot.Plugin):
    def __init__(self):
        if not hasattr(minqlbot,'CaScores'):
            self.debug("Too old version of Minqlbot. Please update to the latest version")
            minqlbot.unload_plugin(self.__class__.__name__)
        else:
            self.add_hook("game_start", self.handle_game_start)
            self.add_hook("game_end", self.handle_game_end)
            self.add_hook("console", self.handle_console)
            self.game_started = False
            self.locked = False
            self.t = threading.Thread(target=self.monitor)
            self.t.start()    

    def handle_console(self, cmd):
        if "The RED team is now locked" in cmd:
            self.locked = True
        elif "The BLUE team is now locked" in cmd:
            self.locked = True
        elif "The RED team is now unlocked" in cmd:
            self.locked = False
        elif "The RED team is now unlocked" in cmd:
            self.locked = False

    def handle_game_start(self, game):
        self.debug("game started")
        self.game_started = True

    def handle_game_end(self,game,score,winner):
        self.game_started = False

    def areTeamsEqualSized(self):
        teams = self.teams()
        return (len(teams["red"]) + len(teams["blue"])) % 2 == 0

    def areEnoughSpecsAvailable(self):
        BOT = 1
        teams = self.teams()
        return (len(teams["spectator"])-BOT) % 2 == 0

    def isGameNearRoundLimit(self):
        threshold = 2 #make this a config variable
        return (self.game().roundlimit - max(self.game().blue_score, self.game().red_score)) <= threshold

    def unlock(self):
        if self.locked:
            self.send_command("unlock")
            self.locked = False

    def lock(self):
        if not self.locked:
            self.locked = True
            self.send_command("lock")

    def monitor(self):
        while True:
            if self.game_started:
                if not self.areTeamsEqualSized():
                    self.unlock()
                else:
                    if self.isGameNearRoundLimit():
                        self.lock()
                    else:
                        if self.areEnoughSpecsAvailable():
                            self.unlock()
                        else:
                            self.lock()
                time.sleep(5)