#!/usr/bin/env python3

import os
from flask import Flask
from .controllers.brief_controller import controller as c

app = Flask(__name__)


def keymaker(app, pathname='secret_key.raw'):
    pathname = os.path.join(app.instance_path, pathname)
    try:
        app.config['SECRET_KEY'] = open(pathname, 'rb').read()
    except IOError:
        parent_directory = os.path.dirname(pathname)
        if not os.path.isdir(parent_directory):
            os.system('mkdir -p {pathname}'.format(pathname=parent_directory))
        os.system(
            'head -c 24 /dev/urandom > {pathname}'.format(pathname=pathname)
        )
        keymaker(app)


keymaker(app)

app.register_blueprint(c)
