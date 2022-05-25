#!/usr/bin/python

import subprocess
import sys
import csv
import json
import shutil
import wget
import zipfile

from tqdm import tqdm
from collections import OrderedDict
from multiprocessing import Pool
from helpers.helper import *

outfilename = "results.json"


def analyze(gitpath):
    master_url = gitpath + "/archive/master.zip"
    git_url = "git@github.com:" + gitpath[19:]
    #   cmd = "git clone " + git_url
    soln = OrderedDict()
    soln['repository_url'] = gitpath
    path = os.path.basename(gitpath)
    path = path + "-master"
    dirpath = os.path.join(os.getcwd(), path)
    filepath = dirpath + ".zip"
    try:
        # Repo.clone_from(git_url, dirpath)
        # subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True)
        wget.download(master_url, filepath)
        zip_ref = zipfile.ZipFile(filepath, 'r')
        zip_ref.extractall(dirpath)
        zip_ref.close()
        os.remove(filepath)
        lf = listfiles(dirpath)
        lines = sum(map(loc, lf))
        soln['number of lines'] = lines
        pkgs = set()
        pkgs = reduce(pkgs.union, map(lambda x: set(packages(x)), lf), set())
        soln['libraries'] = list(pkgs)
        pln = map(nesting, lf)
        nl = []
        for i in pln:
            nl.extend(i)
        nf = 1.0 * sum(nl) / len(nl)
        soln['nesting factor'] = nf
        dup_factor = 100.00 * sum(map(duplicate, lf)) / lines
        soln['code duplication'] = dup_factor
        parms = map(parameters, lf)
        pl = []
        for i in parms:
            pl.extend(i)
        avg_params = 1.0 * sum(pl) / len(pl)
        soln['average parameters'] = avg_params
        avg_variables = 1.0 * sum(map(variables, lf)) / lines
        soln['average variables'] = avg_variables
        shutil.rmtree(dirpath)
    except (subprocess.CalledProcessError, ZeroDivisionError, IOError, IndexError,
            TypeError, zipfile.BadZipfile, OSError) as e:
        soln['number of lines'] = 0
        soln['libraries'] = []
        soln['nesting factor'] = 0
        soln['code duplication'] = 0
        soln['average parameters'] = 0
        soln['average variables'] = 0
    return soln


if __name__ == '__main__':
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        urllist = []
        for row in csv_reader:
            urllist.append(row[0])
            line_count += 1
    jsonlist = []
    pool = Pool()
    jsonlist = list(tqdm(pool.imap(analyze, urllist), total=len(urllist)))
    pool.close()
    with open(outfilename, 'w') as outputFile:
        json.dump(jsonlist, outputFile, indent=4)
