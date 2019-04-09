#!/bin/bash

git pull origin master
supervisorctl restart pmsb-web
