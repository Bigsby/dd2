import threading
from datetime import datetime
import sys
import os
from api import get_data
from console import ESC, COLOURS, FORMATS


REFRESH_INTERVAL = 10
PLAYER_COUNT = 10
RELEASE_DATE = datetime(2024, 5, 3, 20, 00)
FINAL_HEIGHT = 1910


def get_live_player_line(player, record, world, rank_width, count):
    if not player:
        return " " * (FORMATS.RANK + 2 + FORMATS.NAME + 1 + 7 + 2 + 7 + 1 + rank_width + 1)
    record_text = f"({record.height:{FORMATS.HEIGHT}} {record.rank:-{rank_width}})" if record else "(" + " " * (rank_width + 8) + ")" 
    text = f"{player.rank:{FORMATS.RANK}}. {player.display_name[:FORMATS.NAME]:{FORMATS.NAME}} {player.height:{FORMATS.HEIGHT}} {record_text}"
    if player.height >= world * .95:
        return COLOURS.text(text, COLOURS.WHITE, COLOURS.RED)
    if record:
        if player.height > record.height * .9:
            return COLOURS.text(text, COLOURS.WHITE, COLOURS.GREEN)
        if record.rank < 4: 
            return COLOURS.podium(record.rank, text)
        if record.rank < 11:
            return COLOURS.text(text, COLOURS.WHITE, COLOURS.BLUE)
        if record.rank <= count:
            return COLOURS.text(text, COLOURS.WHITE, COLOURS.DARK_GREY)
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


def get_prize_text(donations):
    prize_text = f"Prize: ${donations.pp_total:{FORMATS.CURRENCY}} ("
    prize_text += COLOURS.podium(1, f"1st ${donations.pp_total * .5:{FORMATS.CURRENCY}}")
    prize_text += ", "
    prize_text += COLOURS.podium(2, f"2nd ${donations.pp_total * .3:{FORMATS.CURRENCY}}")
    prize_text += ", "
    prize_text += COLOURS.podium(3, f"3rd ${donations.pp_total * .2:{FORMATS.CURRENCY}}")
    prize_text += ")"
    return prize_text


def get_percentage_text(height):
    return f"({(height * 100) / FINAL_HEIGHT:5.2f}%)"


def show_data():
    data = get_data(PLAYER_COUNT)
    # print(data); input()
    overview, donations, live_heights, players, live_records, lowest_rank = data
    live_rank_width = len(str(lowest_rank))

    if not overview or not donations or not live_heights or not players:
        ESC.position(1,0)
        ESC.write(COLOURS.text("API Error!", COLOURS.RED, COLOURS.BLACK))
    else:
        now = datetime.now()
        time_lapse = now - RELEASE_DATE
        world_record = players[0].height
        ESC.position(0,0)
        print(f"{COLOURS.BOLD}Deep Dip 2 {COLOURS.CLEAR_COLOURS}- {time_delta_str(time_lapse)} {ESC.CLEAR_LINE}")
        if donations:
            print(get_prize_text(donations))
        if overview:
            print(f"Sessions: {overview.sessions:{FORMATS.NUMBER}} Falls: {overview.falls[0]:{FORMATS.NUMBER}} Jumps: {overview.jumps:{FORMATS.NUMBER}} Resets: {overview.resets:{FORMATS.NUMBER}}")
            print(f"Players: Total: {overview.players:{FORMATS.NUMBER}} Live: {overview.nb_players_live:{FORMATS.NUMBER}} (updated {overview.date}){ESC.CLEAR_LINE}")
        print(COLOURS.text("Close to PB", COLOURS.WHITE, COLOURS.GREEN), COLOURS.text("Close to WR", COLOURS.WHITE, COLOURS.RED))

        print("Leaderboard", " " * 43, "Live")

        live_count = len(live_heights)
        for index in range(PLAYER_COUNT):
            live_player = live_heights[index] if index < live_count else None
            record = live_records[live_player.user_id] if live_player else None
            leader = players[index]
            leader_text = f"{leader.rank:{FORMATS.RANK}}. {leader.name[:FORMATS.NAME]:{FORMATS.NAME}} {leader.height:{FORMATS.HEIGHT}} {get_percentage_text(leader.height)} ({time_delta_str(now - leader.date)})"
            leader_text = COLOURS.podium(leader.rank, leader_text)
            print(leader_text, " \u2502 ", get_live_player_line(live_player, record, world_record, live_rank_width, PLAYER_COUNT), "\033[0K")

    tick(REFRESH_INTERVAL)


def tick(time_left):
    global ticker
    if time_left:
        ESC.position(0, 28)
        ESC.clear_line()
        ESC.write("." * time_left)
        ticker = threading.Timer(1, tick, [time_left - 1]).start()
    else:
        ESC.position(0, 28)
        ESC.clear_line()
        ESC.write("Updating...")
        show_data()


def main():
    ESC.enable_alt_buffer()
    ESC.hide_cursor()
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
        
    ESC.position(0, 0)
    ESC.clear_screen()
    try:
        show_data()
    except KeyboardInterrupt:
        if ticker:
            ticker.cancel()
        ESC.disable_alt_buffer()
        ESC.show_cursor()
        os._exit(0)
    finally:
        ESC.disable_alt_buffer()
        ESC.show_cursor()



if __name__ == "__main__":
    main()
