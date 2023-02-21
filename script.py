from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, commonplayerinfo
import pandas as pd
import time

full_league = teams.get_teams()
season = 2022

# all_teams = {}
sum_teams = []

for team in full_league:
  tid = team['id']
  tname = team['abbreviation']
  team_df = commonteamroster.CommonTeamRoster(season=season, team_id=tid).get_data_frames()[0]
  # team_res = []
  lottery_prop = 0
  for player in team_df['PLAYER_ID']:
    pid = player
    player_df = commonplayerinfo.CommonPlayerInfo(player_id=pid).get_data_frames()[0]
    if len(player_df) > 0:
      pid = player_df['PERSON_ID'][0]
      pname = player_df['DISPLAY_FIRST_LAST'][0]
      player_pick = player_df['DRAFT_NUMBER'][0]
      lottery = int(player_pick) <= 14 if player_pick != 'Undrafted' and player_pick is not None else False
      lottery_prop += 1 if lottery is True else 0 
      # team_res['players'].append({'pid': pid, 'pname': pname, 'pick': player_pick, 'lottery': lottery})
      time.sleep(1)
  sum_teams.append({'team': tname, 'lottery_prop': lottery_prop / len(team_df['PLAYER_ID'])})
  # all_teams.append(team_res)

pd.DataFrame(sum_teams).to_csv("data/team_lottery.csv")