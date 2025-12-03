#!/bin/bash

DAY=$1

if [ -z "$DAY" ]; then
    CURRENT_DAY=$(date +%-d)
    if [ ! -d "Day${CURRENT_DAY}" ]; then
        DAY=$CURRENT_DAY
    else
        echo "Day${CURRENT_DAY} already exists. Specify a day number."
        exit 1
    fi
fi

python3 -c "from util.web_scraper import WebScraper; WebScraper().retrieve_input($DAY)"
