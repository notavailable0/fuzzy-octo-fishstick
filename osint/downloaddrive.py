import gdown
import random
import os

def main():
    dr = os.listdir()
    files = []
    for d in dr:
        if "order" in d: files.append(d)

    for f in files:
        with open(f) as fl:
             urls = fl.readlines()
        [gdown.download_folder(url) for url in urls]

main()