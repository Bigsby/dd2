class FORMATS:
    NAME = 15
    HEIGHT = "-7.2f"
    RANK = 2
    NUMBER = "_"
    CURRENCY = ".2f"


class ESC:
    CSI = "\033["
    CLEAR_LINE = CSI + "0K"

    @staticmethod
    def write(text):
        print(text, end="", flush=True)

    @staticmethod
    def clear_line():
        ESC.write(f"{ESC.CSI}0K")

    @staticmethod
    def clear_all_screen():
        ESC.write(f"{ESC.CSI}0J")

    @staticmethod
    def clear_screen():
        ESC.write(f"{ESC.CSI}0J")

    @staticmethod
    def position(row, column):
        ESC.write(f"{ESC.CSI}{row};{column}H")

    @staticmethod
    def hide_cursor():
        ESC.write(f"{ESC.CSI}?25l")

    @staticmethod
    def show_cursor():
        ESC.write(f"{ESC.CSI}?25h")

    @staticmethod
    def enable_alt_buffer():
        ESC.write(f"{ESC.CSI}7{ESC.CSI}?47h")

    @staticmethod
    def disable_alt_buffer():
        ESC.write(f"{ESC.CSI}[2J{ESC.CSI}?47l{ESC.CSI}8")

    # @staticmethod
    # def enable_focus_report():
    #     ESC.write(f"{ESC.CSI}?1004h")


class COLOURS:
    RED = 124
    GREEN = 28
    BLUE = 17
    BLACK = 0
    WHITE = 7
    GOLD = 3
    SILVER = 248
    BRONZE = 173
    DARK_GREY = 236

    CLEAR_COLOURS = "\033[0m"
    BOLD = "\033[1m"

    @staticmethod
    def background(colour):
        return f"{ESC.CSI}48;5;{colour}m"

    @staticmethod
    def foreground(colour):
        return f"{ESC.CSI}38;5;{colour}m"

    @staticmethod
    def text(text, foreground, background):
        return f"{COLOURS.background(background)}{COLOURS.foreground(foreground)}{text}{COLOURS.CLEAR_COLOURS}"

    PODIUM_COLOURS = [BLACK, GOLD, SILVER, BRONZE]
    @staticmethod
    def podium(rank, text):
        if rank > 10:
            return COLOURS.text(text, COLOURS.WHITE, COLOURS.DARK_GREY)
        if rank > 3:
            return COLOURS.text(text, COLOURS.WHITE, COLOURS.BLUE)
        return COLOURS.text(text, COLOURS.BLACK, COLOURS.PODIUM_COLOURS[rank])

