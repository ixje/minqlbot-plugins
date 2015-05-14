minqlbot-plugins
================

All credits go to the original author Mino. Without his work on [minqlbot](https://github.com/MinoMino/minqlbot) there would be no place for plugins.

For the latest version of the original plugins including bux fixes visit the [original plugins repository](https://github.com/MinoMino/minqlbot-plugins)

What new in this branch
=======================

**balance.py** - a modification to the default balance plugin that adds majority voting

### tweaks / additions

* All players can now vote on a !teams suggestion. Based on a configurable majority threshold the switch is enforced even if the suggested players do not vote themselves.
* Added reminders to vote to the suggested players at the start of the round via tell.
* Limited the time a !teams suggestion is valid to current + next round to prevent last round changing to the winning team.
* Enforcement of the switching happens **after** the round has ended.

### Status
Tested. It has been running for several months now on pony.stable. Thanks **Thaya**!

### TODO
* N/A

Installation
============
Replace `balance.py` in your plugins directory. Edit `config.cfg` and add the following lines in the [balance] section

```python
# Enable enforcing of the switch suggestion if the majority (configurable below) of the players vote in favor of the suggestion.
MajorityVotingEnable: True

# Percentage of players that need to agree before voting is enforced. 0.5 = 50%
MajorityVotingThreshold: 0.5
```

Have a look at the `config.cfg` file in this branch if you're unsure where to place the lines.

For further instructions please visit the orignal author's [main repository](https://github.com/MinoMino/minqlbot). I'm usally also present in the irc channel mentioned there.