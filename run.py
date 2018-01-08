# -*- coding: utf8 -*-
import ConfigParser
import argparse

from hulabear import Hulabear

config = ConfigParser.ConfigParser()
config.read("config.ini")


arg_parser = argparse.ArgumentParser(description='-a account -p password -b bord -s article start -e article end')
arg_parser.add_argument('-a', help='your hulabear account')
arg_parser.add_argument('-p', help='your hulabear password')
arg_parser.add_argument('-b', help='bord name you want to download')
arg_parser.add_argument('-s', help='what is the first article number to download (started from 1)')
arg_parser.add_argument('-e', help='what is the last article number to download')
args = arg_parser.parse_args()


host = config.get("host", "host")
config = ConfigParser.ConfigParser()
hulabear = Hulabear(host, args.a, args.p)
hulabear.login()
board = hulabear.enter_board(args.b)
folder = "download_" + str(board.name)
board.download(folder, args.s, args.e)
