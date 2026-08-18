"""Helpers compartidos por los módulos de celdas del informe."""

from __future__ import annotations

import nbformat as nbf


def md(texto: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(texto.strip())


def code(texto: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(texto.strip())
