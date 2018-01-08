# -*- coding: utf8 -*-
import os
import time
from article import Article


class Board():
    def __init__(self, name, tn):
        self.name = name
        self._tn = tn

    def enter(self):
        self._tn.write('s')  # search
        self._tn.write(self.name + '\r\n')  # enter board name
        if self._tn.expect_list([u"錯誤的看板名稱"]) != -1:
            raise KeyError("no board named " + self.name)
        self._skip_opening_page()
        print "now you are in board: " + self.name

    def _skip_opening_page(self):
        retry_cnt = 0
        while self._tn.expect_list([u"看板《" + self.name + u"》"]) == -1:
            print "trying to skip board opening page...."
            self._tn.write('\r\n')
            retry_cnt += 1
            if retry_cnt > 10:
                raise KeyError("cannot enter the board. possible reasons: " +
                               "1) the board have more than 10 opening pages, or " +
                               "2) the board name you entered doesn't match (case-sensitive).")

    def download(self, folder, start, end):
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i in range(int(start), int(end) + 1):
            with open(os.path.join(folder, str(i) + ".txt"), "w") as file:
                print "start downloading article " + str(i)
                self._read()  # read article list to clean screen
                self._tn.write(str(i) + '\r\n' * 2)  # directly input number to find article
                article = Article(i, self._read_article())
                article.build()
                file.write(article.content)
                self._tn.write('q')
            self._rename_article(folder, str(i) + ".txt", article.title + ".txt")

    def _read(self):
        time.sleep(1)
        data = ""
        while True:
            read_data = self._tn.read_eager()
            data += read_data
            if not read_data:
                break
        return data

    def _read_article(self):
        data = ""
        # find the end of an article
        counter = 0
        while counter < 40:
            data += self._read()
            if data.find("(=\[]<>-+;'`jk)") >= 0:
                break
            data += '<<hulabear_page_splitter>>'
            self._tn.write('\r\n')
            counter += 1
        else:
            data = "you don't have permission to read this article. Possibly a F- or L-article."
            print data

        return data

    def _rename_article(self, download_folder, old_title, new_title):
        try:
            if os.path.exists(os.path.join(download_folder, new_title)):
                os.remove(os.path.join(download_folder, new_title))

            os.rename(os.path.join(download_folder, old_title),
                      os.path.join(download_folder, new_title))
        except OSError as e:
            print "cannot rename file as %s" % new_title, e
