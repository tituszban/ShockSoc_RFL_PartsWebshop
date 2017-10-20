import json
import os.path
import requests

address = 'ec2-35-176-114-206.eu-west-2.compute.amazonaws.com'

def upload_stock():
    file_name = input('stock csv file name: ')
    if not os.path.isfile(file_name):
        print('file not found')
        return

    stock = {}

    with open(file_name) as file:
        for line in file:
            columns = line.split(',')
            if columns[2].isdigit():
                stock[columns[2]] = {"description": columns[1], "qty": int(columns[6]),
                                     "price": float(columns[8].replace('Â', '').replace('£', ''))}
    stock['uploader_key'] = 'michaelFaraday'

    confirmation = input('Are you sure, you want to update the stock (Y/n): ')
    if confirmation.lower() != 'y':
        print('cancel')
        return
    else:
        stock['confirmed'] = 'confirmed'

    r = requests.post('http://%s/upload_stock' % address, json=stock)
    if r.ok:
        print('Success')


def download_stock():
    r = requests.get('http://%s/get_stock' % address)
    stock = r.json()
    data = '\n'.join([','.join([stock[key]['description'], key, str(stock[key]['qty'])]) for key in stock.keys() ])
    if r.ok:
        print('Downloaded')
        with open('downloaded_stock.csv', 'w') as save:
            save.write(data)
        print('Saved to downloaded_stock.csv')


def download_transactions():
    r = requests.get('http://%s/get_transactions' % address)
    transactions = r.json()
    #print(transactions)
    data = []
    for key in transactions.keys():
        if transactions[key]['session state'] == 'complete':
            item = [key, transactions[key]['name'], transactions[key]['email'], transactions[key]['ssid']]
            for order in transactions[key]['order items'].keys():
                item.append(order)
                item.append(str(transactions[key]['order items'][order]['qty']))
            data.append(','.join(item))
    result = '\n'.join(data)
    if r.ok:
        print('Downloaded')
        with open('transactions.csv', 'w') as save:
            save.write(result)
        print('Saved to transactions.csv')


def main():
    instruction = {'u': {'name': 'Upload stock', 'function': upload_stock}, 'd': {'name': 'Download stock', 'function': download_stock}, 't': {'name': 'Download transactions', 'function': download_transactions}}
    while True:
        print('Press:')
        print('\tUpload stock: u')
        print('\tDownload stock: d')
        print('\tDownload transaction: t')
        print('\tquit: q')

        inp = input('>').lower()
        if inp == 'q':
            return

        if inp in instruction.keys():
            print(instruction[inp]['name'])
            instruction[inp]['function']()


if __name__ == '__main__':
    main()