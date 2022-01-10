import cv2
import os
import sys
import datetime


def auto_mode(image_path, continuous_mode):
    img = cv2.imread(image_path, 1)
    img = cv2.flip(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE), 0)
    terminal_size = None

    while True:
        if terminal_size != os.get_terminal_size():
            terminal_size = os.get_terminal_size()
            print_width = int(terminal_size[0] / 3)
            print_height = int(terminal_size[1]) - 2
            width, height, channels = img.shape
            scale_x = width / print_width
            scale_y = height / print_height
            os.system('cls' if os.name == 'nt' else 'clear')
            print(frame_to_ascii(img, print_width, print_height, scale_x, scale_y))

        if not continuous_mode:
            break


def custom_res_mode(image_path, print_width, print_height):
    img = cv2.imread(image_path, 1)
    img = cv2.flip(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE), 0)

    width, height, channels = img.shape
    scale_x = width / print_width
    scale_y = height / print_height
    print(frame_to_ascii(img, print_width, print_height, scale_x, scale_y))


def frame_to_ascii(frame, width, height, scale_x, scale_y):
    lines = ''

    for line_y in range(height):
        y = int(line_y * scale_y)
        line = ''

        for line_x in range(width):
            x = int(line_x * scale_x)
            brightness = int(frame[x, y, 0]) + int(frame[x, y, 1]) + int(frame[x, y, 2])

            if brightness > 640:
                line += '@@@'
            elif brightness > 570:
                line += '$$$'
            elif brightness > 510:
                line += '&&&'
            elif brightness > 450:
                line += '###'
            elif brightness > 410:
                line += '%%%'
            elif brightness > 350:
                line += '***'
            elif brightness > 300:
                line += '+++'
            elif brightness > 260:
                line += '==='
            elif brightness > 210:
                line += '"""'
            elif brightness > 175:
                line += '---'
            elif brightness > 140:
                line += ':::'
            elif brightness > 105:
                line += "'''"
            elif brightness > 70:
                line += '...'
            else:
                line += '   '

        lines += line + '\n'

    return lines


if __name__ == '__main__':
    import sys
    import getopt

    x = None
    y = None
    continuous = False
    usage = f'Usage: {sys.argv[0]} [-h help] [-x width] [-y height] [-c continuous mode] <image>'

    opts, args = getopt.getopt(sys.argv[1:], 'x:y:hc')
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt == '-x':
            x = int(arg)
        elif opt == '-y':
            y = int(arg)
        elif opt == '-c':
            continuous = True
        else:
            print('Bad option', opt)
            print(usage)
            sys.exit()

    if x and y:
        custom_res_mode(args[0], x, y)
    elif x or y:
        print('Invalid size arguments')
        print(usage)
        sys.exit()
    else:
        auto_mode(args[0], continuous)
