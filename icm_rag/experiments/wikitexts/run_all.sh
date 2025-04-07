#!/usr/bin/bash

# Get the name of this script
this_script="$(basename "$0")"

# Iterate over all .sh files in the current directory
for script in *.sh; do
    # Skip this script itself
    if [[ "$script" == "$this_script" ]]; then
        continue
    fi

    echo "Running $script"
    bash "$script"
done
