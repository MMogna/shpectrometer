import curses
from curses import wrapper
import textwrap

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
    return [box, box.derwin(height - 2, width - 3, 1, 2)]


def print_to_box(boxes, text):
    box = boxes[1]
    text=text.strip().rstrip()
    y, x = box.getmaxyx()
    box.addstr(0, 0, textwrap.fill(text, width=x -1, max_lines=y))
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
                     width=50,
                     height=25,
                     draw_border=True,
                     title="CPU info")

    ram = create_box(top=0,
                     left=84,
                     width=16,
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

    eng = create_box(top=26,
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
        "eng": eng
    }

    for i in items.values():
        print_to_box(i, text)

    stdscr.addstr(MAX_ROWS - 1 , 0, f" Press Q to quit. ", curses.color_pair(2))

    return items


def main(stdscr):
    global MAX_ROWS, MAX_COLS
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, 214, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.refresh()
    MAX_ROWS, MAX_COLS = stdscr.getmaxyx()
    items = draw_ui(stdscr=stdscr)

    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_RESIZE:
            MAX_ROWS, MAX_COLS = stdscr.getmaxyx()
            curses.resizeterm(MAX_ROWS, MAX_COLS)
            stdscr.clear()
            stdscr.refresh()
            try:
                items = draw_ui(stdscr=stdscr)
            except:
                stdscr.clear()
                stdscr.addstr(0, 0, "Terminal too small!", curses.color_pair(2))
        elif ch == ord('q'):
            break


wrapper(main)
