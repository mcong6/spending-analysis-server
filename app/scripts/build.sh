#!/usr/bin/env bash
set -e
rm -rf $PWD/cenv
echo "$(date) - Create conda environment in $PWD/cenv"
conda env create -f scripts/environments.yml -p $PWD/cenv
ls -l $PWD/cenv
