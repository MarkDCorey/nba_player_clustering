from nba_py import _api_scrape, _get_json, player, league, game, shotchart, team, draftcombine, constants
import pandas as pd
import numpy as np
from datetime import datetime
import time
from scrape import get_player_ids

player_ids = get_player_ids()
