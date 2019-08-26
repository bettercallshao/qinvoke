import inspect
import io
import os
import re
import webbrowser
from contextlib import redirect_stdout

from flask import Flask, render_template, request
from invoke import Program as Base

ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


class Program(Base):
    def serve(self):
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

        app = Flask('qinvoke', root_path=os.path.dirname(__file__))

        @app.route('/')
        def home():
            return render_template('home.html', tasks=tasks)

        @app.route('/<task>')
        def task(task):
            try:
                return render_template(
                    'task.html',
                    task=tasks_map[task],
                    out='')
            except KeyError:
                return 400, 'no such task {}!'.format(task)

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
                            value=request.form.get(arg['name'], '')
                        ) for arg in tasks_map[task]['args']
                    ]
                )

                argv = ['qinvoke', task] + [
                    word
                    for arg in task_dict['args']
                    for word in _list_from_arg(arg)
                ]

                f = io.StringIO()
                with redirect_stdout(f):
                    self.run(argv)
                return render_template(
                    'task.html',
                    task=task_dict,
                    cmd=' '.join(argv),
                    out=ansi_escape.sub('', f.getvalue())
                )

            except KeyError:
                return 400, 'no such task {}!'.format(task)

        port = os.getenv('PORT', '8800')
        webbrowser.open_new_tab('http://localhost:{}'.format(port))
        app.run(port=port)