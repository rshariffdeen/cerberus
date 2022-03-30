#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
benchmark_name=$(echo $script_dir | rev | cut -d "/" -f 3 | rev)
project_name=$(echo $script_dir | rev | cut -d "/" -f 2 | rev)
bug_id=$(echo $script_dir | rev | cut -d "/" -f 1 | rev)
dir_name=$1/$benchmark_name/$project_name/$bug_id
scenario_id=libtiff-bug-2008-04-15-2e8b2f1-0d27dc0
cd $dir_name
TEST_ID=$2
POS_N=61
NEG_N=1

if [ -z "$TEST_ID" ]
then
   # Run passing test cases
  for i in `seq -s " " -f "p%g"  1 $POS_N`
  do
  bash test.sh $i /data
  done

  # Run failing test cases
  for i in `seq -s " " -f "n%g"  1 $NEG_N`
  do
  bash test.sh $i /data
  done
else
  pattern=`expr substr "$TEST_ID" 1 1`
  num=`expr substr "$TEST_ID" 2 ${#TEST_ID}`

  if [[ $pattern == 'n' ]]; then
      cd $dir_name
      timeout 5 bash test.sh $TEST_ID
  elif [[ $pattern == 'p' ]]; then
      cd $dir_name
      timeout 5 bash test.sh $TEST_ID
  else
      cd $dir_name/src
      timeout 5 perl $dir_name/${project_name}-run-tests.pl $TEST_ID
  fi

fi