# -*- coding: utf-8 -*-
"""Class to extend invoke."""

import io
import os
import re
import sys
import inspect
import contextlib
import webbrowser

from flask import Flask, request, render_template
from invoke import Program as Base

ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


@contextlib.contextmanager
def _redirect_stdout():
    original = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = original


class Program(Base):
    """Class to extend invoke."""

    def serve(self):
        """Start the qinvoke webserver and activate browser."""
        self.create_config()
        self.parse_core(None)
        self.parse_collection()
        self.parse_tasks()

        tasks = [{
            'name': c.name,
            'doc': inspect.getdoc(self.collection[c.name]),
            'args': [{
                'name': f.name,
                'doc': f.help,
                'value': f.default,
                'is_list': f.kind == list,
                } for f in c.flags.values()],
            } for c in self.parser.contexts.values()
        ]
        tasks_map = {t['name']: t for t in tasks}

        with _redirect_stdout() as f:
            self.print_version()
            title = f.getvalue().strip()
        app = Flask(title, root_path=os.path.dirname(__file__))

        @app.route('/')
        def home():
            return render_template('home.html', title=title, tasks=tasks)

        @app.route('/<task>')
        def task(task):
            try:
                return render_template(
                    'task.html',
                    title=title,
                    task=tasks_map[task],
                    out='')
            except KeyError:
                return 400, 'no such task {0}!'.format(task)

        @app.route('/<task>', methods=['post'])
        def run(task):
            try:
                def _list_from_arg(arg):
                    name = arg['name']
                    value = arg['value']
                    if arg['is_list']:
                        return [
                            word
                            for line in value.split('\n') if line.strip()
                            for word in ['--' + name, line.strip()]
                        ]
                    else:
                        return ['--' + name, value] if value else []

                task_dict = dict(
                    tasks_map[task],
                    args=[
                        dict(
                            arg,
                            value=request.form.get(arg['name'], ''),
                        ) for arg in tasks_map[task]['args']
                    ],
                )

                argv = ['qinvoke', task] + [
                    word
                    for arg in task_dict['args']
                    for word in _list_from_arg(arg)
                ]

                with _redirect_stdout() as f:
                    self.run(argv)
                    return render_template(
                        'task.html',
                        title=title,
                        task=task_dict,
                        cmd=' '.join(argv),
                        out=ansi_escape.sub('', f.getvalue()),
                    )

            except KeyError:
                return 400, 'no such task {0}!'.format(task)

        port = os.getenv('PORT', '8800')
        webbrowser.open_new_tab('http://localhost:{0}'.format(port))
        app.run(host='0.0.0.0', port=port) # noqa
