#!/usr/bin/env bash
# Script to exchange translation files between repo and Transifex via Travis CI.
# It relies on $TXTOKEN and $GHTOKEN being set as env vars for the given repo
# in Travis CI.
import os
from subprocess import run
import sys

def git_setup():
    run('git config --global user.email "bot+travis@transifex.com"')
    run('git config --global user.name "Transifex Bot (Travis CI)"')


def commit_translation_files():
    print("checkout")
    run('git checkout -b transifex')
    print("add")
    run('git add source/_locale/*.po')
    print("commit")
    run('git commit -m "Translation update from Transifex" -m "[ci skip]"')


def push_translation_files():
    print("git remote")
    run('git remote add origin-travis https://{GHTOKEN}@github.com/{TRAVIS_REPO_SLUG}.git > /dev/null 2>&1'.format(
        GHTOKEN=os.environ['GHTOKEN'], TRAVIS_REPO_SLUG=os.environ['TRAVIS_REPO_SLUG'])
    )
    print("git push")
    run('git push -f --set-upstream origin-travis transifex')


def tx_init():
    with open('~/.transifexrc', 'w') as d:
        d.write(
            "[https://www.transifex.com]"
            "\nhostname = https://www.transifex.com"
            "\nusername = api"
            "\npassword = {TXTOKEN}"
            "\ntoken =".format(TXTOKEN=os.environ['TXTOKEN'])
        )


def update_translations():
    run(
        "make gettext rm .tx/config sphinx-intl create-txconfig sphinx-intl update-txconfig-resources "
        "--transifex-project-name tqdyr"
    )


def tx_push():
    if (os.environ['TRAVIS_BRANCH'] == os.environ['TX_BRANCH']) and (
            not os.environ['TRAVIS_JOB_NUMBER'].endswith(".1")):
        tx_init()
        update_translations()
        run('tx push --source --no-interactive')


def tx_pull():
    if (os.environ['TRAVIS_BRANCH'] == os.environ['TX_BRANCH']) and (
            not os.environ['TRAVIS_JOB_NUMBER'].endswith(".1")):
        tx_init()
        run('tx pull --all --force')
        fresh_translations = run('git diff-index --name-only HEAD --')
        if fresh_translations:
            print("pushing")
            git_setup()
            commit_translation_files()
            push_translation_files()


if __name__ == '__main__':
    arg = sys.argv[1]
if arg == 'push':
    tx_push()
elif arg == 'pull':
    tx_pull()
