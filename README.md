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

It is strongly recommended that you use Git to make a clone of this
repository, to commit your changes to your clone and to push those
changes back to GitHub.  If you prefer to fork and make a pull
requests that is also fine.

To get "push" access to this repository send your GitHub user name to
Brett (see contacts below)

## If you are unable to use Git

If you are unable to use Git your contributions will still be accepted
but will lead to additional effort for the technical editors.  To
minimize that additional effort you **must** follow these steps:

* Start editing from the most recent
  [tagged release](https://github.com/LBNE/lbn-cdr/releases) or the
  specific release you may be requested to use.
* Unpack the release archive (.zip or .tar.gz) on your computer.
* Make your edits inside the directory/folder that is created.
* When you have finished, remove any generated files (eg, `volume-*.pdf`).
* Repack the directory (as `.zip` or `.tar.gz`).
* Send this archive to the contacts listed below.

Note: the technical editors must know the release version that you
started with.  This should be part of the unpacked directory/folder
name so do not strip it out.

Contacts
---

* Anne Heavey <aheavey@fnal.gov> (technical editor, content)

* Brett Viren <bv@bnl.gov> (technical editor, LaTeX machinery and repository)
