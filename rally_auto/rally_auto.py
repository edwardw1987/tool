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
    suffix = '.json'
    # suffix = '.py'
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
                        help="working directory to use")
    parser.add_argument('--json', dest="json_path", metavar="json file path", action="store", help="json file path")
    
    cmdFormat = 'rally task start {}'
    args = parser.parse_args()
    if args.json_path:
      json_abs_path = os.path.abspath(args.json_path)
      print 'json_abs_path:', json_abs_path	
      cmd = cmdFormat.format(json_abs_path)
      output = subprocess.check_output(cmd, shell=True)
      print output
    elif args.workdir: 
      for fp in walk_file_paths(args.workdir):
          cmd = cmdFormat.format(fp)
    	  print cmd
          output = subprocess.check_output(cmd, shell=True)
  	  print
  	  print 
  	  print
	  print
	  print "output", output


	  break
if __name__ == '__main__':
    main()
