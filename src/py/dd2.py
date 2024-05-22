import urllib.request
import json
import threading
import time
from datetime import datetime
import sys

API_URL = "https://dips-plus-plus.xk.io/"
REFRESH_INTERVAL = 10
PLAYER_COUNT = 10
RELEASE_DATE = datetime(2024, 5, 3, 20, 00)
FINAL_HEIGHT = 1910

class LeaderboardEntry():
    def __init__(self, rank, wsid, height, ts, name, update_count, color):
        self.rank = rank
        self.wsid = wsid
        self.height = height
        self.ts = ts
        self.date = datetime.fromtimestamp(ts)
        self.name = name
        self.update_count = update_count
        self.color = color

class Player():
    def __init__(self, color, name, height, rank, ts, update_count, wsid):
        self.color = color
        self.name = name
        self.height = height
        self.rank = rank
        self.ts = ts
        self.date = datetime.fromtimestamp(ts)
        self.update_count = update_count
        self.wsid = wsid

class LiveEntry():
    def __init__(self, display_name, height, ts, rank, user_id):
        self.rank = rank
        self.display_name = display_name
        self.user_id = user_id
        self.height = height
        self.ts = ts
        self.date = datetime.fromtimestamp(ts)

class LiveHeight():
    def __init__(self, display_name, user_id, last_5_points):
        self.display_name = display_name
        self.user_id = user_id
        self.last_5_points = last_5_points

class ServerInfo():
    def __init__(self, nb_players_live):
        self.nb_players_live = nb_players_live

class Donations():
    def __init__(self, gfm_total, pp_total):
        self.gfm_total = gfm_total
        self.pp_total = pp_total

class Overview():
    def __init__(self, falls, falls_raw, floors_fallen, height_fallen, jumps, nb_players_climbing, nb_players_live, players, resets, sessions, ts):
        self.falls = falls,
        self.falls_raw = falls_raw
        self.floors_fallen = floors_fallen
        self.height_fallen = height_fallen
        self.jumps = jumps
        self.nb_players_climbing = nb_players_climbing
        self.nb_players_live = nb_players_live
        self.players = players
        self.resets = resets
        self.sessions = sessions
        self.ts = ts
        self.date = datetime.fromtimestamp(ts)

URLS = {
    LeaderboardEntry: "leaderboard/global",
    Player: "leaderboard/", LiveEntry: "live_heights/global",
    LiveHeight: "live_heights/",
    ServerInfo: "server_info",
    Overview: "overview",
    Donations: "donations",
}

def get_items(type):
    try:
        response = urllib.request.urlopen(API_URL + URLS[type])
        if response.status != 200:
            return []
        data = json.loads(response.read())
        return [ type(**item) for item in data ]
    except:
        return []


def get_item(type, param = None):
    try:
        url = API_URL + URLS[type] + (param if param else "")
        response = urllib.request.urlopen(url)
        if response.status != 200:
            return None
        return type(**json.loads(response.read()))
    except:
        return None


RED = 160
YELLOW = 226
GREEN = 28
NAME_WIDTH = 15
HEIGHT_FORMAT = "-7.2f"
RANK_FORMAT = 2
NUMBER_FORMAT = "_"

def hightlight(text, colour):
    return f"\033[48;5;{colour}m\033[38;5;0m{text}\033[0m"


def get_live_player_line(player, record, world, rank_width):
    if not player:
        return " " * (RANK_FORMAT + 2 + NAME_WIDTH + 1 + 7 + 2 + 7 + 1 + rank_width + 1)
    text = f"{player.rank:{RANK_FORMAT}}. {player.display_name:{NAME_WIDTH}} {player.height:{HEIGHT_FORMAT}} ({record.height:{HEIGHT_FORMAT}} {record.rank:-{rank_width}})"
    if player.height >= world * .9:
        return hightlight(text, RED)
    if player.height > record.height * .9:
        return hightlight(text, GREEN)
    if record.rank < 4:
        return wrap_podium_text(record.rank, text)
    return text


def time_delta_str(delta):
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    days_text = f"{delta.days:2}d" if delta.days else " " * 3
    hours_format = "02" if delta.days else "2"
    hours_text = f"{hours:{hours_format}}h" if delta.days or hours else " " * 3
    minutes_format = "02" if delta.days or hours else "2"
    minutes_text = f"{minutes:{minutes_format}}m" if delta.days or hours or minutes else " " * 3
    seconds_format = "02" if delta.days or hours or minutes else "2"
    return f"{days_text}{hours_text}{minutes_text}{seconds:{seconds_format}}s"


PODIUM_COLOURS = [0, 142, 246, 173]
def wrap_podium_text(rank, text):
    if rank > 3:
        return text
    return hightlight(text, PODIUM_COLOURS[rank])


def get_prize_text(donations):
    prize_text = f"Prize: ${donations.pp_total} ("
    prize_text += wrap_podium_text(1, f"1st ${donations.pp_total * .5:.2f}")
    prize_text += ", "
    prize_text += wrap_podium_text(2, f"2nd ${donations.pp_total * .3:.2f}")
    prize_text += ", "
    prize_text += wrap_podium_text(3, f"2nd ${donations.pp_total * .2:.2f}")
    prize_text += ")"
    return prize_text


def get_percentage_text(height):
    return f"({(height * 100) / FINAL_HEIGHT:5.2f}%)"


def show_data():
    global NAME_WIDTH
    overview = get_item(Overview)
    donations = get_item(Donations)
    live_heights = get_items(LiveEntry)[:PLAYER_COUNT]
    players = get_items(LeaderboardEntry)[:PLAYER_COUNT]
    live_records = dict()
    lowest_rank = 0
    for player in live_heights:
        live_records[player.user_id] = get_item(Player, player.user_id)
        lowest_rank = max(lowest_rank, live_records[player.user_id].rank if live_records[player.user_id] else 0)
    live_rank_width = len(str(lowest_rank))

    if not overview or not donations or not live_heights or not players or any([v is None for v in live_records.values()]):
        print(f"\033[38;5;{RED}mError calling API\033[0m", end="", flush=True)
    else:
        now = overview.date
        time_lapse = now - RELEASE_DATE
        world_record = players[0].height
        NAME_WIDTH = max([len(player.display_name) for player in live_heights] + [ NAME_WIDTH ])
        NAME_WIDTH = max([len(player.name) for player in players] + [ NAME_WIDTH ])
        print(f"\033[;HDeep Dip 2 - {time_delta_str(time_lapse)}")
        print(get_prize_text(donations))
        print(f"Session: {overview.sessions:{NUMBER_FORMAT}} Falls: {overview.falls[0]:{NUMBER_FORMAT}} Jumps: {overview.jumps:{NUMBER_FORMAT}} Resets: {overview.resets:{NUMBER_FORMAT}}")
        print(f"Players: Total: {overview.players:{NUMBER_FORMAT}} Live: {overview.nb_players_live:{NUMBER_FORMAT}} (updated {overview.date})")
        print(hightlight("Close to PB", GREEN), hightlight("Close to WR", RED))

        print("Live", " " * 41, "Leaderboard")

        live_count = len(live_heights)
        for index in range(PLAYER_COUNT):
            live_player = live_heights[index] if index < live_count else None
            record = live_records[live_player.user_id] if live_player else None
            leader = players[index]
            leader_text = f"{leader.rank:{RANK_FORMAT}}. {leader.name:{NAME_WIDTH}} {leader.height:{HEIGHT_FORMAT}} {get_percentage_text(leader.height)} ({time_delta_str(now - leader.date)})"
            leader_text = wrap_podium_text(leader.rank, leader_text)
            print(f"{get_live_player_line(live_player, record, world_record, live_rank_width)}", " \u2502 ", leader_text, "\033[0K")

    tick(REFRESH_INTERVAL)
        
ticker = None

def tick(time_left):
    global ticker
    if time_left:
        print(f"\033[;28H\033[0K{"." * time_left}", end=" ", flush=True)
        ticker = threading.Timer(1, tick, [time_left - 1])
        ticker.start()
    else:
        print(f"\033[;28H\033[0KUpdating...", end=" ", flush=True)
        show_data()


def main():
    print("\033[?25l", end="", flush=True)
    if len(sys.argv) > 1 and len(sys.argv) % 2 == 1:
        index = 0
        global PLAYER_COUNT, REFRESH_INTERVAL, RANK_FORMAT
        while index < len(sys.argv) // 2:
            param = sys.argv[index * 2 + 1]
            value = sys.argv[index * 2 + 2]
            if param == "-p":
                PLAYER_COUNT = int(value)
                RANK_FORMAT = len(str(PLAYER_COUNT))

            elif param == "-r":
                REFRESH_INTERVAL = int(value)
            index += 1

        
    print("\033[H\033[J", end="")
    try:
        show_data()
        while True:
            time.sleep(100)

    except KeyboardInterrupt:
        if ticker:
            ticker.cancel()
    finally:
        print("\033[?25h", end="", flush=True)



if __name__ == "__main__":
    main()
