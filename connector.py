# -*- coding: utf8 -*-
import telnetlib
import ConfigParser
import time
import os
import formatter


class Connector:
    def __init__(self, host, account, password):
        self._host = host
        self._account = account
        self._password = password
        self._formatter = formatter.Formatter()

        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")
        self._timeout = self.config.getint("host", "timeout")
        print "set bbs timeout = " + str(self._timeout) + "s"

    def expect(self, list):
        encoded = [s.encode("big5") for s in list]
        index, matched, text = self._tn.expect(encoded, self._timeout)
        return index

    def login(self):
        print "start to login as %s....." % str(self._account)
        self._tn = telnetlib.Telnet(self._host)
        if self.expect([u"請輸入代號："]) == -1:
            raise KeyError("cannot enter account")
        self._tn.write(self._account + '\r\n')
        print "enter account."

        if self.expect([u"請輸入密碼："]) == -1:
            raise KeyError("cannot enter account")
        self._tn.write(self._password + '\r\n')
        print "enter password."

        if self.expect([u"您想刪除其他重複的 login"]) != -1:
            print "delete duplicated login."
            self._tn.write('y\r\n')

        # skip login info, hot topics, message bord
        self._tn.write(self._password + '\r\n' * 3)
        print "login successfully."

    def enter_board(self, board):
        self._tn.write('b\r\n')         # enter board list
        self._tn.write('s')             # search
        self._tn.write(board + '\r\n')  # enter board name
        if self.expect([u"錯誤的看板名稱"]) != -1:
            raise KeyError("no board named " + board)

        # try to skip board opening picture
        while True:
            if self.expect([u"看板《" + board + u"》"]) == -1:
                print "press enter to skip board opening page."
                self._tn.write('\r\n')
            else:
                break
        print "now you are in board: " + board

    def download_board(self, board, start, end):
        self.enter_board(board)

        download_folder = "download_" + str(board)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for i in range(int(start), int(end)+1):
            with open(os.path.join(download_folder, str(i) + ".txt"), "w") as file:
                print "start downloading article " + str(i)
                self.read()                        # read article list to clean screen
                self._tn.write(str(i) + '\r\n'*2)  # directly input number to find article
                content = self._formatter.normalize(self.read_article())
                title = str(i) + self._formatter.escape_article_title(self._formatter.parse_article_title(content))
                file.write(content)
                self._tn.write('q')

            self._rename_article(download_folder, str(i)+".txt", title+".txt")

    def _rename_article(self, download_folder, old_title, new_title):
        try:
            if os.path.exists(os.path.join(download_folder, new_title)):
                os.remove(os.path.join(download_folder, new_title))

            os.rename(os.path.join(download_folder, old_title),
                      os.path.join(download_folder, new_title))
        except OSError as e:
            print "cannot rename file as %s" % new_title, e

    def read(self):
        time.sleep(1)
        data = ""
        while True:
            read_data = self._tn.read_eager()
            data += read_data
            if not read_data:
                break
        return data

    def read_article(self):
        data = ""
        # find the end of an article
        counter = 0
        while counter < 40:
            data += self.read()
            if data.find("(=\[]<>-+;'`jk)") >= 0:
                break
            data += '<<hulabear_page_splitter>>'
            self._tn.write('\r\n')
            counter += 1
        else:
            data = "you don't have permission to read this article. Possibly a F- or L-article."
            print data

        return data
