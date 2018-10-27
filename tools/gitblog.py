import argparse
import os
import sys
import datetime

# cross platform path
path_root = os.getcwd()
path_articles = os.path.join(os.getcwd(), "articles")


def err(msg):
    print("error:"+msg, file=sys.stderr)


def info(msg):
    print("info:"+msg, file=sys.stdout)


def check_create_category(name):
    if name:
        files = os.listdir(path_articles)
        if name in files:
            info("category "+name+" is already existed.")
            return
        else:
            os.mkdir(os.path.join(path_articles, name))
            info("directory "+name+" has been created.")


def create_article(name, category=None):
    # where to create article
    path_category = path_articles
    if category:
        path_category = os.path.join(path_articles, category)
    # check file name conflict
    files = os.listdir(path_category)
    if name in files:
        err("repetitive article:"+name)
        return
    # create new article
    path_article = os.path.join(path_category, name)
    os.mkdir(path_article)
    path_main_md = os.path.join(path_article, "main.md")
    with open(path_main_md, mode="a") as article:
        article.writelines("# %s\n\n" % name)
        article.writelines("date:%s\n" % datetime.date.today())
    info("article %s has been created!" % name)
    info("path:%s" % path_article)
    info("date:%s" % datetime.date.today())


def build_summary(path):
    info("build_summary", path)


def on_sub_create(args):
    check_create_category(args.category)
    if args.article:
        create_article(args.article, args.category)


def on_sub_summary(args):
    build_summary(args.directory)


def on_main(args):
    info("set option -h or --help for help")


def main():
    # parser setting
    mainparser = argparse.ArgumentParser()
    subparsers = mainparser.add_subparsers()
    # top level parser
    mainparser.add_argument("-v", "--version",
                            action="version",
                            version="none")
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
