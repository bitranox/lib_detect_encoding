#!/bin/bash

sudo_askpass="$(command -v ssh-askpass)"
export SUDO_ASKPASS="${sudo_askpass}"
export NO_AT_BRIDGE=1  # get rid of (ssh-askpass:25930): dbind-WARNING **: 18:46:12.019: Couldn't register with accessibility bus: Did not receive a reply.

"$(command -v sudo 2>/dev/null)" git clone https://github.com/bitranox/lib_bash.git /usr/local/lib_bash 2>/dev/null
"$(command -v sudo 2>/dev/null)" chmod -R 0755 /usr/local/lib_bash 2>/dev/null
"$(command -v sudo 2>/dev/null)" chmod -R +x /usr/local/lib_bash/*.sh 2>/dev/null
"$(command -v sudo 2>/dev/null)" /usr/local/lib_bash/install_or_update.sh 2>/dev/null

source /usr/local/lib_bash/lib_helpers.sh


function upgrade_pytest {
    clr_green "updating pytest"
    pip3 install --upgrade pytest 2>/dev/null
    pip3 install --upgrade pytest-pep8 2>/dev/null
}

function upgrade_mypy {
    clr_green "updating mypy"
    pip3 install --upgrade pypy &>/dev/null
}



function pytest_loop {
    local sleeptime_on_error my_dir
    sleeptime_on_error=3
    my_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"
    while true; do
        python3 -m pytest "${my_dir}" --pep8 || banner_warning "Error in PYTEST"
        python3 -m mypy "${my_dir}" --strict --no-warn-unused-ignores || banner_warning "Error in MYPY"
        sleep "${sleeptime_on_error}"
    done

}

upgrade_pytest
upgrade_mypy
pytest_loop


