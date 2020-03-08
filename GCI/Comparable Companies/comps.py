from bs4 import BeautifulSoup as bs
import requests


# create a class with all the company's information
'''
INFORMATION to scrape for
- name
- market cap
- price per share
- EV/(Revenue TTM)
- EV/(EBIT TTM)
- EV/(EBITDA TTM)
- EV/(FCF TTM)
- beta
- debt/equity
'''


class Company:
    def __init__(self, ticker):
        self.ticker = str(ticker).upper()
        self.get_links()
        self.scrape_general()
        # primary data not initially called to save computing power

    # get the links that will be used for information
    def get_links(self):
        self.stat_link = f'https://www.gurufocus.com/stock/{self.ticker}/summary'
        self.guru_links = [
            f'https://www.gurufocus.com/term/Preferred+Stock/{self.ticker}/Preferred-Stock',
            f'https://www.gurufocus.com/term/Minority_interest/{self.ticker}/Minority-Interest',
            f'https://www.gurufocus.com/term/LongTermDebt/{self.ticker}/Long-Term-Debt',
            f'https://www.gurufocus.com/term/ShortTermDebt_without_lease/{self.ticker}/Short-Term-Debt',
            f'https://www.gurufocus.com/term/CashAndCashEquivalents/{self.ticker}/Cash-And-Cash-Equivalents',
            f'https://www.gurufocus.com/term/BS_share/{self.ticker}/Shares-Outstanding-(EOP)',
            f'https://www.gurufocus.com/term/Revenue/{self.ticker}/Revenue',
            f'https://www.gurufocus.com/term/total_freecashflow/{self.ticker}/Free-Cash-Flow',
            f'https://www.gurufocus.com/term/EBITDA/{self.ticker}/EBITDA',
            f'https://www.gurufocus.com/term/EBIT/{self.ticker}/EBIT',
            f'https://www.gurufocus.com/term/Net+Income/{self.ticker}/Net-Income'
        ]

    # scrape the general information
    def scrape_general(self):
        raw = requests.get(self.stat_link).text
        soup = bs(raw, 'html.parser')

        # get general info
        gen_info = soup.find('h1').text.split('$')
        self.name = gen_info[0]

        # all tables of information
        try:
            gen_table = soup.find("div", {"class": "stock-summary-table fc-regular"}).find_all('div')
        except AttributeError:
            gen_table = soup.find_all("div", {"data-v-cd388136]": ""})

        tables = soup.find_all('tbody')

        # get market cap
        self.market_cap = find_ratio_simple(gen_table, 'market cap')

        # get EV
        self.enterprise_value = find_ratio_simple(gen_table, 'enterprise value')

        # get price per share
        self.price_per_share = float(gen_info[1].split('\n')[1])

        # get the general info
        self.get_primary_data()

        # get EV/(Revenue TTM)
        self.ev_to_revenue = self.enterprise_value / self.revenue

        # get EV/(EBITDA TTM)
        self.ev_to_ebitda = self.enterprise_value / self.ebitda

        # get EV/(EBIT TTM)
        self.ev_to_ebit = self.enterprise_value / self.ebit

        # get EV/(FCF TTM)
        self.ev_to_fcf = self.enterprise_value / self.fcf

        # get p/e
        self.price_to_earnings = find_ratio_simple(gen_table, 'p/e')

        # get eps
        self.eps = self.net_income / self.shares_outstanding

        # get D/E
        self.debt_to_equity = find_ratio(tables[1].find_all('tr'), 'td', 'Debt-to-Equity')

        # get beta
        self.beta = self.find_beta()

    # get data off of guru focus
    def get_guru_data(self, guru_link):
        raw = requests.get(guru_link).text
        soup = bs(raw, 'html.parser')
        font_info = {"style": "font-size: 24px; font-weight: 700; color: #337ab7"}
        tag = soup.find('font', font_info).text

        # clean up the tag text
        try:
            ends = tag.split('$')[1].split(' ')
        except IndexError:
            ends_list = tag.split(' ')
            ends = ends_list[1] + ends_list[2]
        value = ends[0]  # preferred stock value
        multiplier = ends[1][:1]
        value += multiplier
        guru_data = string_to_num(value)
        return guru_data

        # get shares outstanding
    def get_guru_shares_outstanding(self, guru_link):
        raw = requests.get(guru_link).text
        soup = bs(raw, 'html.parser')
        font_info = {"style": "font-size: 24px; font-weight: 700; color: #337ab7"}
        tag = soup.find('font', font_info).text

        # clean up the tag text
        ends = tag.split(' ')
        value = ends[1].replace(',', '')  # preferred stock value
        multiplier = ends[2][:1]
        value += multiplier
        guru_data = string_to_num(value)
        return guru_data

    def get_primary_data(self):
        self.preferred_stock = self.get_guru_data(self.guru_links[0])
        self.minority_interest = self.get_guru_data(self.guru_links[1])

        long_term_debt = self.get_guru_data(self.guru_links[2])
        short_term_debt = self.get_guru_data(self.guru_links[3])
        self.total_debt = long_term_debt + short_term_debt

        self.cash_and_cash_equivalents = self.get_guru_data(self.guru_links[4])
        self.shares_outstanding = self.get_guru_shares_outstanding(self.guru_links[5])

        # get some metrics about the primary from the summary link
        self.revenue = self.get_guru_data(self.guru_links[6])
        self.fcf = self.get_guru_data(self.guru_links[7])  # --> can use for price to fcf
        self.ebitda = self.get_guru_data(self.guru_links[8])
        self.ebit = self.get_guru_data(self.guru_links[9])
        self.net_income = self.get_guru_data(self.guru_links[10])

    def find_beta(self):
        # load link
        link = f"https://finance.yahoo.com/quote/{self.ticker}/key-statistics?p={self.ticker}"
        raw = requests.get(link).text
        soup = bs(raw, 'html.parser')

        # get table
        table = soup.find_all('tbody')[1].find_all('tr')

        # get ratio
        beta = find_ratio(table, 'td', 'Beta')

        return beta


# convert strings with letters denoting thousands, millions, or billions into regular floats
def string_to_num(num_string):

    # handle nonetype
    if 'none' in str(type(num_string)):
        print('no value found to convert')
        return('-')

    # make it easier to scan
    num_string = num_string.lower().replace(',', '')
    num_string = num_string.replace(' ', '')

    # convert to correct value
    if 't' in num_string:
        num = float(num_string.split('t')[0])
        num *= 1000000000000.0
    elif 'b' in num_string:
        num = float(num_string.split('b')[0])
        num *= 1000000000.0

    elif 'm' in num_string:
        num = float(num_string.split('m')[0])
        num *= 1000000.0

    elif ('k' in num_string):
        num = float(num_string.split('k')[0])
        num *= 1000.0
    else:
        try:
            num = float(num_string)
        except ValueError:
            num = "-"

    return num

# create a function to turn values into accounting format


def af(num):
    if 'float' in str(type(num)):
        num = str(round(num, 2))
    elif 'str' in str(type(num)):
        num = str(round(float(num), 2))
    accounting_formatted_number = f"${num}"
    return accounting_formatted_number


# create a function to find the average of a list
def average(my_list):
    average = sum(my_list) / len(my_list)
    return average


# create a function to find the median of a list
def median(my_list):
    length = len(my_list)
    my_list.sort()

    if length % 2 == 0:
        median1 = my_list[length // 2]
        median2 = my_list[length // 2 - 1]
        median = (median1 + median2) / 2
    else:
        median = my_list[length // 2]

    return median


def find_ratio(tag_list, tag_type, ratio_name):
    # set ratio to 0 (will return false as boolean)
    ratio = 0

    # iterate through the rows in the table
    for row in tag_list:
        if ratio_name.lower() in row.text.lower():
            tags = row.find_all(tag_type)

            # iterate through tags in row
            for tag in tags:
                if ratio_name.lower() in tag.text.lower():
                    index = tags.index(tag)
                    ratio = string_to_num(tags[index + 1].text)
                    return ratio

    # return a string if no ratio found
    if not ratio:
        print(f"    {ratio_name} not found")
        return '-'


def find_ratio_simple(tag_list, ratio_name):
    # set ratio to 0 (will return false as boolean)
    ratio = 0

    # iterate through the rows in the table
    for tag in tag_list:
        if ratio_name.lower() in tag.text.lower():
            index = tag_list.index(tag)
            ratio = string_to_num(tag_list[index + 1].text)
            return ratio

    if not ratio:
        return '-'

# uses equation to project price of stock based on factors below


def project_price(ratio, primary_stat, shares_outstanding):
    # perform necessary operations
    implied_price = (ratio * primary_stat) / shares_outstanding

    # make into accounting format
    implied_price = af(implied_price)
    return implied_price


def af_average(projections_list):
    # revert numbers from accounting format to floats
    projections_list = list(projections_list)
    print(projections_list)
    working_list = []
    for num in projections_list:
        try:
            num = float(str(num).replace('$', ''))
        except ValueError:
            num = '-'

    # find average of working list
    wl_average = average(working_list)

    # revert to accounting format
    implied_price = af(wl_average)
    return implied_price


def af_median(projections_list):
    # revert numbers from accounting format to floats
    working_list = []
    for num in projections_list:
        try:
            num = float(str(num).replace('$', ''))
        except ValueError:
            num = '-'

    # find median of working list
    wl_median = median(working_list)

    # revert to accounting format
    implied_price = af(wl_median)
    return implied_price
