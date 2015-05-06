# a small plugin to auto level the teams on round start by speccing the person with the lowest score on the oversized team

import minqlbot
import re

class leveller(minqlbot.Plugin):
    def __init__(self):
        if not hasattr(minqlbot,'CaScores'):
            self.debug("Too old version of Minqlbot. Please update to the latest version")
            minqlbot.unload_plugin("leveller")
        else:
            self.add_hook("round_start", self.handle_round_start)
            self.add_hook("scores", self.handle_scores)
            self.roundstart_triggered = False

    def handle_scores(self, scores):
         if self.roundstart_triggered:
            teams = self.teams()
            if (len(teams["red"]) + len(teams["blue"])) % 2 == 0:
                return

            if len(teams["red"]) > len(teams["blue"]):
                reduceteam = teams["red"]
            else:
                reduceteam = teams["blue"]
            playernames = list(map(lambda p:p.clean_name, reduceteam))
            
            lowestscore = 999
            toSpec = None
            for p in scores:
                cleanName = re.sub(r"\^[0-9]", "", str(p.player))

                if cleanName in playernames:
                    if p.score < lowestscore:
                        toSpec = p.player

            self.put(toSpec, "spectator")
            self.roundstart_triggered = False

    def handle_round_start(self, round):
        self.roundstart_triggered = True
        self.send_command("score")