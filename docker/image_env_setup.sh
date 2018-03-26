#!/bin/bash

# Environment variables.
export PATH="$PATH":"/opt/cantera/bin"
export LD_LIBRARY_PATH="/usr/lib64:/opt/cantera/lib"
export PS1="[\u@docker: \w]\$ "
export TERM="xterm-256color"
export GREP_OPTIONS='--color=auto'

alias ls='ls --color=always'
export EDITOR=/usr/bin/vim

#Limit the core dump size to zero.
ulimit -c 0
ulimit -s unlimited
