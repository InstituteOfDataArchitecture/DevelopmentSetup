#!/bin/zsh

if [ "$BUILD_DUMMY_DATA" = "TRUE" ]; then
    python courses/1-relational-databases-for-analysts/2-dummy-data/create_dummy_data.py 
fi