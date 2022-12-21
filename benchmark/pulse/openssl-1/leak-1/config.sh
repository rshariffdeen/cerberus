#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
benchmark_name=$(echo $script_dir | rev | cut -d "/" -f 3 | rev)
project_name=$(echo $script_dir | rev | cut -d "/" -f 2 | rev)
bug_id=$(echo $script_dir | rev | cut -d "/" -f 1 | rev)
dir_name=$1/$benchmark_name/$project_name/$bug_id
cd $dir_name/src


PROJECT_CFLAGS="-O0 -g -Wno-error"
PROJECT_CXXFLAGS="-O0 -g -Wno-error"


if [[ -n "${CFLAGS}" ]]; then
  PROJECT_CFLAGS="${PROJECT_CFLAGS} ${CFLAGS}"
fi
if [[ -n "${CXXFLAGS}" ]]; then
  PROJECT_CXXFLAGS="${PROJECT_CXXFLAGS} ${CXXFLAGS}"
fi


PROJECT_CONFIG_OPTIONS="--disable-shared --disable-gdb --disable-libdecnumber --enable-static"

if [[ -n "${CONFIG_OPTIONS}" ]]; then
  PROJECT_CONFIG_OPTIONS="${PROJECT_CONFIG_OPTIONS} ${CONFIG_OPTIONS}"
fi

CFLAGS="${PROJECT_CFLAGS}"  CXXFLAGS="${PROJECT_CXXFLAGS}"  ./configure  ${PROJECT_CONFIG_OPTIONS}
