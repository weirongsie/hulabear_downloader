# -*- coding: utf8 -*-
import telnetlib
import ConfigParser
from board import Board


class Hulabear:
    def __init__(self, host, account, password):
        self._host = host
        self._account = account
        self._password = password

        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self._timeout = self.config.getint("host", "timeout")
        print "set bbs timeout = " + str(self._timeout) + "s"

    def login(self):
        print "start to login as %s....." % str(self._account)
        self._tn = ChineseTelnet(self._host, self._timeout)
        if self._tn.expect_list([u"請輸入代號："]) == -1:
            raise KeyError("cannot enter account")
        self._tn.write(self._account + '\r\n')
        print "enter account."

        if self._tn.expect_list([u"請輸入密碼："]) == -1:
            raise KeyError("cannot enter account")
        self._tn.write(self._password + '\r\n')
        print "enter password."

        if self._tn.expect_list([u"您想刪除其他重複的 login"]) != -1:
            print "delete duplicated login."
            self._tn.write('y\r\n')

        # skip login info, hot topics, message bord
        skip_cnt = 0
        while self._tn.expect_list([u"看板《尚未選定》"]) == -1:
            skip_cnt += 1
            print "skipped " + str(skip_cnt) + " / 3 login page..."               
            self._tn.write('\r\n')
        print "login successfully."

    def enter_board(self, board_name):
        self._tn.write('b\r\n')         # enter board list
        if self._tn.expect_list([u"看板列表"]) == -1:
            with open('error.log', 'a') as f:
                f.write(self.buffer)
            raise KeyError("expect board list but not. check error.log for details")
        board = Board(board_name, self._tn)
        board.enter()
        return board


class ChineseTelnet(telnetlib.Telnet, object):
    def __init__(self, host, timeout):
        self._timeout = timeout
        super(ChineseTelnet, self).__init__(host)

    def expect_list(self, list):
        encoded = [s.encode("big5") for s in list]
        index, matched, text = super(ChineseTelnet, self).expect(encoded, self._timeout)
        return index