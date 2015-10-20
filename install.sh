#! /bin/sh

install="full"
if [ "$1" == "-lite" ]; then
    install="lite"
fi

location="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [[ $install == "full" ]]; then
    cmdlist=(
    "lock_interface.py"
    "read_process.py"
    "unlock_door.py"
    )
else
    cmdlist=(
    "read_process.py"
    "unlock_door.py"
    )
fi

echo "setting up database"
$location/sql_setup.py

echo "starting lock"
for cmd in ${cmdlist[*]}
do
    sudo $location/$cmd &
done 

echo "adding programs to cron"
for cmd in ${cmdlist[*]}
do
    job="@reboot $location/$cmd"
    cat <(fgrep -i -v "$cmd" <(sudo crontab -l)) <(echo "$job") | sudo crontab -
done
