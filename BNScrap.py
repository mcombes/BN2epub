import urllib.request as urlRequest
import urllib.parse as urlParse
import sys
import codecs as cs
import os
import shutil
import subprocess

try:
    shutil.rmtree("OEBPS")
except:
    if os.path.isdir("OEBPS"):
        raise
def MakeAChapter(page):
	if page.count('<div class="cha-words">')>0 and (page.split('<div class="cha-words">')[-1].split('<div class="c-select-bottom">')[0]).count("</p>")>0:
		return ("</p>".join(page.split('<div class="cha-words">')[-1].split('<div class="c-select-bottom">')[0].split('</p>')[:-1])+"</p>")
	if page.count('<div class="cha-words">')>0:
		if len(page.split('<div class="cha-words">')[-1].split('<div class="c-select-bottom">')[0].split("</div>")[:-1])>1:
			return "".join(page.split('<div class="cha-words">')[-1].split('<div class="c-select-bottom">')[0].split("</div>")[:-1])
		else:
			return page.split('<div class="cha-words">')[-1].split('<div class="c-select-bottom">')[0].split("</div>")[:-1]
	elif(page.count('Editor:')>0):
		return "\n".join(("</p>".join(page.split('Editor:')[-1].split('<div class="c-select-bottom">')[0].split('</p>')[:-1])+"</p>").splitlines()[1:])
	else:
		return "</p>".join(page.split('<div class="text-left">')[-1].split('<div class="c-select-bottom">')[0].split('</p>')[:-1])+"</p>"
def MakeAWebpage(pathname, meme=True, default=""):
    chapterName = pathname.split("/")[-1]
    bookName = pathname.split("/")[-2]
    file_name = chapterName+'.html'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    req = urlRequest.Request(pathname, headers = headers)
    x = urlRequest.urlopen(req)
    sourceCode = x.read()
    try:
        os.makedirs("OEBPS")
    except OSError:
        if not os.path.isdir("OEBPS"):
            raise
    if(meme):
        html = cs.open("OEBPS/"+file_name,'w','utf-8')
        decoded=sourceCode.decode("utf-8") 
        html.write(MakeAChapter(decoded))
        html.close()
    else:
        html = cs.open("OEBPS/"+default,'w','utf-8')
        decoded=sourceCode.decode("utf-8") 
        html.write(decoded)
        html.close()

def GatherCompleteSummaryPages():
    MakeAWebpage("https://boxnovel.com/novel/" + sys.argv[1]+'/',False,"index.html")
    memeFile=open("OEBPS/index.html","r",encoding="utf-8")
    wholeIndex=memeFile.read()
    memeFile.close()
    ListeLiens=[]
    mymeme = wholeIndex.split('<ul class="main version-chap">')[1].split('</ul>')[0]
    xd=mymeme.splitlines()
    for line in xd:
        if line.count("a href")!=0:
            ListeLiens.append(line.split('"')[1])
    return(ListeLiens)
	
def WriteSummary(listeLiens, outPath="OEBPS/toc.html"):
    html_doc = """<body>
    <h1>Table of Contents</h1>
    <p style="text-indent:0pt">
"""
    for lien in listeLiens:
        MakeAWebpage(lien)
        chapterName = (lien).split("/")[-1]
        html_doc = html_doc + "      <a href=" + "\"" + chapterName + ".html\">" + chapterName + "</a><br/>" + "\r\n"
    html_doc += """    </p>
  </body>
</html>
    """
    tocHTML = cs.open(outPath, 'w', 'utf-8')
    tocHTML.write(html_doc)
    tocHTML.close()
maListe=GatherCompleteSummaryPages()
maListe.reverse()
WriteSummary(maListe)
os.remove("OEBPS/index.html")
#exec(open("epubTest.py").read())
subprocess.run(["python", 'epubMaker.py', sys.argv[1]])