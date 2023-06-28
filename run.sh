#!/bin/bash

#######################
# User Configurations
#######################

SCRIPT_FOLDER=keelimebot
SCRIPT_MAIN=${SCRIPT_FOLDER}.main
TWITCH_SUDO_ID=

# Point to your python 3 executable
PYTHON=python

# STRONGLY RECOMMENDED!
# so long as you have pip installed: (e.g. `apt-get install python3-pip`)
# then the run script will set this up automatically
USE_VENV=yes # no|yes

#######################
#######################

print_usage () {
    echo "usage: \`$0 [help|venv|test|format|-h]\`"
    echo "  args:"
    echo "     help: prints this"
    echo "     venv: updates the virtual environment"
    echo "     test: runs the tests"
    echo "     format: runs the autoformatter"
    echo "     -h: prints bot script help options"
}

validate_script_assumptions () {
    # Check python version
    if [ "$(${PYTHON} -c "import sys; print(sys.version_info[0])")" -ne 3 ]; then
        echo "This script assumes python version 3, you are using:"
        ${PYTHON} --version
        exit 1
    fi

    # Check script directory
    if [ "$(dirname $0)" != "." ]; then
        echo "This script needs to be ran from within it's own directory, e.g. \`./$(basename $0)\`"
        exit 1
    fi

    # ${PYTHON} -c "import tkinter" > /dev/null 2>&1
    # if [ "$?" != "0" ]; then
    #     echo "This script requires tkinter, try \`apt-get install python3-tk\`"
    #     exit 1
    # fi

    # Require at least one argument
    if [ "$#" -eq 0 ]; then
        print_usage
        exit 1
    fi
}

activate_venv () {
    if [ "${USE_VENV}" == "yes" ]; then
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate || exit 1
        elif [ -f "venv/Scripts/activate" ]; then
            source venv/Scripts/activate || exit 1
        else
            echo "Virtual environment is not setup! Try \`$0 venv\` or modify \"USE_VENV\" in script configuration."
            exit 1
        fi
    elif [  "${USE_VENV}" != "no"  ]; then
        echo "invalid configuration: \"USE_VENV\" should be yes|no"
        exit 1
    fi
}

run_venv () {
    if [ "${USE_VENV}" == "yes" ]; then
        if [ ! -f "venv/Scripts/activate" ] && [ ! -f "venv/bin/activate" ]; then
            ${PYTHON} -m pip install virtualenv || exit 1
            ${PYTHON} -m virtualenv venv || exit 1

            activate_venv

            ${PYTHON} -m pip install --upgrade pip
            ${PYTHON} -m pip install flake8 pytest coverage autopep8
            ${PYTHON} -m pip install -r requirements.txt

        else
            activate_venv
            ${PYTHON} -m pip install -r requirements.txt
        fi

    else
        echo "Sorry, but your configurations specify not to use a virtual environment!"
        exit 1
    fi
}

run_test () {
    activate_venv

    flake8 ${SCRIPT_FOLDER} --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 ${SCRIPT_FOLDER} --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    coverage run --source=${SCRIPT_FOLDER} -m pytest
    coverage report --skip-covered
}

run_format () {
    activate_venv

    for f in `find ${SCRIPT_FOLDER} -name "*.py"`; do autopep8 --in-place --max-line-length=127 $f; done
}

make_twitch_secret () {
    echo "Detected first-time setup of Twitch bot"
    openssl version || exit 1
    echo "Ready to encrypt twitch secret, enter your info:"

    read -p "TWITCH_ID (Client ID - passed to authorization endpoints to identify your application): " TWITCH_ID
    echo
    read -s -p "TWITCH_SECRET (Client Secret - passed to token exchange endpoints to obtain a token): " TWITCH_SECRET
    echo
    read -s -p "TWITCH_TOKEN (Access Token): " TWITCH_TOKEN
    echo
    read -s -p "TWITCH_REFRESH_TOKEN (Refresh Token): " TWITCH_REFRESH_TOKEN
    echo

    read -s -p "Enter a password to protect your secret: " PASS
    echo

    echo ${TWITCH_ID}$'\n'${TWITCH_SECRET}$'\n'${TWITCH_TOKEN}$'\n'${TWITCH_REFRESH_TOKEN} | openssl enc -aes-256-cbc -pbkdf2 -salt -pass pass:$PASS > twitch_secret || exit 1
    echo "Your twitch secret has been encrypted! Simply delete the \"twitch_secret\" file to reset it."
    echo ""

    set -o pipefail
    DATA_DIR=`${PYTHON} -m ${SCRIPT_MAIN} $@ --print-data-dir | tail -n1`
    if [ "$?" -eq 1 ]; then
        exit 1
    fi

    if [ ! -f "${DATA_DIR}/twitch_channels.json" ]; then
        read -p "Which Twitch channel do you want to connect to? (you can add more channels later): " TWITCH_CHANNEL

        mkdir -p ${DATA_DIR}
        echo "{\"initial_channels\":[\"${TWITCH_CHANNEL}\"]}" > ${DATA_DIR}/twitch_channels.json

        echo "You can modify your channels for future in: \"${DATA_DIR}/twitch_channels.json\""
    fi
}

make_discord_secret () {
    echo "Detected first-time setup of Discord bot"
    openssl version || exit 1
    echo "Ready to encrypt discord secret, enter your info:"

    read -p "DISCORD_OWNER_ID (User ID): " DISCORD_OWNER_ID
    echo
    read -p "BOT_EMOJI_GUILD (Guild ID): " BOT_EMOJI_GUILD
    echo
    read -s -p "DISCORD_TOKEN: " DISCORD_TOKEN
    echo

    read -s -p "Enter a password to protect your secret: " PASS
    echo

    echo ${DISCORD_OWNER_ID}$'\n'${BOT_EMOJI_GUILD}$'\n'${DISCORD_TOKEN} | openssl enc -aes-256-cbc -pbkdf2 -salt -pass pass:$PASS > discord_secret || exit 1
    echo "Your discord secret has been encrypted! Simply delete the \"discord_secret\" file to reset it."
}

run_bot () {
    activate_venv

    TWITCH_ID=""
    TWITCH_SECRET=""
    TWITCH_TOKEN=""
    TWITCH_REFRESH_TOKEN=""
    DISCORD_OWNER_ID=""
    BOT_EMOJI_GUILD=""
    DISCORD_TOKEN=""

    IS_HELP=0
    for arg in $@; do
        if [ "${arg}" == "-h" ] || [ "${arg}" == "--help" ]; then
            IS_HELP=1
        fi
    done

    if [ "${IS_HELP}" -eq 0 ]; then
        if [ "$1" == "twitch" ]; then
            if [ ! -f "twitch_secret" ]; then
                make_twitch_secret $@
            fi

            PASS=
            if [ -z ${PASS} ]; then
                read -s -p "Enter password to unlock \"twitch_secret\": " PASS
                echo
            fi

            twitch_secret=$(cat twitch_secret | openssl enc -aes-256-cbc -pbkdf2 -d -pass pass:${PASS})
            twitcharr=(${twitch_secret})

            TWITCH_ID=${twitcharr[0]}
            TWITCH_SECRET=${twitcharr[1]}
            TWITCH_TOKEN=${twitcharr[2]}
            TWITCH_REFRESH_TOKEN=${twitcharr[3]}

        elif [ "$1" == "discord" ]; then
            if [ ! -f "discord_secret" ]; then
                make_discord_secret $@
            fi

            PASS=
            if [ -z ${PASS} ]; then
                read -s -p "Enter password to unlock \"discord_secret\": " PASS
                echo
            fi

            discord_secret=$(cat discord_secret | openssl enc -aes-256-cbc -pbkdf2 -d -pass pass:${PASS})
            discordarr=(${discord_secret})

            DISCORD_OWNER_ID=${discordarr[0]}
            BOT_EMOJI_GUILD=${discordarr[1]}
            DISCORD_TOKEN=${discordarr[2]}
        fi
    fi

    TWITCH_SUDO_ID=${TWITCH_SUDO_ID} TWITCH_TOKEN=${TWITCH_TOKEN} DISCORD_OWNER_ID=${DISCORD_OWNER_ID} BOT_EMOJI_GUILD=${BOT_EMOJI_GUILD} DISCORD_TOKEN=${DISCORD_TOKEN} \
     ${PYTHON} -m ${SCRIPT_MAIN} $@
}


##############################################

validate_script_assumptions $@

if [ "$#" -eq 1 ]; then
    if  [ "$1" == "help" ]; then
        print_usage
        exit 0

    elif [ "$1" == "test" ]; then
        run_test
        exit 0

    elif [ "$1" == "venv" ]; then
        run_venv
        exit 0

    elif [ "$1" == "format" ]; then
        run_format
        exit 0
    fi
fi

run_bot $@
