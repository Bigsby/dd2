from datetime import datetime


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
    def __init__(self, display_name, height, ts, rank, user_id, color, pos, vel):
        self.rank = rank
        self.display_name = display_name
        self.user_id = user_id
        self.height = height
        self.ts = ts
        self.date = datetime.fromtimestamp(ts)
        self.color = color,
        self.pos = pos
        self.vel = vel


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
    def __init__(self, falls, falls_raw, floors_fallen, height_fallen, jumps, nb_players_climbing, nb_players_live, players, resets, sessions, ts, nb_climbing_shallow_dip):
        self.falls = falls,
        self.falls_raw = falls_raw
        self.floors_fallen = floors_fallen
        self.height_fallen = height_fallen
        self.jumps = jumps
        self.nb_players_climbing = nb_players_climbing
        self.nb_climbing_shallow_dip = nb_climbing_shallow_dip
        self.nb_players_live = nb_players_live
        self.players = players
        self.resets = resets
        self.sessions = sessions
        self.ts = ts
        self.date = datetime.fromtimestamp(ts)
