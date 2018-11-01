# -*- coding: utf-8 -*-
import argparse
import os
import sys
import datetime
import re

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


# information table follows the markdown table:
# markdown table:                   # description:
# information | details             # head
# ------------|-----------          # divide
# date        | 2018-10-27          # date

pattern_headline = re.compile(r"^#.*")
pattern_info_head = re.compile(r"^\s*information\s*\|\s*details\s*$")
pattern_info_divide = re.compile(r"^\s*-*\s*\|\s*-*\s*$")
pattern_info_date = re.compile(r"^\s*date\s*\|\s*(\d*-\d*-\d*)\s*$")
pattern_info_author = re.compile(r"^\s*author\s*\|\s*(.*)\s*$")
patterns_info_supported = {
    "date": pattern_info_date,
    "author": pattern_info_author
}


def get_article_info(path):
    """
    get article's info
    :param path: article's name with path
    :return: return None or all of the supported info's value named info_value
    """
    info_value = dict()
    info("parse article info.file path:%s" % path)
    with open(path, "r") as article:
        line = article.readline()
        line_count = 1
        while line:
            if pattern_info_head.match(line):
                info("info table head found")
                line = article.readline()
                # effective info table
                if pattern_info_divide.match(line):
                    info("info table found")
                    line = article.readline()
                    # traverse every info list
                    while line:
                        is_supported = False
                        # query every supported key word
                        for info_key in patterns_info_supported.keys():
                            match = patterns_info_supported[info_key].match(line)
                            if match:
                                info("key word matched:%s" % info_key)
                                is_supported = True
                                info_value[info_key] = match.group(1)
                                break
                        # once any unsupported word appears,stop parsing
                        if is_supported is False:
                            info("the end of info table")
                            return info_value
                        line = article.readline()
                        if not line:
                            info("the end of info table because of eof")
                            return info_value
                else:
                    err("bad info table.return")
                    return None
            else:
                line_count += 1
                # info table has to be written in 10 lines
                if line_count > 10:
                    err("can't find info table in %d lines." % line_count)
                    return None
                line = article.readline()
    err("can't find any thing")
    return None


def build_summary_category(path):
    """
    build SUMMARY-CATEGORY.md at path
    :param path: SUMMARY-CATEGORY.md's full name with path
    :return: None
    """
    categorys_name = []
    articles_name = []
    # classify all files in articles
    for filename in os.listdir(path_articles):
        if is_article(os.path.join(path_articles, filename)):
            articles_name.append(filename)
        else:
            categorys_name.append(filename)
    # descending order
    categorys_name.sort()
    articles_name.sort()
    with open(path, mode="w") as summary_file:
        summary_file.writelines("# CATEGORY\n\n")
        # handle every category
        for category_name in categorys_name:
            category_path = os.path.join(path_articles, category_name)
            subarticles_name = os.listdir(category_path)
            # descending order
            subarticles_name.sort()
            summary_file.writelines("## %s\n\n" % category_name)
            # handle every sub article
            for subarticle_name in subarticles_name:
                subarticle_path = os.path.join(category_path, subarticle_name)
                summary_file.writelines("- [%s](articles/%s/%s/main.md)\n" % (subarticle_name, category_name, subarticle_name))
            summary_file.writelines("\n")
        # handle every article without category
        summary_file.writelines("## undefined\n\n")
        for article_name in articles_name:
            summary_file.writelines("- [%s](articles/%s/main.md)\n" % (article_name, article_name))
        info(""+path+" has been created!")


def build_summary_date(path):
    """
    build SUMMARY-DATE.md at path
    :param path: SUMMARY-DATE.md's full name with path
    :return: None
    """
    pass


def build_summary(path):
    """
    build all the summary at path
    :param path: where to save summary files without filename
    :return: None
    """
    if path is None:
        path = path_root
    # list by category
    path_summary_category = os.path.join(path, "SUMMARY-CATEGORY.md")
    # list by date
    path_summary_date = os.path.join(path, "SUMMARY-DATE.md")
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
        article.writelines("# %s\n\n" % name)                       # headline
        article.writelines("information | details\n")               # table head
        article.writelines("------------|--------\n")               # table divide
        article.writelines("date | %s\n" % datetime.date.today())   # date
    info("path:%s" % path_article)
    info("date:%s" % datetime.date.today())
    info("article %s has been created!" % name)


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
