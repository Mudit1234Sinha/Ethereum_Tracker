from requests import get
from matplotlib import pyplot as plt
from datetime import datetime

API_KEY = 'QFAI6VEKE8MJGGEXIGHZ9KJYPFBG48EJZ4'

BASE_URL = 'https://api.etherscan.io/api'
ETHER_VALUE = 10 ** 18


def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f'?module={module}&action={action}&address={address}&apikey={API_KEY}'

    for key, value in kwargs.items():
        url += f'&{key}={value}'

    return url


def get_account_balance(address):
    get_balance_url = make_api_url('account', 'balance', address, tag='latest')
    response = get(get_balance_url)
    data = response.json()

    value = (int(data['result']) / ETHER_VALUE)
    return value


def get_transactions(address):
    get_transactions_url = make_api_url('account', 'txlist', address, startblock=0, endblock=99999999, page=1,
                                        offset=10000, sort='asc')
    response = get(get_transactions_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
                                                                'Safari/537.36'})
    data = response.json()['result']

    internal_tx_url = make_api_url('account', 'txlistinternal', address, startblock=0, endblock=99999999, page=1,
                                   offset=10000, sort='asc')
    response2 = get(internal_tx_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
                                                                'Safari/537.36'})
    data2 = response2.json()['result']

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))

    current_balance = 0
    balances = []
    times = []

    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / ETHER_VALUE

        if 'gasPrice' in tx:

            gas = int(tx['gasUsed']) * int(tx['gasPrice']) / ETHER_VALUE
        else:
            gas = int(tx['gasUsed']) / ETHER_VALUE
        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value

        else:
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    plt.plot(times, balances)
    plt.show()


address = '0x1aD91ee08f21bE3dE0BA2ba6918E714dA6B45836'
get_transactions(address)
# eth = get_account_balance(address)
# print(eth)
