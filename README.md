# naver-webtoon
Automatically exported from code.google.com/p/naver-webtoon

* Install Python 2.7.15
  * https://www.python.org/downloads/release/python-2715/
  * https://www.python.org/ftp/python/2.7.15/python-2.7.15.msi

* Install moudles
    python -m pip install pip --upgrade
    python -m pip install pillow
    python -m pip install requests
    python -m pip install py2exe_py2

* Copy cacert.pem bundle file. (for requests library)
  * copy to .\downloader\dist\
  * I found cacert.pem file from 'C:\Python27\Lib\site-packages\certifi'.


* Run make.bat
  * This is the same 'Run C:\Python27\python.exe setup.py py2exe C:\Python27\python.exe setup2.py py2exe'

* You can get the download.exe and merge_image.exe in ./dist folder.
