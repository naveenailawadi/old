import os

try:
    import bs4
except ImportError:
    os.system('python3 -m pip install bs4')

try:
    import requests
except ImportError:
    os.system('python3 -m pip install requests')

try:
    import statistics
except ImportError:
    os.system('python3 -m pip install statistics')

try:
    import pandas
except ImportError:
    os.system('python3 -m pip install pandas')

try:
    import datetime
except ImportError:
    os.system('python3 -m pip install datetime')

# print if all installed
import bs4
import requests
import statistics
import pandas
import datetime
print('Everything has been installed! You can run comps_to_xl.py now!')
