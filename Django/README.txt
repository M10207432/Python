Django Installation Process:
1) Download Python & PIP
2) Install PIP ("python get-pip.py")
3) Setup Environment variables in Windows System Settings under Advanced Settings:
C:\Python27;C:\Python27\python.exe;C:\Py-thon27\Scripts\; C:\Python27\Lib\site-packages\django\bin-;
4) Install Virtual environment "pip install virtualenv"
5) Create virtualenv and activate:
virtualenv somename
cd somename
.\Scripts\activate
6) Install Django:
pip install django==1.X.Y (replace x and y for version numbers)
7) Start django project:
python .\Scripts\django-admin.py startproject yourprojectname