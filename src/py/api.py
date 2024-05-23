import urllib.request
import json
from models import LeaderboardEntry, Player, LiveEntry, LiveHeight, ServerInfo, Overview, Donations


API_URL = "https://dips-plus-plus.xk.io/"

URLS = {
    LeaderboardEntry: "leaderboard/global",
    Player: "leaderboard/", LiveEntry: "live_heights/global",
    LiveHeight: "live_heights/",

    ServerInfo: "server_info",
    Overview: "overview",
    Donations: "donations",
}


def get_item(type, param = None):
    try:
        url = API_URL + URLS[type] + (param if param else "")
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return None
        return type(**json.loads(response.read()))
    except:
        return None


def get_items(type):
    try:
        response = urllib.request.urlopen(API_URL + URLS[type])
        if response.status != 200:
            return []
        data = json.loads(response.read())
        return [ type(**item) for item in data ]
    except:
        return []


def get_data(player_count):
    overview = get_item(Overview)
    donations = get_item(Donations)
    live_heights = get_items(LiveEntry)[:player_count]
    players = get_items(LeaderboardEntry)[:player_count]
    live_records = dict()
    lowest_rank = 0
    for player in live_heights:
        live_records[player.user_id] = get_item(Player, player.user_id)
        lowest_rank = max(lowest_rank, live_records[player.user_id].rank if live_records[player.user_id] else 0)
    return (overview, donations, live_heights, players, live_records, lowest_rank)
