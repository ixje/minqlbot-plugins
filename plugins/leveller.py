# a small plugin to auto level the teams on round start by speccing the person with the lowest score on the oversized team

import minqlbot
import re

class leveller(minqlbot.Plugin):
    def __init__(self):
        if not hasattr(minqlbot,'CaScores'):
            self.debug("Too old version of Minqlbot. Please update to the latest version")
            minqlbot.unload_plugin("leveller")
        else:
            self.add_hook("game_start", self.handle_game_start)
            self.add_hook("game_end", self.handle_game_start)
            self.add_hook("round_start", self.handle_round_start)
            self.add_hook("scores", self.handle_scores)
            self.add_hook("team_switch", self.handle_team_switch)
            
            self.roundstart_triggered = False
            self.blue_joins = []
            self.red_joins = []
            self.game_started = False
            self.round_number = 1
   

    def handle_game_start(self, game):
        self.debug("game_started")
        self.game_started = True
        self.round_number = 1

    def handle_game_end(self,game,score,winner):
        #is this triggered on an 'abort'?
        self.game_started = False
        self.round_number = 1

    def handle_round_start(self, round):
        self.debug("round: {}".format(round))
        self.round_number = round

        if not self.game_started:
            self.game_started = True
        elif self.game_started:
            self.roundstart_triggered = True
            self.send_command("score")

    def handle_scores(self, scores):
        if self.roundstart_triggered:
            self.roundstart_triggered = False
            teams = self.teams()
            #if (len(teams["red"]) + len(teams["blue"])) % 2 == 0:
            #    return

            if len(teams["red"]) > len(teams["blue"]):
                reduceteam = teams["red"]
                reduceJoinersFrom = self.red_joins
            else:
                reduceteam = teams["blue"]
                reduceJoinersFrom = self.blue_joins
            #list of player names in the oversized team
            playernames = list(map(lambda p:p.clean_name, reduceteam))

            if self.game_started:
                #Scenario 1, first round (gamestart, all scores 0)
                if self.round_number == 1:
                    self.debug("scenario 1")
                    #always remove last joiner
                    self.put(reduceJoinersFrom.pop(), "spectator")
                    return

                #Scenario 2, round 2 or later (on-going game)
                if self.round_number > 1:
                    self.debug("scenario 2")
                    
                    #2A - 1 joiner, spec him
                    #2c - 2 join, 1 other leaves. spec last joiner on other team regardless of score
                    #TODO: determine when it's scenario 2A/3C
                    # if (scenario 2A | 2C):
                        self.put(reduceJoinersFrom.pop(), "spectator")
                        return

                    #2B - 1 leaver, spec lowest score on other team
                    #TODO: determine when it's scenario 2B
                    # if (scenario 2b):
                        lowestscore = 999
                        toSpec = []
                        for p in scores:
                            cleanName = re.sub(r"\^[0-9]", "", str(p.player))

                            if cleanName in playernames:
                                if p.score < lowestscore:
                                    toSpec.append(p.player)
                                if p.score == lowestscore:
                                    toSpec.append(p.player)
                        
                        if len(toSpec) == 1:
                            self.put(toSpec[0], "spectator")
                        elif len(toSpec) >1: #2 or more with the same score. Find the last joiner
                            
                            #starting from the back, assuming the last added is last joined to the team
                            for p in reversed(reduceJoinersFrom):
                                if p in toSpec:
                                    reduceJoinersFrom.remove(p)
                                    self.put(p, "spectator")

    def handle_team_switch(self, player, old_team, new_team):
        #TODO: make sure the blue_joins & red_joins are updated when the bot balances without the players being considered as the last joiner
        #      Currently the last player on the list is treated as the last joiner
        
        #add to a list such that we can pop the last joiner when needed
        if old_team == "spectator" and new_team == "blue":
            self.blue_joins.append(player)
        if old_team == "spectator" and new_team == "red":
            self.red_joins.append(player)

        if old_team == "blue" and new_team == "spectator":
            self.blue_joins.remove(player)
        if old_team == "red" and new_team == "spectator":
            self.red_joins.remove(player)