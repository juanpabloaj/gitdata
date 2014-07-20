#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import os
import subprocess
import copy

from git import git_root

def gitdata_path():
    return os.path.join(git_root(), '.gitdata')

def sha1sum(content):
    return hashlib.sha1(content).hexdigest()

def file_sha1sum(filepath):
    return sha1sum(open(filepath, 'rb').read())

def files_sha1sum(path_list):
    return dict( (f, file_sha1sum(f) ) for f in path_list )

def get_file_list(d="."):

    file_list = []
    for root, dirs, files in os.walk(d, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    return file_list

def gitdata_readlines():
    try:
        return open(gitdata_path()).readlines()
    except IOError:
        return []

def gitdata_info(lines):
    info = {}

    for line in lines:
        line = line.replace('\n','').split(" ")
        sha1, file_path = line[:2]
        info[file_path] = {'sha1':sha1}
        if len(line) == 3:
            info[file_path]['remote'] = line[2]
    return info

def get_gitdata_info():
    return gitdata_info(gitdata_readlines())

def make_ssh_cmd(gitdata_info, cmd):
    ssh_cmd_lines = []

    for file_path, info in gitdata_info.items():
        if 'remote' in info:

            file_name = os.path.basename(file_path)
            remote = "{}{}_{}".format(info['remote'], info['sha1'], file_name)

            if cmd == 'push':
                scp = "scp {} {}".format(file_path, remote)
            else:
                scp = "scp {} {}".format(remote, file_path)

            ssh_cmd_lines.append(scp)

    return ssh_cmd_lines

def remote_sync(cmd='push'):
    gitdata_info = get_gitdata_info()

    for scp in make_ssh_cmd(gitdata_info, cmd):
        print scp
        subprocess.check_output(scp.split(" "))

def status():
    """ check sha1 of file with sha1 in .gitdata """
    gitdata_info = get_gitdata_info()
    for file_path in gitdata_info.keys():
        if file_sha1sum(file_path) != gitdata_info[file_path]['sha1']:
            print "modified:\t"+file_path

def list_files():
    gitdata_info = get_gitdata_info()
    for file_path in gitdata_info.keys():
        print file_path

def make_gitdata_content(gitdata_info):
    content = ''

    for file_path in sorted(gitdata_info.keys()):
        info = gitdata_info[file_path]

        sha1 = info['sha1']
        line = "{} {}".format(sha1, file_path)

        if 'remote' in info:
            line += " {}".format(info['remote'])

        line += '\n'
        content += line

    return content

def update_gitdata_info(gitdata_info, previous_files, new_files_sha1):
    updated = copy.deepcopy(gitdata_info)

    for f in new_files_sha1.keys():
        if f not in previous_files:
            updated[f] = {}
        updated[f]['sha1'] = new_files_sha1[f]

    return updated

def add(d):
    """ add or update sha1 of files """

    gitdata_info = get_gitdata_info()

    new_files_sha1 =  files_sha1sum(get_file_list(d))
    previous_files = gitdata_info.keys()

    gitdata_info = update_gitdata_info(gitdata_info, previous_files, new_files_sha1)

    gitdata = open(gitdata_path(), 'w')
    gitdata.write(make_gitdata_content(gitdata_info))
    gitdata.close()

