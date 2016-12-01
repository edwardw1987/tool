# -*- coding: utf-8 -*-
# @Author: wangwh8
# @Date:   2016-11-30 16:58:08
# @Last Modified by:   wangwh8
# @Last Modified time: 2016-12-01 11:36:06
import subprocess
import os
import argparse
import re
# 1 find all *.json of directory
def walk_file_paths(topdir):
    ret = []
    suffix = '.json'
    abspath = os.path.abspath(topdir)
    for root, dirs, files in os.walk(abspath):
        for name in files:
            if name.endswith(suffix):
                fp = os.path.join(root, name)
                ret.append(fp)
    return ret

def handle_output(output):
    pat = re.compile(r'rally task report ([0-9a-z-]{10,}) --out output.html')
    groups = pat.search(output)
    task_report_cmd = groups.group(0)
    task_uuid = groups.group(1)
    outfilepath = os.path.join(os.path.dirname(__file__), task_uuid + '.html')
    task_report_cmd = task_report_cmd.replace('output.html', outfilepath)
    print 'task_report_cmd:', task_report_cmd
    # return task_report_cmd
    subprocess.call(task_report_cmd, shell=True)
    # handle reprot script
    #outfilepath = './30b4cdc0-9e89-4b78-bfb0-a5c716858550.html'
    script_pat = re.compile(r'https://.+\.js')
    prefix = r'\\10.240.196.10\du\Openstack\Performance Test\js'
    print 'prefix:', prefix
    with open(outfilepath) as inf:
        content = inf.read()
        new_content = content
        for src in script_pat.findall(content):
            newsrc = prefix + '\\' + src.rsplit('/', 1)[-1]
            new_content = new_content.replace(src, newsrc)
            print 'INFO: replace "%s" with "%s"' % (src, newsrc)
    with open(outfilepath, 'w') as outf:
        outf.write(new_content)
    print 'finished.'
        # 


    # rally task report 4235fc2d-e9e4-4d31-a5fa-b6339ab3204c --out output.html
def main():
    parser = argparse.ArgumentParser(
        prog="rally_auto.py",
        version='v0.1',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="rally automation script")
    parser.add_argument('--dir', dest="workdir", metavar="working directory", action="store",
                        help="working directory to use")
    parser.add_argument('--json', dest="json_path",
                        metavar="json file path", action="store", help="json file path")

    cmdFormat = 'rally task start {}'
    args = parser.parse_args()
    if args.json_path:
        json_abs_path = os.path.abspath(args.json_path)
        print 'json_abs_path:', json_abs_path
        cmd = cmdFormat.format(json_abs_path)
        output = subprocess.check_output(cmd, shell=True)
        handle_output(output)
    elif args.workdir:
        for fp in walk_file_paths(args.workdir):
            cmd = cmdFormat.format(fp)
            print cmd
            output = subprocess.check_output(cmd, shell=True)
            task
            break
if __name__ == '__main__':
    main()

    #handle_output(open('output.txt').read())
