# BN2epub
 A web scraper and epub maker all-in-one
I made a pretty massive breakthrough while making this one, I might go back and update the other ones accordingly!


Uses: python BNScrap.py [novelReference]
(without the brackets)


A novel reference is the last item between slashes in your browser bar when you're on a given novel's summary page.
The script will output a valid .epub file.

TODO:

Maybe try to fiddle with compression rates so that apart from the first file that I absolutely must never compress, the text gets compressed.
Dependencies: Python 3, a few libraries listed down below, an internet connexion.

urllib
sys
codecs as cs
os
shutil
subprocess
zipfile