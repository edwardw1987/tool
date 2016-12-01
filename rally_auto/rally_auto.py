# -*- coding: utf-8 -*-
# @Author: wangwh8
# @Date:   2016-11-30 16:58:08
# @Last Modified by:   wangwh8
# @Last Modified time: 2016-11-30 18:02:16
import subprocess
import os
import argparse
#1 find all *.json of directory
def walk_file_paths(topdir):
    ret = []
    # suffix = '.json'
    suffix = '.py'
    abspath = os.path.abspath(topdir) ##
    for root, dirs, files in os.walk(abspath):
        for name in files:
            if name.endswith(suffix): ##
                fp = os.path.join(root, name)
                ret.append(fp)
    return ret
# cmd e.g rally run task path/to/xxx.json
def main():
    parser = argparse.ArgumentParser(
        prog="rally_auto.py",
        version='v0.1',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="rally automation script")
    parser.add_argument('--dir', dest="workdir", metavar="working directory", action="store", 
                        help="working directory to use", required=True)
    args = parser.parse_args()
    for fp in walk_file_paths(args.workdir):
        cmdFormat = 'rally run task {}'
        print cmdFormat.format(fp)
        s = subprocess.check_output('echo hello', shell=True)
        print repr(s)
if __name__ == '__main__':
    main()