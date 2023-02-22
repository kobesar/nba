from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, commonplayerinfo
import pandas as pd
import time

full_league = teams.get_teams()
season = 2022

sum_teams = []
full_df = []

for team in full_league:
  tid = team['id']
  tname = team['abbreviation']
  team_df = commonteamroster.CommonTeamRoster(season=season, team_id=tid).get_data_frames()[0]
  lottery_players = 0
  for player in team_df['PLAYER_ID']:
    pid = player
    player_df = commonplayerinfo.CommonPlayerInfo(player_id=pid).get_data_frames()[0]
    pid = player_df['PERSON_ID'][0]
    pname = player_df['DISPLAY_FIRST_LAST'][0]
    player_pick = player_df['DRAFT_NUMBER'][0]
    lottery = int(player_pick) <= 14 if (player_pick != 'Undrafted') and (player_pick is not None) else False
    lottery_players += 1 if lottery is True else 0
    full_df.append(player_df.to_dict())
    time.sleep(1)
  sum_teams.append({'team': tname, 'lottery_players': lottery_players, 'players': len(team_df['PLAYER_ID'])})

full = pd.DataFrame()

for row in full_df:
  full = pd.concat([full, pd.DataFrame([val[0] for val in row.values()]).transpose()])
full.columns = full_df[0].keys()

pd.DataFrame(sum_teams).to_csv("data/team_lottery.csv")
full.to_csv("data/all_players.csv")