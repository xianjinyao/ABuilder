#!/bin/bash

# clean output
rm -rf ../output/*

# clean tmp
for tmp in `find .. -name tmp`
do
    rm -rf $tmp/*
done

# clean mysql_config

