script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
benchmark_name=$(echo $script_dir | rev | cut -d "/" -f 3 | rev)
project_name=$(echo $script_dir | rev | cut -d "/" -f 2 | rev)
bug_id=$(echo $script_dir | rev | cut -d "/" -f 1 | rev)
dir_name=/data/$benchmark_name/$project_name/$bug_id
cd $dir_name/src

# Config libtiff.
make clean

sed -i 's/no-dependencies ansi2knr/no-dependencies/g' configure.in
./.bootstrap
./configure --disable-shared --enable-static \
            --disable-fft \
            --disable-mpbsd \
            --disable-cxx \
            --disable-fast-install \
            --disable-minithres