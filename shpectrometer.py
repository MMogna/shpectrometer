import curses
from curses import wrapper
import textwrap
from time import sleep

from host_explorer import print_host_info
from cpu_explorer import print_cpu_info
from ram_explorer import print_ram_info
from pci_explorer import print_pci_info
from net_explorer import print_nics
from pow_explorer import print_total_power

global MAX_ROWS, MAX_COLS


def create_box(top, left, width, height, draw_border=False, title=None):
    global MAX_ROWS, MAX_COLS

    curses.setsyx(0, 0)

    width = int(MAX_COLS * width / 100)
    height = int(MAX_ROWS * height / 100)
    top = int(MAX_ROWS * top / 100)
    left = int(MAX_COLS * left / 100)

    box = curses.newwin(height,
                        width,
                        top,
                        left)
    if draw_border:
        box.border(0, 0, 0, 0, 0, 0, 0, 0)
    if title:
        box.addstr(0, 2, f" {title} ", curses.color_pair(1))
    box.refresh()
    return [box, box.derwin(height - 2, width - 3, 2, 2)]


def print_to_box(boxes, text, wrap=True):
    box = boxes[1]
    text=text.strip().rstrip()
    y, x = box.getmaxyx()
    if wrap:
        box.addstr(0, 0, textwrap.fill(text, width=x -1, max_lines=y))
    else:
        text_list = text.split("\n")
        for i, t in enumerate(text_list):
            text_list[i] = textwrap.fill(t, width=x-1, break_long_words=False)
        text = '\n'.join(text_list[0:y-1])
        box.addstr(0, 0, text)
    box.refresh()


def draw_ui(stdscr):
    host = create_box(top=0,
                      left=0,
                      width=34,
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

    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel nulla leo. Sed sed felis hendrerit nisl faucibus faucibus. Morbi vitae dui metus. Proin vel orci vel nunc hendrerit sodales. Phasellus nisi magna, finibus nec fermentum at, facilisis sit amet lacus. Morbi in eros congue nisl ultricies finibus. Fusce eros nulla, semper a massa et, accumsan pellentesque tellus. Cras eu pharetra elit. Praesent laoreet posuere mi non suscipit. Vivamus ac fermentum orci. Vestibulum volutpat lorem ut congue ornare. Integer diam felis, facilisis sit amet lectus in, pulvinar mollis leo."

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
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, 214, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.refresh()
    MAX_ROWS, MAX_COLS = stdscr.getmaxyx()

    running = True

    items = draw_ui(stdscr=stdscr)

    print_info(items=items)

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
            except:
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
