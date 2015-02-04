This is the Conceptual Design Report for the next long-baseline experiment at Fermilab.
====

Guidance
---

The definitive source for guidance for CDR authors is availble in the
document:

  volume-readme.pdf
  [volume-readme.tex](volume-readme.tex)

This document is written following its own guidance so its source also
serves as an example.

Getting started
---

Clone the repository:

    git clone https://github.com/LBNE/lbn-cdr.git
    cd lbn-cdr/

To build the documents you need `pdflatex` and `bibtex`.  
The CDR is comprised of a number of stand-alone volumes (the LaTeX
ones are in this repository).
Each volume is built separately
Taking the guidance volume as an example:

    pdflatex volume-readme
    bibtex volume-readme
    pdflatex volume-readme
    pdflatex volume-readme

Substitute "readme" for other volume names.  Unless refernces change
it is usually sufficient for subsequent builds to run only:

    pdflatex volume-readme

Repository
---

To get "push" access to this repository send your GitHub user name to
the contacts:

    Brett Viren bv@bnl.gov
    Anne Heavey aheavey@fnal.gov

You may also clone/fork this repository and issue pull-requests.
