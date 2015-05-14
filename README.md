minqlbot-plugins
================

All credits go to the original author Mino. Without his work on [minqlbot](https://github.com/MinoMino/minqlbot) there would be no place for plugins.

For the latest version of the original plugins including bux fixes visit the [original plugins repository](https://github.com/MinoMino/minqlbot-plugins)

What new in this branch
=======================

**locker.py** - a standalone plugin that auto locks and unlocks teams based on their size, spectator count or near round limit threshold. 

### (un)locking rules
Teams are locked if:

1. the game is started 
2. the game has progressed to 2 rounds from the round limit (to prevent last round inbalancing)

Teams are unlocked if:

1. at any point in time teams are unequal in size
2. there are enough specators to make equal sized bigger teams. Note that this rule is inferior to the round limit locking rule.

### Status
Experimental. It is only partially tested due to the lack of a premium quake live account.

### TODO
* Make the 'near round limit' value configurable through the `config.cfg`

Installation
============
Copy `locker.py` to your plugins directory and add *locker* to the plugins list in your `config.cfg`. 

For further instructions please visit the orignal author's [main repository](https://github.com/MinoMino/minqlbot). I'm usally also present in the irc channel mentioned there.