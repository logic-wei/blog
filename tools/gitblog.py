import argparse


def check_create_category(name):
    print("create_category", name)
    pass


def create_article(name, category=None):
    print("create_article", name, category)
    pass


def build_summary(path):
    print("build_summary", path)
    pass


def on_sub_create(args):
    check_create_category(args.category)
    if args.article:
        create_article(args.article, args.category)


def on_sub_summary(args):
    build_summary(args.directory)


def on_main(args):
    print("set option -h or --help for help")


def main():
    # parser setting
    mainparser = argparse.ArgumentParser()
    subparsers = mainparser.add_subparsers()
    # top level parser
    mainparser.add_argument("-v", "--version",
                            action="version",
                            version="v1.0")
    mainparser.set_defaults(func=on_main)
    # sub parser for create
    subparser_create = subparsers.add_parser("create",
                                             help="create a category or  start a new article")
    subparser_create.add_argument("-c", "--category",
                                  help="specify a category or create a new category")
    subparser_create.add_argument("-a", "--article",
                                  help="start a new article")
    subparser_create.set_defaults(func=on_sub_create)
    # sub parser for summary
    subparser_summary = subparsers.add_parser("summary", help="build summary")
    subparser_summary.add_argument("-d", "--directory",
                                   help="specify a directory to save summary")
    subparser_summary.set_defaults(func=on_sub_summary)
    # parse args
    args = mainparser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
