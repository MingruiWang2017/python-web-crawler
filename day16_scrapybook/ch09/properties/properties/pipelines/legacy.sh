#!/bin/bash

trap "" SIGINT  # 进入ctrl + C，想停止改脚本需要ctrl + D

sleep 3

while read line
do
    # 4 per second
    sleep 0.25
    awk "BEGIN {print 1.20 * $line}"  # 读入值 * 1.2
done