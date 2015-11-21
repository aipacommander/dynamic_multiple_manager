#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 

import urllib2
import chardet
import BeautifulSoup
import sqlite3
import os
import Image
import pickle
import cStringIO
import sys
import urllib
import shutil
import threading
import time
import glob
import cv2
import numpy as n
import math
 
base_url = 'http://www.dmm.co.jp'
db_name  = 'dmm'

def getCID():
  class MakerThread(threading.Thread):
    def __init__(self, url):
      self.url = url
      threading.Thread.__init__(self)

    def run(self):
      # print self.url
      self.cids = []
      for self.i in range(1,1000):
        self.open_url = "%slimit=120/page=%d/" % (self.url, self.i)
        self.opened_url = urllib2.urlopen(self.open_url)
        # print self.open_url
        # print self.opened_url.url
        # 取得したら同じurlのはず。
        # 違う場合は恐らく404かトップページ
        if self.opened_url.url != self.open_url:
            break
        self.lines = self.opened_url.read()
        self.lines = unicode(self.lines, chardet.detect(self.lines)['encoding'])
        self.soup = BeautifulSoup.BeautifulSoup(self.lines)
        for self.s in self.soup(attrs={'class': 'tmb'}):
          self.vurl = "%s%s" % (base_url, self.s('a')[0]['href'])
          self.pos1 = self.vurl.index("cid=") + 4
          self.pos2 = self.vurl.index("/", self.pos1)
          self.cids.append((self.vurl[self.pos1:self.pos2],))
      while True:
        try:
          self.con = sqlite3.connect(db_name)
          self.con.executemany('insert into cid values (?)', self.cids)
          self.con.commit()
          self.con.close()
          break
        except:
          time.sleep(10)
      print 'done'

  class CharThread(threading.Thread):
    def __init__(self, consonant, vowel):
      self.url = "http://www.dmm.co.jp/digital/videoa/-/maker/=/keyword=%s%s/" % (consonant, vowel) # プライベート変数（？）をセット
      threading.Thread.__init__(self) # これはまだよくわからん

    def run(self):
      max_threads = 100 # スレッド上限数をセット
      self.lines = urllib2.urlopen(self.url).read() # ここからwebへ接続しリソースを取得
      self.lines = unicode(self.lines, chardet.detect(self.lines)['encoding']) # utf8へ変換。かな？
      self.soup = BeautifulSoup.BeautifulSoup(self.lines) # 確かBeautifulSoupはパーサーのライブラリだはず
      self.r = self.soup(attrs={'class': 'd-boxpicdata d-smalltmb'}) # 取得したい箇所だけ
      self.maker = []
      for self.r1 in self.r: # 複数あるのでループしてリンクを取得
        while True:
          time.sleep(10)
          # ここがいまいちわからない。上限をこえたらループから抜けさすの？あ。そのとおりだね。
          if threading.activeCount() <= max_threads:
              break
        self.t = MakerThread("%s%s" % (base_url, self.r1('a')[0]['href'])) # リンクからidを取得するメソッドへurlを渡す
        self.t.setDaemon = True
        self.t.start()
   
  # db処理
  con = sqlite3.connect(db_name) # sqliteへ接続する
  cur = con.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='cid';") # cid tableを確認
  if cur.fetchone() != None: # 存在する場合
    con.execute("drop table cid;") # 削除する
  con.execute("create table cid (cid);") # どちらにせよ実行時に新規作成
  con.commit() # sql実行
  con.close()  # connection close

  # 子音母音を合わせて検索する
  for consonant in ['', 'k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w']:
    for vowel in ['a', 'i', 'u', 'e', 'o']:
      t = CharThread(consonant, vowel) # スレッドを生成するメソッドを呼び出し
      t.setDaemon = True # これはよくわからん
      t.start() # スレッドスタート
      time.sleep(1) # 1秒ずつ遅らせる

if __name__ == '__main__':
  getCID()