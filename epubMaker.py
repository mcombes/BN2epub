import zipfile
import os
import sys
import shutil
opening= """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	
        <dc:title>myBook</dc:title>
		
        <dc:language>en</dc:language>
		
        <dc:identifier id="uuid_id" opf:scheme="uuid">isbn-000-0-000-00000-0</dc:identifier>
        <dc:creator>Your Author Name Here</dc:creator>
        <dc:publisher>Your Publisher Name Here</dc:publisher>
        <dc:date>2013-08-17</dc:date>
		
        <meta name="cover" content="my-cover-image"/>

    </metadata>
    <manifest>
"""
ending1="""        <item href="toc.html" id="toc" media-type="application/xhtml+xml"/>
        <item href="toc.ncx" id="tableofcontents" media-type=application/x-dtbncx+xml"/>
    </manifest>
    <spine toc="tableofcontents">
        <itemref idref="toc"/>
"""
ending2="""    </spine>
    <guide>
        <reference href="toc.html" title="Table Of Contents" type="toc"/>
    </guide>
</package>"""
added_to_TOCHeader="""<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Unknown</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  </head>
  """
myTOCFile=open("OEBPS/toc.html","r",encoding="utf-8")
TOCTemp=myTOCFile.read()

myTOCFile.close()
myTemp=[]
for line in TOCTemp.splitlines():
	if line.count("<a href=")>0:
		myTemp.append(line.split('a href="')[1].split('"')[0])
TOCTemp=added_to_TOCHeader+TOCTemp
myTOCModif=open("OEBPS/toc.html","w",encoding="utf-8")
myTOCModif.write(TOCTemp)
myTOCModif.close()
#ToC is edited
tocncx="""<?xml version="1.0" encoding="UTF-8" standalone="no" ?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
	<head>
		<meta content="isbn-000-0-000-00000-0" name="dtb:uid"/>
		<meta content="2" name="dtb:depth"/>
		<meta content="0" name="dtb:totalPageCount"/>
		<meta content="0" name="dtb:maxPageNumber"/>
	</head>
	<docTitle>
		<text>Your Book Title Goes in Here</text>
	</docTitle>
	<navMap>
		<navPoint class="chapter" id="toc" playOrder="1">
			<navLabel>
				<text>Table of Contents</text>
			</navLabel>
			<content src="OEBPS/toc.html"/>
		</navPoint>"""
middleMan=[]
playOrder=2
for item in myTemp:
	middleMan.append('        <item id="'+item.split('.')[0]+'" href="'+item+'" media-type="application/xhtml+xml"/>')
	ending1+='        <itemref idref="'+item.split('.')[0]+'"/>'+"\n"
	tocncx+='''
		<navPoint class="chapter" id="'''+item.split('.')[0]+'''" playOrder="'''+str(playOrder)+'''">
			<navLabel>
				<text>It's a chapter</text>
			</navLabel>
			<content src="OEBPS/'''+item+'''"/>
		</navPoint>'''
	playOrder+=1
tocncx+="""
	</navMap>
</ncx>"""
ending=ending1+ending2
wholeContentOPF=opening+"\n".join(middleMan)+"\n"+ending
myNCXFile=open("OEBPS/toc.ncx","w",encoding="utf-8")
myNCXFile.write(tocncx)
myNCXFile.close()
myOPFFile=open("OEBPS/content.opf","w",encoding="utf-8")
myOPFFile.write(wholeContentOPF)
myOPFFile.close()
myMimeType=open("mimetype","w")
myMimeType.write("application/epub+zip")
myMimeType.close()
try:
    os.makedirs("META-INF")
except OSError:
    if not os.path.isdir("META-INF"):
        raise
myContainer="""<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
      
   </rootfiles>
</container>"""
myContainerXML=open("META-INF/container.xml","w",encoding="utf-8")
myContainerXML.write(myContainer)
myContainerXML.close()

zout = zipfile.ZipFile(sys.argv[1]+".zip", "w")
OEBPSpath=os.listdir("./OEBPS")
zout.write("./mimetype")
zout.write("./META-INF")
zout.write("./META-INF/container.xml")
zout.write("./OEBPS")
for fname in OEBPSpath:
    #print("writing: ", fname)
    zout.write("./OEBPS/"+fname)
zout.close()
os.rename(sys.argv[1]+".zip",sys.argv[1]+".epub")
shutil.rmtree("OEBPS")
shutil.rmtree("META-INF")
os.remove("mimetype")