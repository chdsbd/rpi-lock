#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python2 $DIR/lock_interface.py &
python2 $DIR/read_process.py &
python2 $DIR/unlock_door.py &
