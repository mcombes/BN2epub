import urllib.request as urlRequest
import urllib.parse as urlParse
import sys
import codecs as cs
import os
import shutil
import subprocess

def MakeAWebpage(pathname, meme=True, default=""):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    req = urlRequest.Request(pathname, headers = headers)
    x = urlRequest.urlopen(req)
    sourceCode = x.read()
    try:
        os.makedirs("tempIndex")
    except OSError:
        if not os.path.isdir("tempIndex"):
            raise
    if(meme):
        html = cs.open("tempIndex/"+"mainIndex1.html",'w','utf-8')
        decoded=sourceCode.decode("utf-8") 
        html.write(decoded)
        html.close()
    else:
        html = cs.open("tempIndex/"+default,'w','utf-8')
        decoded=sourceCode.decode("utf-8")
        decoded="<h4>".join(decoded.split("<h4>")[2:])
        html.write(decoded)
        html.close()
MakeAWebpage("https://boxnovel.com/?s&post_type=wp-manga&m_orderby=rating")
myFile=open("tempIndex/mainIndex1.html","r",encoding="utf-8")
myText=myFile.read()
myFile.close()
myNumber=myText.split(" results")[0].split("</i> ")[-1]
myMaxIndex=int(myNumber)/10
myListOfLinks=[]
for oneSplit in myText.split("<h4>")[2:]:
    myListOfLinks.append(oneSplit.split('href="')[1].split('"')[0].split("/")[-2])
i=2
while (i<=myMaxIndex):
	MakeAWebpage("https://boxnovel.com/page/"+str(i)+"/?s&post_type=wp-manga&m_orderby=rating",False,"mainIndex"+str(i)+".html")
	myFile=open("tempIndex/mainIndex"+str(i)+".html","r",encoding="utf-8")
	myText=myFile.read()
	myFile.close()
	for oneSplit in myText.split("<h4>"):
		myListOfLinks.append(oneSplit.split('href="')[1].split('"')[0].split("/")[-2])
	i+=1
try:
    shutil.rmtree("tempIndex")
except:
    if os.path.isdir("tempIndex"):
        raise
print(myListOfLinks[:10])
for currentItem in myListOfLinks:
	subprocess.run(["python", 'BNScrap.py', currentItem])
#print(myMaxIndex)