#!/bin/sh

pattern=$1
if [ ! -z $pattern ]; then
    pattern="-p *$pattern*.py"
fi
python -m unittest discover -s tests/ -v $pattern

