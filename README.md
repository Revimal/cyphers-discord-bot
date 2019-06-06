# Cyphers Discord Bot
![Cyphers Discord Bot Logo](logo.png)

## For Users
[![Play Cyphers Now](https://img.shields.io/badge/play-Cyphers-Red.svg)](http://cyphers.nexon.com/cyphers/main)
[![Add This Bot To Your Server](https://img.shields.io/badge/Add_This_Bot_To_Your_Server-Blue.svg)](https://discordapp.com/api/oauth2/authorize?client_id=585768609893318666&permissions=67584&scope=bot)

### Available Commands
* **`!cyp user {Username}`**
	View Game statistics & Basic Information of a player
* **`!cyp match {Username}`**
	View Game Win/Lose History of a player

## For Developers
[![Beerware License](https://img.shields.io/badge/license-Beerware-green.svg)](https://wikipedia.org/wiki/Beerware)
[![Special Thanks To 'discord.py'](https://img.shields.io/badge/Speical_Thanks_To-discord.py-Purple.svg)](https://github.com/Rapptz/discord.py)
[![Need Neople API Token](https://img.shields.io/badge/Get_API_Token-From_Neople_Developers-Yellow.svg)](https://developers.neople.co.kr/main)

### Essential Token Files
* **{discord_bot.token}** Discord bot token file (RAW Text Format)
* **{neople_api.token}** Neople Developers API Token (RAW Text Format)

### Template Example: Default
#### Target JSON Data
```javascript
{
  "playerId" : "9fd9f63e0d6487537569075da85a0c7f",
  "nickname" : "JohnDoe",
  "grade" : 100,
  "clanName" : "BestClanEver",
  "ratingPoint" : 3000,
  "maxRatingPoint" : 3000,
  "tierName" : "ACE 1ST",
  "records" : [ {
    "gameTypeId" : "rating",
    "winCount" : 161,
    "loseCount" : 44,
    "stopCount" : 3
  }, {
    "gameTypeId" : "normal",
    "winCount" : 1386,
    "loseCount" : 732,
    "stopCount" : 15
  } ]
}
```

#### Template File Content
```markdown
**{nickname} ({grade} Grade)**
- Clan: {clanName}
- Tier  : {tierName} (RP {ratingPoint}/{maxRatingPoint})
- Stat
	- Ranked Game (W: {records/$0/winCount}, L: {records/$0/loseCount}, S: {records/$0/stopCount})
	- Random Game (W: {records/$1/winCount}, L: {records/$1/loseCount}, S: {records/$1/stopCount})
```

### Template Example: Format String
#### Target JSON Data
```javascript
"rows" : [ {
  "date" : "2019-05-20 23:00",
  "matchId" : "cc9084078f65af6444fe244dd19bb2d1e8603e3861db91441794067bded388df",
  "playInfo" : {
    "result" : "win",
    "random" : false,
    "partyUserCount" : 0,
    "characterId" : "a4636e5b1ac646c6f320b53004a34e29",
    "characterName" : "히카르도",
    "level" : 63,
    "killCount" : 19,
    "deathCount" : 5,
    "assistCount" : 11,
    "attackPoint" : 59876,
    "damagePoint" : 48409,
    "battlePoint" : 285,
    "sightPoint" : 391
  }
}, {
  "date" : "2019-05-20 22:35",
  "matchId" : "e0a716ad3a744831169be8e0d6d05d300bb1e963baf7f6601604d3f5373808f8",
  "playInfo" : {
    "result" : "win",
    "random" : false,
    "partyUserCount" : 0,
    "characterId" : "a4636e5b1ac646c6f320b53004a34e29",
    "characterName" : "히카르도",
    "level" : 56,
    "killCount" : 21,
    "deathCount" : 8,
    "assistCount" : 12,
    "attackPoint" : 69875,
    "damagePoint" : 51781,
    "battlePoint" : 274,
    "sightPoint" : 405
  }
}]
```

#### Template File Content
```markdown
**[History]** %game_0/%game_1/%game_2/%game_3/%game_4/%game_5/%game_6/%game_7/%game_8/%game_9 **(W:%game_win, L:%game_lose)**
```

#### Python Fmtstr Builder
```python
rmtstr = {}
for i in range(10):
    try:
        matchres = MatchListBuilder.instance().parse(randomlist[i], 'playInfo/result')
        if matchres == 'win':
            randomwin += 1
            fmtstr['game_' + str(i)] = 'W'
        else:
            randomlose += 1
            fmtstr['game_' + str(i)] = 'L'
    except IndexError:
        fmtstr['random_' + str(i)] = 'X'
fmtstr['game_win'] = ratingwin
fmtstr['game_lose'] = ratinglose

matchlist = MatchListBuilder.instance().build(userdata, fmtstr)
if matchlist is None:
    return '**Markdown Build Failed**'
return matchlist
```

#### Built Format String
```text
{'game_0': 'W', 'game_1': 'W', 'game_2': 'X', 'game_3': 'X', 'game_4': 'X', 'game_5': 'X', 'game_6': 'X', 'game_7': 'X', 'game_8': 'X', 'game_9': 'X', 'game_win': 2, 'game_lose': 0}
```
