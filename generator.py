"""Blocklistt
"""
from typing import *
import os
from datetime import datetime as date
import re

now=date.now().strftime("%Y-%m-%d %H:%M:%S")

def generateIPV4Hosts(block_list: list):
    return sorter(block_list, 'hosts')

def generateAdblockList(block_list: list):
    return sorter(block_list, 'adblock')

def genwholelist(block_list: list):
    return sorter(block_list, 'list')

def sorter(domains:list[str], mode):
    '''gets list of domains and returns sorted by domain in alphabetical order'''    
    already = l = []
    entries = '\n'#{time}'

    for i in domains:
        if t := re.findall(r'\w+\.\w+$', i):
            print(i)
            l.append([i.split(t[0])[0], t[-1]])
        else:pass
    l = sorted(l, key = lambda x: x[::-1])

    for i in l:
        domain = i[-1]
        if domain not in already:
            ae=[j if j[-1] == domain else None for j in l]
            ae=list(filter(None, ae))

            so_ = sorted(ae, key = lambda x: x[::-1])


            if mode in ['hosts', 'list']:
                if mode=='hosts':string='0.0.0.0 '
                else:string=''
                entries += f'\n# {domain}\n' + '\n'.join(['{}{}'.format(string, entry) for entry in [''.join(j) for j in so_]])

            elif mode=='adblock':
                entries += '\n||{}^'.format(domain)

            already.append(domain)
    return entries


# All generators
generator_list: dict = {
    "hosts.txt": generateIPV4Hosts,
    "adblok.txt": generateAdblockList,
    "whole.txt": genwholelist
}
file_list=[
    "wot.txt",
    "melcosoft.txt",
    "rom.txt",
    "tikkok.txt"
]
list_=' + '.join(file_list)

def main() -> int:
    # Load the block list to a newline-seperated list
    entries = []
    for i in file_list:
        with open(i, "r") as f:
            rr=f.read().split("\n")
            [entries.append(i) for i in rr]

    # Filter empty lines
    entries = list(filter(None, entries))

    # Create the output dir
    os.makedirs("output", exist_ok=True)

    # Run every generator
    for gen in generator_list:
        print(f"Running generator: {gen}")
        with open(f"output/{gen}", "w") as f:
            f.write(f'''#{now}
            # {list_}
            '''+generator_list[gen](entries))


if __name__ == "__main__":
    main()
