#!/usr/bin/python
# -*- encoding: UTF-8 -*-

# convert html to lyrics from http://utaten.com

import urllib2
# import numpy as np
# import re
# import time, json
import sys
import difflib
from bs4 import BeautifulSoup
import StringIO, gzip

useragent = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36",
    "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
    'Mozilla/5.0']
header = {'User-Agent':useragent[0],
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close',
    'Referer':'http://javtorrent.xyz/censored/111101/'}
timeout = 5

def urlopen(url):
    request = urllib2.Request(url,None,header)
    response = urllib2.urlopen(request,None,timeout)
    # if response.headers['content-encoding'] in ('gzip', 'x-gzip'):
    data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(response.read()))
    # elif response.headers['content-encoding'] == 'deflate':
    #     data = StringIO.StringIO(zlib.decompress(content))
    response.close()
    return data

def visitpage(href):
    # msp_href = 'http://javtorrent.xyz/date/2015/09/'
    try:
        page = urlopen(href)
    except urllib2.HTTPError, e:
        return
    else:
        soup = BeautifulSoup(page, 'html.parser')
        m = soup.findChild(class_="lyricBody").findChild("div",class_="medium").findChild("div",class_="hiragana")
        return m.encode_contents()

prefix = r"""% !TeX encoding = UTF-8
% !TeX program = LuaLaTeX

%\documentclass[12pt]{article}
\documentclass[14pt]{ltjsarticle}
\input{Nihongo-lyrics-luamacros.tex}
\begin{document}

\lyrics{
\item
  \textbf{\ldots \hfill %
    「\ldots」のOP/ED/\zhuyin{挿}{そう}\zhuyin{入}{にゅう}\zhuyin{歌}{か}/\zhuyin{主}{しゅ}\zhuyin{題}{だい}\zhuyin{歌}{か}}

\item
  """
suffix = r"""
}
\end{document}
"""

def tolatex(m):
    return prefix + \
        m.replace(r'</span></span>',"}")\
        .replace(r'</span><span class="rt">',"}{") \
        .replace(r'</span>',"}") \
        .replace(r'<span class="ruby"><span class="rb">',"\z{") \
        .replace('%', r'\%') \
        .replace(r'&amp;', r'\&') \
        .replace('\n', "") \
        .replace('<br/><br/>',"\n  \\jisho{}\n\n\\item\n  ") \
        .replace(r'<br/>',"\n  \\jisho{}\n\n  ") \
        + suffix

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "{} URL".format(sys.argv[0])
        print "{} diff URL URL".format(sys.argv[0])
    elif sys.argv[1] == "diff":
        m1, m2 = (m.replace(r'</span></span>',"}")
            .replace(r'</span><span class="rt">',"{")
            .replace(r'</span>',"")
            .replace(r'<span class="ruby"><span class="rb">',"")
            .replace(r'<br/>',"\n")
            for m in (visitpage(sys.argv[2]), visitpage(sys.argv[3])))
        for line in difflib.context_diff(m1.decode('utf-8'), m2.decode('utf-8')):
            print line
    else:
        print tolatex(visitpage(sys.argv[1]))
