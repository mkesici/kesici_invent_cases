import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-date', type=str, required=False, default="2021-01-08")
    parser.add_argument('--max-date', type=str, required=False, default="2021-05-30")
    parser.add_argument('--top', type=int, required=False, default=5)

    args = parser.parse_args()

    if args.min_date > args.max_date:
        raise ValueError("min-date cannot be greater than max-date")
    elif args.top < 1:
        raise ValueError("top cannot be less than 1")

    return args