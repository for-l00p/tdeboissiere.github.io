Title: CelebA dataset: a parallel download from dropbox
Date: 2016-05-17
Category: Deep Learning
Tags: python, multiprocessing, datasets
Author: TDB
Summary: Using the multiprocessing module to download the CelebA dataset


# Introduction

I recently got interested in face recognition with deep learning. I eventually chanced upon the [CelebA dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html). It is freely available for academic purposes and has facial attributes annotations.

However, it is a bit of a pain to download. It is split into 14 independent `.zip` on Dropbox. And you can't download all these files at the same time (probably because of server restrictions).

So I decided to write a script to do the download for me. And for the sake of it, demonstrate how simple it is to parallelize processes with the python `map` function and the `multiprocessing` module.

# Install dependencies

You should make sure to have urllib2 and bs4 installed.

# Strategy breakdown

- Use urllib2 and bs4 to parse the target url and look for the download links.
- Use subprocess to call the wget module (probably possible to do it with some python functions as well but I did not bother to search).
- Use the map function for easy multiprocessing.

# The code 

This code has been tailored to the dropbox page of the [CelebA dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html). It should be simple enough to adapt to other purposes.

Simply call:

	python <name_of_the_file_you_put_the_code_in>

For completeness sake, here are the running times:

- Download in parallel with this code : 515 sec for 2 `.zip` folders
- Download in serial : 540 sec for 2 `.zip` folders


```
from bs4 import BeautifulSoup
import urllib2
import subprocess
from multiprocessing.dummy import Pool as ThreadPool
import time


def download_from_dropbox(url):

	# Get the content of the url page
    resp = urllib2.urlopen(url)
    # Parse it with beautifulsoup
    soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().getparam('charset'))

    list_zip = []

    # Look for the links in the soup
    for link in soup.find_all('a', href=True):
        try:
            # Exploring the source code of said page shows
            # that the links I'm interested in have these properties
            if link["class"] == ["file-link"]:
                list_zip.append(link["href"])
        except KeyError:
            pass

    # Strip the "?dl=0" at the end of each link
    list_zip = [f.split("?dl=0")[0] for f in list_zip]

    # Function we'll map to the url so that the calls
    # are in parallel
    def call_wget(file_name):
        subprocess.call('wget ' + file_name, shell=True)

    pool = ThreadPool(4)  # Sets the pool size to 4
    # Open the urls in their own threads
    # and return the results
    pool.map(call_wget, list_zip)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()


if __name__ == '__main__':

    links = ["https://www.dropbox.com/sh/8oqt9vytwxb3s4r/AAAq9krDJxUMh1m0hbbxdnl4a/Img/img_celeba.7z?dl=0"]

    start = time.time()
    for url in links:
        download_from_dropbox(url)
    print time.time() - start
```
