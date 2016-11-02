#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-10-28 23:23:01
# @Last Modified by:   edward
# @Last Modified time: 2016-10-29 01:19:05
import xml.etree.ElementTree as ET
import os
import sys
import argparse
import time
import socket

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def main():
    """
    usage:
    python xmlToHtml.py --dir dirname --xunit-file filepath
    e.g
        $ python xmlToHtml.py --xunit-file=tempest.xml
        RUN: nosetests tempest/ --with-xunit --xunit-file=tempest.xml -v
        wait for seconds...
        output to tempest.html
    """
    # defaultOutputFilename = time.strftime('%Y%d%m%H%M%S') + '.xml'
    defaultOutputFilename = 'tempest.xml'
    defaultDirname = 'tempest/'
    # cmd:　nosetests tempest/ --with-xunit --xunit-file=/root/tempest.xml -v

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Transform xunit-file of xml into html, V0.1")
    parser.add_argument('--dir', dest="workdir", metavar="working directory", action="store", default=defaultDirname,
                        help="working directory to use")
    parser.add_argument('--xunit-file', dest="xunitFile", metavar="xunitFile",
                        type=str, default=defaultOutputFilename,
                        required=False, action="store", help="output xml filepath")
    args = parser.parse_args()
    cmd_tpl = "nosetests %(workdir)s --with-xunit --xunit-file=%(outFilePath)s -v"
    outFileAbsPath = os.path.join(BASE_DIR, args.xunitFile)
    cmd_str = cmd_tpl % dict(workdir=args.workdir, outFilePath=outFileAbsPath)
    print 'RUN: %s' % cmd_str
    signal = os.system(cmd_str)

    print 'wait for seconds...'
    time_counter = 0
    while not os.path.exists(outFileAbsPath):
        time.sleep(0.5)
        time_counter += 0.5
        if time_counter > 5:
            return
    # if len(sys.argv) < 2:
    #     sys.exit(0)
    # filepath = sys.argv[1]
    oldfilepath = outFileAbsPath
    filepath = os.path.splitext(oldfilepath)[0] + '_%s.xml' % time.strftime('%Y%d%m%H%M%S')
    print 'old:', oldfilepath
    print 'new:', filepath
    os.rename(oldfilepath, filepath)
    tree = ET.parse(filepath)
    root = tree.getroot()
    all = 0
    errorsNum = 0
    fails = 0
    skip = 0
    startTpl = """
    <tr>
        <td>{no}</td>
        <td>{classname}</td>
        <td>{name}</td>
        <td>{time}</td>
    """
    errorLinkTpl = "<td><a data-error=\"{no}\" href=\"javascript:;\">{errorName}</a></td>"
    errorDivTpl = """
    <div class="error-msg" id="error-msg-{no}" style="display: none;">
        <span style="float:left; color: red; font-size:2em;">{no}</span>
        <a style="float: right; color:white; font-size:2em; text-decoration:none;" data-error=\"{no}\" href="javascript:;">X</a>
        <p style="font-size:1.5em;">{errorMsg}</p>
    </div>
    """
    html = ""
    errorDivHtml = ""
    for idx, val in enumerate(root):
        all += 1
        params = val.attrib.copy()
        params["no"] = idx + 1
        html += startTpl.format(**params)
        for e in val:
            errorsNum += 1
            errorDivHtml += errorDivTpl.format(no=idx + 1, errorMsg=e.text)
            if e.tag == "error":
                html += errorLinkTpl.format(no=idx + 1,
                                            errorName=e.attrib["type"])
            elif e.tag == "system-err":
                html += errorLinkTpl.format(no=idx + 1, errorName="system-err")

        html += '</tr>'
    templatePath = os.path.join(os.path.dirname(__file__), 'template.html')
    with open(templatePath) as fp:
        outhtml = fp.read().replace(
            "{{template}}", html).replace(
            "{{all}}", str(all)).replace(
            "{{display}}", str(all)).replace(
            "{{errorsNum}}", str(errorsNum)).replace(
            "{{fails}}", str(fails)).replace(
            "{{skip}}", str(skip)).replace(
            "{{errorDivs}}", errorDivHtml
        )

    newfilepath = os.path.splitext(filepath)[0] + '.html'
    with open(newfilepath, 'w') as outf:
        print 'output to %s' % newfilepath
        outf.write(outhtml)


if __name__ == '__main__':
    main()
