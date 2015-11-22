#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*- 

import urllib2
import chardet
import BeautifulSoup
import sqlite3
import os
import urllib
import threading
import time
import glob
 
def downloadImage():
  max_threads = 2

  class downloadThread(threading.Thread):
    def __init__(self, cid):
      self.cid = cid
      self.url = "http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=%s/" % cid
      threading.Thread.__init__(self)

    def run(self):
      self.directory = "./img/%s" % cid
      self.directory_temp = "./img/tmp_%s" % cid
     
      os.mkdir(self.directory_temp)

      # get image filename
      self.lines = urllib2.urlopen(self.url).read()
      self.lines = unicode(self.lines, chardet.detect(self.lines)['encoding'], 'ignore')
       
      # no sample
      if u"拡大表示されません" in self.lines:
        print "no image", self.url
        os.rename(self.directory_temp, self.directory)
        return
        
      self.soup = BeautifulSoup.BeautifulSoup(self.lines)

      self.s4 = self.soup(attrs={'id': 'sample-image-block'})
      if len(self.s4) != 0:
        self.s2 = self.s4[0]
        for self.s3 in self.s2('img'):
          self.img_url = self.s3['src'].replace('-', 'jp-')
          self.filename = self.img_url[self.img_url.rindex("/")+1:]
          print self.img_url
           
          self.opened_url = urllib2.urlopen(self.img_url)
          if self.opened_url.url != self.img_url:
            print "connect error"
            return
       
          urllib.urlretrieve( self.img_url, "%s/%s" % (self.directory_temp, self.filename))

      os.rename(self.directory_temp, self.directory)

  print "remove temp directories"
  for directory in glob.glob('./img/tmp_*'):
    shutil.rmtree(directory)

  print "open database"
  con = sqlite3.connect(db_name["cid"])

  cur = con.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='filename';")
  if cur.fetchone() == None:
    ct_sql = "create table filename (cid, number, filename);"
    con.execute(ct_sql)
    con.commit()

  cur = con.execute("SELECT * FROM cid;")

  try:
    for row in cur.fetchall():
      cid = row[0]
      directory = "./img/%s" % cid
      directory_temp = "./img/tmp_%s" % cid

      # check exists
      if os.path.exists(directory):
        continue
      if os.path.exists(directory_temp):
        continue
      
      while True:
        if threading.activeCount() <= max_threads:
          t = downloadThread(cid)
          t.setDaemon = True
          t.start()
          time.sleep(0.2)
          break
        time.sleep(1)
  finally:
    con.close()