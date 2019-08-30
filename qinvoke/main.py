# -*- coding: utf-8 -*-
"""Entrypoint for the standalone qinvoke."""

from . import Program, version

program = Program(
    name='qinvoke',
    binary='qinv[oke]',
    binary_names=['qinvoke', 'qinv'],
    version=version,
)
