#!/bin/sh
if type pdflatex; then
    cd build && pdflatex -interaction=nonstopmode engel.tex
    cp engel.pdf html/
else
    echo "pdflatx not found. Skipping PDF build"
fi
