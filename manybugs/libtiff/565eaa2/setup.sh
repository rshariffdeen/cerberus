project_name=libtiff
bug_id=565eaa2
dir_name=$1/manybugs/$project_name/$bug_id
download_url=https://repairbenchmarks.cs.umass.edu/ManyBugs/scenarios/libtiff-bug-2008-12-30-362dee5-565eaa2.tar.gz
current_dir=$PWD
mkdir -p $dir_name
cd $dir_name
wget $download_url
#cp $current_dir/libtiff-bug-2008-12-30-362dee5-565eaa2.tar .
tar xf libtiff-bug-2008-12-30-362dee5-565eaa2.tar.gz
mv libtiff-bug-2008-12-30-362dee5-565eaa2 src
rm libtiff-bug-2008-12-30-362dee5-565eaa2.tar.gz
mv src/* .
rm -rf src
rm -rf  coverage* \
        configuration-oracle \
        local-root \
        limit* \
        *.cache \
        *.debug.* \
        sanity \
        compile.pl \
        *~ \
        test \
        reconfigure \
        preprocessed \
        fixed-program.txt
mv bugged-program.txt manifest.txt
mv *.lines bug-info
mv fix-failures bug-info
mv libtiff src
cd $dir_name/src
cp $current_dir/tif_dirwrite.c ./libtiff/tif_dirwrite.c
cp $current_dir/thumbnail.c ./tools/thumbnail.c
make distclean
chown -R root $dir_name

## Compile libtiff.
make clean
CC=wllvm CXX=wllvm++ ./configure CFLAGS='-g -O0' --enable-static --disable-shared
sed -i '978 s/./\t&/' test/Makefile
CC=wllvm CXX=wllvm++ make CFLAGS="-march=x86-64" -j32

cd $dir_name

## fix the test harness and the configuration script
sed -i "s#/root/mountpoint-genprog/genprog-many-bugs/libtiff-bug-2008-12-30-362dee5-565eaa2#/data/manybugs/libtiff/565eaa2#g" test.sh
sed -i "s#/data/manybugs/libtiff/565eaa2/src/limit#timeout 5#g" test.sh
sed -i "s#/usr/bin/perl#perl#g" test.sh
sed -i "s#cd libtiff#cd src#g" test.sh

cd src

