import os
import subprocess

if __name__ == "__main__":
    travis_tag = os.environ.get('TRAVIS_TAG')
    if travis_tag:
        version = travis_tag
    else:
        version = subprocess.check_output('git describe --tags', shell=True, encoding='utf-8').strip()

    with open('flask_app/__version__.py', 'w') as f:
        print(f'__version__ = "{version}"', file=f)

    with open('webapp/app/utils/ui_version.js', 'w') as f:
        print(f'export default "{version}";', file=f)
