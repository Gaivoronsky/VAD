import argparse
import os


def create_parser():
    """
    Parses each of the arguments from the command line
    :return ArgumentParser representing the command line arguments that were supplied to the command line:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--vad", help="mode operating VAD", type=int, default=1, choices=[0, 1, 2, 3])
    parser.add_argument("--file", help="path audio file")
    parser.add_argument("--save_dir", help="dir save split audio file")
    return parser


def main(args):
    if args.save_dir:
        if not os.path.exists(args.save_dir): os.mkdir(args.save_dir)
    if args.vad == 3:
        from exp_vad import VAD
        VadAudio = VAD(args.file, args.save_dir)
        timeline = VadAudio.scanning()

    else:
        from vad import VAD
        VadAudio = VAD(args.file, args.save_dir, mode=args.vad)
        timeline = VadAudio.scanning()
    print(timeline)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)