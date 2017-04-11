import sys

progress_pos = 0
step = 1

def print_progressbar(progress=None):
    """

    :param progress: Progress between 0 and 1 
    """
    global progress_pos
    global step
    sys.stdout.write('\r')
    # the exact output you're looking for:
    if progress is None:
        sys.stdout.write('▕{0:░<20}▏'.format('░' * progress_pos + '█'))
        progress_pos += step
        if progress_pos % 19 == 0:
            step *= -1
    else:
        int_progress = int(progress * 20)
        bar = '█' * int_progress
        last_block_percentage = progress * 20 - int_progress
        bar += chr(ord('█') + round(7 - last_block_percentage * 7))
        sys.stdout.write('▕{0:20}▏ {1:03.2f}%'.format(bar, progress * 100))
    sys.stdout.flush()