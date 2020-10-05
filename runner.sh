#!/usr/bin/env bash
# Copyright © 2020 PixelExperience Project
#
# SPDX-License-Identifier: GPL-3.0
#
### Script to test and format our jsons

# Env vars
# TELEGRAM_TOKEN
# GH_PERSONAL_TOKEN
# GIT_PR_NUMBER
# BUILD_URL

ADMINS="@Hlcpereira @baalajimaestro @Shreejoy\_Dash @Rk585 @itsjoeoui @Hasaber8"
GIT_DIR="official_devices"
GIT_CMD="git -C ${GIT_DIR}"
COMMIT_MESSAGE="$(${GIT_CMD} log -1 --pretty=%B)"
COMMIT_SMALL_HASH="$(${GIT_CMD} rev-parse --short HEAD)"
COMMIT_HASH="$(${GIT_CMD} rev-parse --verify HEAD)"
COMMIT_URL="https://github.com/PixelExperience/official_devices/commit/$COMMIT_HASH"

function sendTG() {
    message="PixelExperience CI ([URL]($BUILD_URL)) ([$COMMIT_SMALL_HASH]($COMMIT_URL)): $1"
    curl -s "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendmessage" --data "text=$message&chat_id=-1001463677498&disable_web_page_preview=true&parse_mode=Markdown" > /dev/null
}

function commentPR() {
    message="$1"
    curl -s -X POST -d "{\"body\": \"$message\"}" -H "Authorization: token $GH_PERSONAL_TOKEN" "https://api.github.com/repos/PixelExperience/official_devices/issues/$GIT_PR_NUMBER/comments" > /dev/null
}

function approvePR() {
    curl -s -X POST -d "{\"commit_id\": \"${COMMIT_HASH}\", \"event\": \"APPROVE\"}" -H "Authorization: token $GH_PERSONAL_TOKEN" "https://api.github.com/repos/PixelExperience/official_devices/pulls/$GIT_PR_NUMBER/reviews" > /dev/null
}

function CheckCommit() {
    if [[ "$COMMIT_MESSAGE" =~ "[PIXEL-CI]" ]]; then
        if [[ -n "$GIT_PR_NUMBER" ]]; then
            commentPR "Please remove \"[PIXEL-CI]\" from your commit message."
            exit 0
        else
            echo "Commit already formatted, nothing to do."
            exit 0
        fi
    fi
}

function Validator() {
    python3 validator.py
    RESULT=$?
    if [ -n "$GIT_PR_NUMBER" ]; then
        if [ "$RESULT" -ne 0 ]; then
            message="JSON validation failed. Please check ${BUILD_URL} to find possible error."
            commentPR "$message"
            echo -e "$message"
        else
            message="JSON successfully validated"
            commentPR "$message"
            echo -e "$message"
        fi
    elif [ "$RESULT" -ne 0 ]; then
        sendTG "Someone has merged a failing file. Please check console to find possible error.\n\n${ADMINS}"
    else
        pushToGit
    fi
}

function pushToGit() {
    if [ -z "$GIT_PR_NUMBER" ] && [ -n "$(${GIT_CMD} status -s)" ]; then
        ${GIT_CMD} add --all
        ${GIT_CMD} commit -m "[PIXEL-CI]: Lint files"
        ${GIT_CMD} remote set-url origin "https://pixelexperiencebot:${GH_PERSONAL_TOKEN}@github.com/PixelExperience/official_devices.git"
        ${GIT_CMD} push origin master
        RESULT=$?
        if [ "$RESULT" -eq 0 ]; then
            message="JSON linted and pushed."
            echo -e "$message"
            sendTG "$message"
        else
            message="Failed to lint and push json."
            echo -e "$message"
            sendTG "$message"
            exit 1
        fi
    fi
}

checkCommit
Validator
