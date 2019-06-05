# Cyphers Discord Bot
![Cyphers Discord Bot Logo](logo.png)

## For Users
[![Play Cyphers Now](https://img.shields.io/badge/play-Cyphers-Red.svg)](http://cyphers.nexon.com/cyphers/main)
[![Add This Bot To Your Server](https://img.shields.io/badge/Add_This_Bot_To_Your_Server-Blue.svg)](https://discordapp.com/api/oauth2/authorize?client_id=585768609893318666&permissions=67584&scope=bot)

## For Developers
[![Beerware License](https://img.shields.io/badge/license-Beerware-green.svg)](https://wikipedia.org/wiki/Beerware)
[![Special Thanks To 'discord.py'](https://img.shields.io/badge/Speical_Thanks_To-discord.py-Purple.svg)](https://github.com/Rapptz/discord.py)
[![Need Neople API Token](https://img.shields.io/badge/Get_API_Token-From_Neople_Developers-Yellow.svg)](https://developers.neople.co.kr/main)

### Essential Token Files
* **{discord_bot.token}** Discord bot token file (RAW Text Format)
* **{neople_api.token}** Neople Developers API Token (RAW Text Format)

### Markdown Template Example
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
