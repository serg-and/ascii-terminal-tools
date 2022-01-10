import cv2
from multiprocessing import Pool, cpu_count
import datetime
import os
import sys


def direct_mode(video):
    cap = cv2.VideoCapture(video)
    os.system('cls' if os.name == 'nt' else 'clear')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        print_width = int(os.get_terminal_size()[0]/3)
        print_height = int(os.get_terminal_size()[1])-2
        frame = cv2.flip(cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE), 0)
        width, height, channels = frame.shape
        scale_x = width / print_width
        scale_y = height / print_height

        sys.stdout.write(f'\033[{print_height + 1}F')
        print(frame_to_ascii(frame, print_width, print_height, scale_x, scale_y))

    cap.release()
    cv2.destroyAllWindows()
    os.system('cls' if os.name == 'nt' else 'clear')


def direct_custom_res_mode(video, print_width, print_height):
    cap = cv2.VideoCapture(video)
    os.system('cls' if os.name == 'nt' else 'clear')
    jump_height = print_height + 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE), 0)
        width, height, channels = frame.shape
        scale_x = width / print_width
        scale_y = height / print_height

        sys.stdout.write(f'\033[{jump_height}F')
        print(frame_to_ascii(frame, print_width, print_height, scale_x, scale_y))

    cap.release()
    cv2.destroyAllWindows()
    os.system('cls' if os.name == 'nt' else 'clear')


def preload_mode(video):
    cap = cv2.VideoCapture(video)
    frame_time = datetime.timedelta(seconds=(1 / int(cap.get(cv2.CAP_PROP_FPS))))
    segment_size = cv2.VideoCapture(video).get(cv2.CAP_PROP_FRAME_COUNT) / cpu_count()
    print_width = int(os.get_terminal_size()[0] / 3)
    print_height = int(os.get_terminal_size()[1]) - 2
    jump_height = print_height + 1
    values = []

    for process in range(cpu_count()):
        start_frame = process * int(segment_size)
        end_frame = ((process + 1) * int(segment_size)) - 1
        values.append((video, start_frame, end_frame, print_width, print_height))

    with Pool() as pool:
        res = pool.starmap(worker, values)

    ascii_frames = []
    for lst in res:
        ascii_frames += lst

    os.system('cls' if os.name == 'nt' else 'clear')

    for frame in ascii_frames:
        stamp = datetime.datetime.now() + frame_time
        sys.stdout.write(f'\033[{jump_height}F')
        print(frame)

        while datetime.datetime.now() < stamp:
            continue

    cap.release()
    os.system('cls' if os.name == 'nt' else 'clear')


def preload_custom_res_mode(video, print_width, print_height):
    cap = cv2.VideoCapture(video)
    frame_time = datetime.timedelta(seconds=(1 / int(cap.get(cv2.CAP_PROP_FPS))))
    segment_size = cv2.VideoCapture(video).get(cv2.CAP_PROP_FRAME_COUNT) / cpu_count()
    jump_height = print_height + 1
    values = []

    for process in range(cpu_count()):
        start_frame = process * int(segment_size)
        end_frame = ((process + 1) * int(segment_size)) - 1
        values.append((video, start_frame, end_frame, print_width, print_height))

    with Pool() as pool:
        res = pool.starmap(worker, values)

    ascii_frames = []
    for lst in res:
        ascii_frames += lst

    os.system('cls' if os.name == 'nt' else 'clear')

    for frame in ascii_frames:
        stamp = datetime.datetime.now() + frame_time
        sys.stdout.write(f'\033[{jump_height}F')
        print(frame)

        while datetime.datetime.now() < stamp:
            continue

    cap.release()
    os.system('cls' if os.name == 'nt' else 'clear')


def worker(video, start, end, print_width, print_height):
    cap = cv2.VideoCapture(video)
    cap.set(1, start)
    total_frames = end - start
    ascii_frames = []

    while cap.get(cv2.CAP_PROP_POS_FRAMES) < end:
        if start == 0:
            progress_bar(cap.get(cv2.CAP_PROP_POS_FRAMES), total_frames, (print_width, print_height))

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE), 0)
        width, height, channels = frame.shape
        scale_x = width / print_width
        scale_y = height / print_height
        ascii_frames.append(frame_to_ascii(frame, print_width, print_height, scale_x, scale_y))

    cap.release()
    return ascii_frames


def progress_bar(current, total, window_size, barLength = 25):
    percent = float(current) * 100 / total
    arrow = '█' * int(percent/100 * barLength)
    spaces = ' ' * (barLength - len(arrow))

    print('='*54 + '\n  Using initial window size: %sx%s' % (round(window_size[0]/3), window_size[1])
          + '\n  Preloading video: |%s%s| %d %%\n' % (arrow, spaces, percent) + '='*54 + '\n', end='\r')
    sys.stdout.write('\033[4F')


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
    preload = False
    usage = f'Usage: {sys.argv[0]} [-h help] [-x width] [-y height] [-p] <video>'

    opts, args = getopt.getopt(sys.argv[1:], 'x:y:hp')
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt == '-x':
            x = int(arg)
        elif opt == '-y':
            y = int(arg)
        elif opt in ['-p', '--preload']:
            preload = True
        else:
            print('Bad option', opt)
            print(usage)
            sys.exit()

    if preload:
        if x and y:
            preload_custom_res_mode(args[0], x, y)
        elif x or y:
            print('Invalid size arguments')
            print(usage)
            sys.exit()
        else:
            preload_mode(args[0])
    else:
        if x and y:
            direct_custom_res_mode(args[0], x, y)
        elif x or y:
            print('Invalid size arguments')
            print(usage)
            sys.exit()
        else:
            direct_mode(args[0])
