import os

if __name__ == "__main__":
    travis_tag = os.environ.get('TRAVIS_TAG')
    if travis_tag:
        with open('flask_app/__version__.py', 'w') as f:
            print(f'__version__ = "{travis_tag}"', file=f)
