# naver-webtoon
Automatically exported from code.google.com/p/naver-webtoon

1. Install Python 2.7.5
	- http://www.python.org/download/

2. Install py2exe (for 2.7) 
	- http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/

3. Install PIL 1.1.7 (Python Imaging Library 1.1.7 for Python 2.7) 
	- http://www.pythonware.com/products/pil/

3-1. Copy cacert.pem bundle file. (for requests library)
	- copy to .\downloader\dist\
	- I found cacert.pem file from 'C:\Python27\Lib\site-packages\certifi'.


4. Run make.bat
	- This is the same 'Run C:\Python27\python.exe setup.py py2exe C:\Python27\python.exe setup2.py py2exe'

5. You can get the download.exe and merge_image.exe in dist folder.
