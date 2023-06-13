import curses
from _curses import error as CursesError
from curses import wrapper
import textwrap
from os import environ, geteuid

from host_explorer import print_host_info
from cpu_explorer import print_cpu_info
from ram_explorer import print_ram_info
from pci_explorer import print_pci_info
from net_explorer import print_nics
from pow_explorer import print_total_power

def check_privileges():
    if not environ.get("SUDO_UID") and geteuid() != 0:
        raise PermissionError("You need to run this script with sudo or as root.")

check_privileges()

global MAX_ROWS, MAX_COLS

curses.initscr()
if curses.has_colors():
    curses.start_color()
    curses.init_pair(1, 214, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, 214)

def get_info():
    output = ""
    output += "Created by Elemento Cloud\n"
    output += "Visit www.elemento.cloud\n"
    output += "v 0.1.0\n"
    return output


def create_box(top, left, width, height, draw_border=False, title=None, fill=False, bg=None):
    global MAX_ROWS, MAX_COLS

    curses.setsyx(0, 0)

    width = int(MAX_COLS * width / 100)
    height = int(MAX_ROWS * height / 100)
    top = int(MAX_ROWS * top / 100)
    left = int(MAX_COLS * left / 100)

    if left + width > MAX_COLS:
        width = MAX_COLS - left
    if top + height > MAX_ROWS:
        height = MAX_ROWS - top

    box = curses.newwin(height,
                        width,
                        top,
                        left)
    if draw_border:
        box.border(0, 0, 0, 0, 0, 0, 0, 0)
    if title:
        box.addstr(0, 2, f" {title} ", curses.color_pair(1) | curses.A_BOLD)
    box.refresh()
    if not fill:
        der = box.derwin(height - 3, width - 4, 2, 2)
    else:
        der = box.derwin(height - 2, width -2, 1, 1)
    if bg:
        der.bkgd(' ', curses.color_pair(bg))
    return [box, der]


def print_to_box(boxes, text, wrap=True, cp=None):
    box = boxes[1]
    text=text.strip().rstrip()
    y, x = box.getmaxyx()
    if wrap:
        box.addstr(0, 0, textwrap.fill(text, width=x -1, max_lines=y), cp or  curses.color_pair(3))
    else:
        text_list = text.split("\n")
        for i, t in enumerate(text_list):
            text_list[i] = textwrap.fill(t, width=x-1, break_long_words=False)
        text = '\n'.join(text_list[0:y-1])
        box.addstr(0, 0, text, cp or  curses.color_pair(3))
    box.refresh()


def draw_ui(stdscr):
    logo = create_box(top=0,
                      left=0,
                      width=16,
                      height=25,
                      draw_border=True,
                      fill=False,
                      title="Elemento Shell Meter")
    host = create_box(top=0,
                      left=16,
                      width=18,
                      height=25,
                      draw_border=True,
                      title="Host info")

    cpu = create_box(top=0,
                     left=34,
                     width=25,
                     height=25,
                     draw_border=True,
                     title="CPU info")

    ram = create_box(top=0,
                     left=59,
                     width=41,
                     height=25,
                     draw_border=True,
                     title="RAM info")

    net = create_box(top=26,
                     left=0,
                     width=25,
                     height=74,
                     draw_border=True,
                     title="Network info")

    dsk = create_box(top=26,
                     left=25,
                     width=25,
                     height=74,
                     draw_border=True,
                     title="Disk info")

    pci = create_box(top=26,
                     left=50,
                     width=25,
                     height=74,
                     draw_border=True,
                     title="PCIe info")

    pow = create_box(top=26,
                     left=75,
                     width=25,
                     height=74,
                     draw_border=True,
                     title="Power info")

    items = {
        "host": host,
        "cpu": cpu,
        "ram": ram,
        "net": net,
        "dsk": dsk,
        "pci": pci,
        "pow": pow
    }

    stdscr.addstr(MAX_ROWS - 1 , 0, f" Press Q to quit. ", curses.color_pair(2))
    stdscr.addstr(MAX_ROWS - 1 , 18, f" Press R to refresh. ", curses.color_pair(1))

    y, x = logo[0].getmaxyx()
    box = curses.newwin(y,
                        x,
                        0,
                        0)

    print_to_box(logo, get_info(), wrap=False, cp = curses.A_BOLD)

    return items


def print_info(items):
    print_to_box(items["host"], print_host_info(), wrap=False)
    print_to_box(items["cpu"], print_cpu_info(), wrap=False)
    print_to_box(items["ram"], print_ram_info(), wrap=False)
    print_to_box(items["pci"], print_pci_info(), wrap=False)
    print_to_box(items["net"], print_nics(), wrap=False)
    print_to_box(items["pow"], print_total_power(), wrap=False)


def main(stdscr):
    global MAX_ROWS, MAX_COLS

    stdscr.refresh()
    MAX_ROWS, MAX_COLS = stdscr.getmaxyx()

    running = True

    try:
        items = draw_ui(stdscr=stdscr)
        print_info(items=items)
    except CursesError:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small!", curses.color_pair(2))

    running = True

    while running:
        ch = stdscr.getch()
        if ch == curses.KEY_RESIZE:
            MAX_ROWS, MAX_COLS = stdscr.getmaxyx()
            curses.resizeterm(MAX_ROWS, MAX_COLS)
            stdscr.erase()
            stdscr.refresh()
            try:
                items = draw_ui(stdscr=stdscr)
                print_info(items=items)
            except CursesError:
                stdscr.clear()
                stdscr.addstr(0, 0, "Terminal too small!", curses.color_pair(2))
        elif ch == ord('q'):
            running = False
            curses.endwin()
        elif ch == ord('r'):
            print_info(items=items)
            for i in items.values():
                i[1].refresh()
        curses.doupdate()
        curses.flushinp()


wrapper(main)
# if __name__ == "__main__":
    # print(get_info())
