#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
benchmark_name=$(echo $script_dir | rev | cut -d "/" -f 3 | rev)
project_name=$(echo $script_dir | rev | cut -d "/" -f 2 | rev)
bug_id=$(echo $script_dir | rev | cut -d "/" -f 1 | rev)
dir_name=$1/$benchmark_name/$project_name/$bug_id
current_dir=$PWD

cp CONFIG.json $dir_name/

mkdir -p $dir_name
cd $dir_name
project_url=https://github.com/apache/tomcat.git

bug_commit_id=49ff4703e46feb23ec1dd3a9f3576231446f6dee
git clone $project_url src
cd src
git checkout $bug_commit_id

sed -i "20 i\import com.facebook.infer.annotation.*;" java/org/apache/coyote/http2/Http2AsyncParser.java
sed -i "s/public class/@ThreadSafe public class/g" java/org/apache/coyote/http2/Http2AsyncParser.java
