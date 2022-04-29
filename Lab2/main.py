import argparse
import sys

from serializer_lib.factory.factory import Factory


def parse(from_file, to_file, from_type, to_type):
    serializer_from = Factory.get_parser(from_type)
    serializer_to = Factory.get_parser(to_type)

    result = serializer_from.load(from_file)

    serializer_to.dump(result, to_file)


def main():
    argsparser = argparse.ArgumentParser(description="Custom serializer")
    argsparser.add_argument("-config", dest="config", type=str, help="Parse config")
    argsparser.add_argument("-from_file", dest="from_file", type=str, help="From file")
    argsparser.add_argument("-to_file", dest="to_file", type=str, help="To file")
    argsparser.add_argument("-from_type", dest="from_type", type=str, help="From format type")
    argsparser.add_argument("-to_type", dest="to_type", type=str, help="To format type")

    parse_args = argsparser.parse_args()

    from_file = ""
    to_file = ""
    from_type = ""
    to_type = ""

    if parse_args.config is not None:
        with open("config.txt", "r") as f:
            config = eval(f.read())

        from_file = config["from_file"]
        to_file = config["to_file"]
        from_type = config["from_type"]
        to_type = config["to_type"]
    else:
        from_file = parse_args.from_file
        to_file = parse_args.to_file
        from_type = parse_args.from_type
        to_type = parse_args.to_type

    if from_file == "" or to_file == "" or from_type == "" or to_type == "" or from_type == to_type:
        print("Input format = output format or one of args is missing")
        sys.exit()
    else:
        parse(from_file, to_file, from_type, to_type)


if __name__ == '__main__':
    main()
