# -*- coding: utf-8 -*-
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


def is_article(path):
    path_main = os.path.join(path, "main.md")
    return os.path.exists(path_main) and os.path.isfile(path_main)


def build_summary_category(path):
    categorys_name = []
    articles_name = []
    # classify all files in articles
    for filename in os.listdir(path_articles):
        if is_article(os.path.join(path_articles, filename)):
            articles_name.append(filename)
        else:
            categorys_name.append(filename)
    with open(path, mode="w") as summary_file:
        summary_file.writelines("# CATEGORY\n\n")
        # handle every category
        for category_name in categorys_name:
            category_path = os.path.join(path_articles, category_name)
            subarticles_name = os.listdir(category_path)
            summary_file.writelines("## %s\n\n" % category_name)
            # handle every sub article
            for subarticle_name in subarticles_name:
                subarticle_path = os.path.join(category_path, subarticle_name)
                summary_file.writelines("- [%s](articles/%s/%s/main.md)\n" % (subarticle_name, category_name, subarticle_name))
        # handle every article without category
        summary_file.writelines("\n## undefined\n\n")
        for article_name in articles_name:
            summary_file.writelines("- [%s](articles/%s/main.md)\n" % (article_name, article_name))
        info(""+path+" has been created!")


def build_summary_date(path):
    pass


def build_summary(path):
    if path is None:
        path = path_root
    # list by category
    path_summary_category = os.path.join(path, "SUMMARY-CATEGORY.md")
    # list by date
    path_summary_date = os.path.join(path, "SUMMARY-DATE.md")
    # create summary file
    # open(path_summary_category, mode="a").close()
    # open(path_summary_date, mode="a").close()
    # modify summary file
    build_summary_category(path_summary_category)
    build_summary_date(path_summary_date)


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
