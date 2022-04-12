#!/usr/bin/env python
# Copyright (C) 2016 Fan Long, Martin Rianrd and MIT CSAIL
# Prophet
#
# This file is part of Prophet.
#
# Prophet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prophet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prophet.  If not, see <http://www.gnu.org/licenses/>.
from sys import argv
from os import system, path, chdir, getcwd, environ
from tester_common import extract_arguments
import subprocess
import getopt


def compileit(out_dir, compile_only=False, config_only=False, paraj=0):
    ori_dir = getcwd()
    chdir(out_dir)

    my_env = environ
    my_env["LD"] = "/usr/bin/ld -m elf_x86_64"
    # my_env["PATH"] = deps_dir + "/apr-1.5.1-build/bin:" + my_env["PATH"]
    # my_env["PATH"] = deps_dir + "/apr-util-1.5.3-build/bin:" + my_env["PATH"]

    if not compile_only:
        my_env["CFLAGS"] = "-g -O0 -Wno-error"
        my_env["CXXFLAGS"] = my_env["CFLAGS"]
        my_env["FORCE_UNSAFE_CONFIGURE"] = "1"
        config_command = "./configure --disable-pthreads".split(" ")
        ret = subprocess.call(config_command, env=my_env)
        if ret != 0:
            print("Configure Error!")
            chdir(ori_dir)
            exit(1)
        system("make clean")

    if not config_only:
        my_env["CFLAGS"] = "-fsanitize=address -g -O0"
        my_env["CXXFLAGS"] = "-fsanitize=address -g -O0"
        my_env["LDFLAGS"] = "-fsanitize=address"
        my_env["ASAN_OPTIONS"] = "detect_leaks = 0"
        if (paraj == 0):
            ret = subprocess.call(
                ["make", "CFLAGS=\"-fsanitize=address\"", "CXXFLAGS=\"-fsanitize=address\"", "src/shred"],
                env=my_env)
        else:
            ret = subprocess.call(
                ["make", "CFLAGS=\"-fsanitize=address\"", "CXXFLAGS=\"-fsanitize=address\"", "src/shred",
                 "-j", str(paraj)],
                env=my_env)
        if ret != 0:
            print("Failed to make!")
            exit(1)

    # ret = subprocess.call(["make", "install"], env = my_env)
    # if ret != 0:
    #   print "Failed to make install!"
    #   exit(1)

    chdir(ori_dir)


if __name__ == "__main__":

    compile_only = False
    opts, args = getopt.getopt(argv[1:], 'cd:hlj:p:r:x')
    dryrun_src = ""

    paraj = 0

    print_fix_log = False
    print_usage = False
    config_only = False
    for o, a in opts:
        if o == "-d":
            dryrun_src = a
        elif o == "-p":
            if a[0] == "/":
                deps_dir = a
            else:
                deps_dir = getcwd() + "/" + a
        elif o == "-x":
            config_only = True
        elif o == "-c":
            compile_only = True
        elif o == "-l":
            print_fix_log = True
        elif o == "-h":
            print_usage = True
        elif o == "-j":
            paraj = int(a)

    if (len(args) < 1) or (print_usage):
        print("Usage: libtiff-build.py <directory> [-d src_file | -l] [-h]")
        exit(0)

    out_dir = args[0]
    # fetch from github if the directory does not exist
    if path.exists(out_dir):
        print("Working with existing directory: " + out_dir)
    else:
        print("Non-exists directory")
        exit(1)

    compileit(out_dir, compile_only, config_only, paraj)
    if dryrun_src != "":
        (builddir, buildargs) = extract_arguments(out_dir, dryrun_src)
        if len(args) > 1:
            out_file = open(args[1], "w")
            print >> out_file, builddir
            print >> out_file, buildargs
            out_file.close()
        else:
            print(builddir)
            print(buildargs)
