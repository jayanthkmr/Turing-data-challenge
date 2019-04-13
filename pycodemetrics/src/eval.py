import subprocess
import sys
import csv
import json

from tqdm import tqdm
from collections import OrderedDict
from multiprocessing import Pool
from helpers.helper import *

outfilename = "results.json"


def analyze(gitpath):
    cmd = "git clone " + gitpath
    soln = OrderedDict()
    soln['repository_url'] = gitpath
    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
        path = os.path.basename(gitpath)
        dirpath = os.path.join(os.getcwd(), path)
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
        subprocess.check_call("rm -rf "+dirpath, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError:
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
            if line_count == 0:  # header
                pass
                line_count += 1
            else:
                urllist.append(row[0])
                line_count += 1
    pool = Pool()
    jsonlist = list(tqdm(pool.imap(analyze, urllist), total=len(urllist)))
    pool.close()
    with open(outfilename, 'w') as outputFile:
        json.dump(jsonlist, outputFile, indent=4)
