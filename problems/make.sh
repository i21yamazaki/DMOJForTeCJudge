#!/bin/sh

for problem in ./*/
do
    if [ -d $problem/testcases ]; then
        zip -j $problem/$(basename $problem).zip \
            $problem/testcases/*.in \
            $problem/testcases/*.out
    fi
done
