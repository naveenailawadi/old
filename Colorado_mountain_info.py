from bs4 import BeautifulSoup as bs
import requests


def a_basin_snow():
    website = 'https://opensnow.com/location/arapahoebasin'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "report-data"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('A Basin new snow: ')
    for s in snow:
        print(s.text)
    for s in no_snow:
        print(s.text)
    for s in high_snow:
        print(s.text)
    return


def vail_snow():
    website = 'https://opensnow.com/location/vail'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "report-data"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Vail new snow:')
    for s in snow:
        print(s.text)
    for s in no_snow:
        print(s.text)
    for s in high_snow:
        print(s.text)
    return


def breck_snow():
    website = 'https://opensnow.com/location/breckenridge'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "report-data"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Breckenridge new snow:')
    for s in snow:
        print(s.text)
    for s in no_snow:
        print(s.text)
    for s in high_snow:
        print(s.text)
    return


def keystone_snow():
    website = 'https://opensnow.com/location/keystone'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "report-data"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Keystone new snow:')
    for s in snow:
        print(s.text)
    for s in no_snow:
        print(s.text)
    for s in high_snow:
        print(s.text)
    return


def beaver_creek_snow():
    website = 'https://opensnow.com/location/beavercreek'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "report-data"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Beaver Creek new snow:')
    for s in snow:
        print(s.text)
    for s in no_snow:
        print(s.text)
    for s in high_snow:
        print(s.text)
    return


def snow_report():
    breck_snow()
    a_basin_snow()
    keystone_snow()
    vail_snow()
    beaver_creek_snow()
    return


def a_basin_weather():
    website = 'https://opensnow.com/location/arapahoebasin'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    high = site_soup.find("div", class_="high")
    print('A-Basin high:')
    print(high.text)
    low = site_soup.find("div", class_="low")
    print('A-Basin low:')
    print(low.text)
    return


def vail_weather():
    website = 'https://opensnow.com/location/vail'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    high = site_soup.find("div", class_="high")
    print('Vail high:')
    print(high.text)
    low = site_soup.find("div", class_="low")
    print('Vail low:')
    print(low.text)
    return


def breck_weather():
    website = 'https://opensnow.com/location/breckenridge'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    high = site_soup.find("div", class_="high")
    print('Breckenridge high:')
    print(high.text)
    low = site_soup.find("div", class_="low")
    print('Breckenridge low:')
    print(low.text)
    return


def keystone_weather():
    website = 'https://opensnow.com/location/keystone'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    high = site_soup.find("div", class_="high")
    print('Keystone high:')
    print(high.text)
    low = site_soup.find("div", class_="low")
    print('Keystone low:')
    print(low.text)
    return


def beaver_creek_weather():
    website = 'https://opensnow.com/location/beavercreek'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    high = site_soup.find("div", class_="high")
    print('Beaver Creek high:')
    print(high.text)
    low = site_soup.find("div", class_="low")
    print('Beaver Creek low:')
    print(low.text)
    return


def weather_report():
    breck_weather()
    a_basin_weather()
    keystone_weather()
    vail_weather()
    beaver_creek_weather()
    return

# forecast-block


def a_basin_forecast():
    website = 'https://opensnow.com/location/arapahoebasin'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "forecast-block"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('A-Basin snow prediction:')
    for s in snow:
        print(s.text)
        break
    for s in no_snow:
        print(s.text)
        break
    for s in high_snow:
        print(s.text)
        break
    return


def vail_forecast():
    website = 'https://opensnow.com/location/vail'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "forecast-block"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Vail snow prediction:')
    for s in snow:
        print(s.text)
        break
    for s in no_snow:
        print(s.text)
        break
    for s in high_snow:
        print(s.text)
        break
    return


def breck_forecast():
    website = 'https://opensnow.com/location/breckenridge'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "forecast-block"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Breckenridge snow prediction:')
    for s in snow:
        print(s.text)
        break
    for s in no_snow:
        print(s.text)
        break
    for s in high_snow:
        print(s.text)
        break
    return


def keystone_forecast():
    website = 'https://opensnow.com/location/keystone'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "forecast-block"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Keystone snow prediction:')
    for s in snow:
        print(s.text)
        break
    for s in no_snow:
        print(s.text)
        break
    for s in high_snow:
        print(s.text)
        break
    return


def beaver_creek_forecast():
    website = 'https://opensnow.com/location/beavercreek'
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    report_data = site_soup.find("div", {"id": "forecast-block"})
    snow = report_data.find_all('div', {'class': 'data-cell snow'})
    no_snow = report_data.find_all('div', {'class': 'data-cell nosnow'})
    high_snow = report_data.find_all('div', {'class': 'data-cell highsnow'})
    print('Beaver Creek snow prediction:')
    for s in snow:
        print(s.text)
        break
    for s in no_snow:
        print(s.text)
        break
    for s in high_snow:
        print(s.text)
        break
    return


def snow_forecast():
    breck_forecast()
    a_basin_forecast()
    keystone_forecast()
    vail_forecast()
    beaver_creek_forecast()


while True:
    answer = str(input('If you want to know the snow report: type "snow".\n\
If you want to know the weather: type "weather".\n\
IF you want the snow forecast for tomorrow: type "forecast".\n'))
    if 'snow' in answer.lower():
        snow_report()
    if 'weather' in answer.lower():
        weather_report()
    if 'forecast' in answer.lower():
        snow_forecast()
