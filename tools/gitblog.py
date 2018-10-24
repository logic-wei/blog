import argparse


def create_category(name):
    print("create_category", name)
    pass


def create_article(name, category=None):
    print("create_article", name, category)
    pass


def build_summary(path):
    print("build_summary", path)
    pass


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("command",
                           choices=("create", "summary"),
                           nargs="?")
    argparser.add_argument("-c", "--category",
                           help="specify a category or create a new category")
    argparser.add_argument("-a", "--article",
                           help="start a new article")
    argparser.add_argument("-d", "--directory",
                           help="specify a directory to save summary")
    argparser.add_argument("-v", "--version",
                           action="version",
                           version="v1.0")
    args = argparser.parse_args()
    if args.command:
        if args.command == "create":
            if args.article:
                create_article(args.article, args.category)
            else:
                create_category(args.category)
        elif args.command == "summary":
            build_summary(args.directory)
        else:
            print("command can't be supported!")
    else:
        print("command not found!")


if __name__ == "__main__":
    main()
