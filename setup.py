from setuptools import setup

from qinvoke import version

with open('README.md') as f:
    long_description = f.read()

setup(
    name='qinvoke',
    version=version,
    description='A web gui for running invoke commands.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shaoqing Tan',
    author_email='tansq7@gmail.com',
    url='https://github.com/hydiant/qinvoke',
    license='MIT',
    packages=['qinvoke'],
    data_files=[
        (
            'templates', [
                'qinvoke/templates/{}.html'.format(n)
                for n in ['base', 'home', 'task']
            ]
        )
    ],
    entry_points={
        'console_scripts': [
            'qinvoke = qinvoke.main:program.run',
            'qinv = qinvoke.main:program.run',
        ]
    },
    install_requires=[
        'flask',
        'invoke',
    ],
    include_package_data=True,
    zip_safe=False,
)
