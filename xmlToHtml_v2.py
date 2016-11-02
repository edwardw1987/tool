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


def main():

    filepath = sys.argv[1]
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
    templatePath = templatePath = os.path.join(os.path.dirname(__file__), 'template.html')
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
