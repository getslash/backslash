#! env /usr/bin/python3.6
import logging
import os
import subprocess
import sys


if __name__ == "__main__":
    logging.basicConfig(level='DEBUG', stream=sys.stderr)

    username = os.environ.get('DOCKER_USERNAME')
    password = os.environ.get('DOCKER_PASSWORD')
    travis_branch = os.environ.get('TRAVIS_BRANCH')
    travis_tag = os.environ.get('TRAVIS_TAG')
    repo = 'getslash/backslash'

    if travis_tag:
        tag = travis_tag
    elif travis_branch == 'master':
        tag = 'latest'
    elif travis_branch == 'develop':
        tag = 'unstable'
    else:
        tag = None

    if not username or not password:
        sys.exit('No docker username/password provided')

    logging.info('Logging in to docker')
    subprocess.check_call(f'docker login -u {username} -p {password}', shell=True)

    if tag is not None:
        logging.info('Pushing image')
        subprocess.check_call(f'docker tag getslash/backslash getslash/backslash:{tag}', shell=True)
        subprocess.check_call(f'docker push getslash/backslash:{tag}', shell=True)
    else:
        logging.info('Tag is empty. Not pushing anything to docker')
