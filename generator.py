"""Blocklistt
"""
import os
from datetime import datetime as date
import re

import urllib.request
import json
from subprocess import check_output


url = "https://edge.microsoft.com/abusiveadblocking/api/v1/blocklist"
print("hello")
response = urllib.request.urlopen(url)
data = json.loads(response.read())
res = [i["url"] for i in data["sites"]]
# Get the timestamp of the response
created_time = data["created_time"]
# Convert the timestamp to a date string using the date command
version = check_output(["date", "-d", f"@{created_time}", "+%Y%m%d%H%M"]).decode().strip()
with open("edge_blocklist", "w") as f:
    f.write(
        f"""! Title: MsEdge blocklist
! Expires: 1 days
! Version: {version}
! Homepage: https://github.com/monolit/fuckhosts

"""
        + "\n".join(res)
    )

now = date.now().strftime("%Y-%m-%d %H:%M:%S")

def generateIPV4Hosts(block_list: list):
    return sorter(block_list, 'hosts')

def generateAdblockList(block_list: list):
    return sorter(block_list, 'adblock')

def genwholelist(block_list: list):
    return sorter(block_list, 'list')

def sorter(domains:list, mode):
    '''gets list of domains and returns sorted by domain in alphabetical order'''    
    already = ll = []
    entries = '\n'#{time}'

    for i in domains:
        if t := re.findall(r'\w+\.\w+$', i):
            print(i)
            ll.append([i.split(t[0])[0], t[-1]])
    ll = sorted(ll, key = lambda x: x[::-1])

    for i in ll:
        domain = i[-1]
        if domain not in already:
            ae=[j if j[-1] == domain else None for j in ll]
            ae=list(filter(None, ae))

            so_ = sorted(ae, key = lambda x: x[::-1])


            if mode == 'adblock':
                entries += f'\n||{domain}^'

            elif mode in ['hosts', 'list']:
                string = '0.0.0.0 ' if mode == 'hosts' else ''
                entries += (
                    f'\n# {domain}\n'
                    + '\n'.join(
                        [
                            f'{string}{entry}'
                            for entry in [''.join(j) for j in so_]
                        ]
                    )
                    + '\n'
                )

            already.append(domain)
    return entries


# All generators
generator_list: dict = {
    "hosts.txt": generateIPV4Hosts,
    "adblok.txt": generateAdblockList,
    "whole.txt": genwholelist
}
file_list = [
    "wot.txt",
    "melcosoft.txt",
    "rom.txt",
    "tikkok.txt",
    "edge_blocklist"
]

extra_list = [
    "banking_ru.txt",
    "extras.txt",
    "resabuse.txt"
]

list_ = ' + '.join(file_list)
list_2 = ' + '.join(extra_list)

def main() -> int:
    # Load the block list to a newline-seperated list
    entries = []
    for i in file_list+extra_list:
        with open(i, "r") as f:
            rr = f.read().split("\n")
            [entries.append(i) for i in rr]

    # Create the output dir
    os.makedirs("output", exist_ok=True)

    entries = list(filter(None, entries))
    # Run every generator
    for gen in generator_list:
        print(f"Running generator: {gen}")
        with open(f"output/{gen}", "w") as f:
            f.write(
                f'''# {now}
# {list_+list_2}
{generator_list[gen](entries)}'''
            )


if __name__ == "__main__":
    main()
