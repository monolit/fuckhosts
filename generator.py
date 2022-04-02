"""Blocklistt
"""
from typing import *
import os, sys
from datetime import datetime as date

now=date.now().strftime("%Y-%m-%d %H:%M:%S")

def generateIPV4Hosts(block_list: List[str]) -> List[str]:
    return [f"{entry}" for entry in block_list]

def generateAdblockList(block_list: List[str]) -> List[str]:
    return ["||{}^".format(entry) for entry in block_list]


# All generators
generator_list: dict = {
    "hosts.txt": generateIPV4Hosts,
    "adblok.txt": generateAdblockList
}
file_list=[
	"wot.txt",
	"melcosoft.txt",
	"rom.txt",
	"tikkok.txt"
]

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
            f.write(f"#{now}\n"+"\n".join(generator_list[gen](entries)))


if __name__ == "__main__":
    main()
