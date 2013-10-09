#! /usr/bin/python
from __future__ import print_function
import random
import string

if __name__ == '__main__':
    secret_key = "".join([random.choice(string.ascii_letters) for i in range(50)])
    print('SECRET_KEY: "{0}"'.format(secret_key))
