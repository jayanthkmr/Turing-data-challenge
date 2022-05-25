#!/usr/bin/python

import os
import re

python_keywords = [
    'and', 'del', 'from', 'not', 'while',
    'as', 'elif', 'global', 'or', 'with',
    'assert', 'else', 'if', 'pass', 'yield',
    'break', 'except', 'import', 'print',
    'class', 'exec', 'in', 'raise',
    'continue', 'finally', 'is', 'return',
    'def', 'for', 'lambda', 'try'
]


def listfiles(dirpath):
    lf = []
    for root, dirs, files in os.walk(dirpath):
        for filepath in files:
            if filepath.endswith(".py"):
                lf.append(os.path.join(root, filepath))
    return lf

def duplicate(filepath):
    ld = dict()
    linecount = 0
    for line in open(filepath):
        line = line.strip()
        line = re.sub(r"\s+", "", line)
        if line.startswith("#"):
            pass
        linecount += 1
        if line in ld:
            ld[line] += 1
        else:
            ld[line] = 1
    if '' in ld:
        del ld['']
    duplinecount = linecount - len(ld)
    return duplinecount


def loc(filepath):
    num_lines = sum(1 for line in open(filepath))
    return num_lines


def nesting(filepath):
    pn = 0
    nl = []
    base_indentation = 4
    base_indentation_set = False
    base_indentation_tab = True
    previndentation_level = 0
    for line in open(filepath):
        linec = line.strip()
        if line[0] == "\t" and not base_indentation_set:
            base_indentation = len(line) - len(line.lstrip("\t"))
            base_indentation_set = True
            base_indentation_tab = True
        elif line[0] == " " and not base_indentation_set:
            base_indentation = len(line) - len(line.lstrip(" "))
            base_indentation_set = True
            base_indentation_tab = False
        elif line[0] == "\t" or line[0] == " ":
            if base_indentation_tab:
                indentationlevel = len(line) - len(line.lstrip("\t"))
            else:
                indentationlevel = (len(line) - len(line.lstrip(" "))) / base_indentation
            if linec.startswith("for"):
                if previndentation_level >= indentationlevel:
                    if pn != 0:
                        nl.append(pn)
                    pn = 1
                else:  # nesting
                    pn += 1
            previndentation_level = indentationlevel
    nl.append(pn)
    #print(nl)
    return nl


def packages(filepath):
    pkgs = list()
    for line in open(filepath):
        linesplit = line.strip().split(" ")
        firstword = linesplit[0].strip()
        if firstword == "import":
            map(pkgs.append, linesplit[1].strip().split(","))
        elif firstword == "from":
            pkgs.append(linesplit[1].strip())
        else:
            pass
    return pkgs


def parameters(filepath):
    pl = list()
    for line in open(filepath):
        linesplit = line.strip().split(" ")
        firstword = linesplit[0].strip()
        if firstword == "def":
            count_comma = line.count(',')
            if count_comma == 0:
                pl.append(0)
            else:
                pl.append(count_comma + 1)
        else:
            pass
    return pl


def variables(filepath):
    vd = set()
    fd = set()
    for line in open(filepath):
        if "\"" in line or "'" in line:
            pass
        else:
            regexp1 = r"[_a-zA-Z][_a-zA-Z0-9]*"  # all chars possible
            regexp2 = r"[_a-zA-Z][_a-zA-Z0-9]*\s*\("  # all function ids
            ids = re.findall(regexp1, line)
            fids = re.findall(regexp2, line)
            for id in ids:
                if id not in python_keywords:
                    if id not in vd:
                        vd.add(id)
            for fid in fids:
                fid = fid[:-1]
                if fid in vd:
                    vd.remove(fid)
    return len(vd)