import os

import requests

session = requests.Session()

session.cookies.set('wpsua', 'FILL YOUR COOKIE HERE')
session.cookies.set('wps_sid', 'FILL YOUR COOKIE HERE')
devices: list[str] = ['1234567']  # FILL YOUR DEVICES ID HERE, you can get it from the url of the device page


def get_files(device: str):
    count = 20
    offset = 0
    while True:
        resp = session.get(
            f'https://drive.wps.com/api/v5/groups/tmp/devices/{device}/files?count={count}&offset={offset}')
        files = resp.json()['files']
        if not files:
            break
        for file in files:
            yield file
        offset += count


def download_file(file):
    url = f"https://drive.wps.com/api/v3/groups/{file['groupid']}/files/{file['id']}/download"
    download_url = session.get(url).json()['fileinfo']['url']
    with open('data/' + file['fname'], 'wb') as f:
        f.write(session.get(download_url).content)
    print(f"Downloaded {file['fname']}")


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    for device in devices:
        for file in get_files(device):
            download_file(file)
