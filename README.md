This repository holds the source for three volumes of the Conceptual Design Report for the next long-baseline experiment at Fermilab.
====

Guidance
---

The definitive source for guidance for CDR authors is available in the
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
Each volume is built separately.
Taking `volume-readme` as an example:

    pdflatex volume-readme
    bibtex volume-readme
    pdflatex volume-readme
    pdflatex volume-readme

To build one of the CDR volumes, substitute the volume name for "readme.”  Unless references change,
it is usually sufficient for subsequent builds to run only:

    pdflatex volume-readme
    pdflatex volume-readme

You may need the second run to get the paging and numbering correct.

The technical editors are responsible for producing a clean final
version of each volume with all the editing markup removed.  To compare
the “working” readme volume with its “clean” counterpart, first save the
pdf to a new name (to avoid overwriting), then compile the source again, 
replacing each `pdflatex volume-readme` command with this one:

    pdflatex "\def\isfinal{1} \input{volume-readme}"

This command can be used to produce a clean compilation of any volume.

Repository
---

It is strongly recommended that you use Git to make a clone of this
repository, to commit your changes to your clone and to push those
changes back to GitHub.  If you prefer to fork and make pull
requests that is also fine.

To get "push" access to this repository send your GitHub user name to
Brett (see contacts below).

General git procedure:

    cd lbn-cdr
    (edit)
    git pull
    git commit -a -m "Some commit message"
    git push

If adding a new file:

    git add the-new-file.tex
    git pull
    git commit -a -m "Some commit message"
    git push

Sometimes upstream changes occur that can affect what you are doing. Doing a `git pull` just before you commit is a good idea. When your local changes do not conflict with the changes in the upstream, a simple git pull will let you move forward.

If your local changes do conflict with the upstream changes, and git pull refuses to overwrite your changes, you can stash your changes away, perform a pull, and then unstash, like this:

    git stash
    git pull
    git stash pop

Now you should be able to do a `git push`.


## If you are unable to use Git

If you are unable to use Git, your contributions will still be accepted
but will lead to additional effort for the technical editors.  To
minimize that additional effort we ask that you **please** follow these steps:

* Start editing from the most recent
  [tagged release](https://github.com/LBNE/lbn-cdr/releases) or the
  specific release you may be requested to use.
* Unpack the release archive (.zip or .tar.gz) on your computer.
* Make your edits inside the directory/folder that is created.
* When you have finished, remove any generated files (eg, `volume-*.pdf`).
* Repack the directory (as `.zip` or `.tar.gz`).
* Upload this archive to the [document library](https://web.fnal.gov/project/LBNF/ReviewsAndAssessments/CD-1Preparation/Shared%20Documents/Forms/AllItems.aspx). (FNAL
[Services account](https://fermi.service-now.com/kb_view.do?sysparm_article=KB0010542) required)

Note: the technical editors must know the release version that you
started with.  This should be part of the unpacked directory/folder
name so do not strip it out.

If you are unable to edit in LaTeX, please talk to Anne (see contacts below).

Contacts
---

* Anne Heavey <aheavey@fnal.gov> 630-840-8039 (technical editor, content)

* Brett Viren <bv@bnl.gov> (technical editor, LaTeX machinery and repository)
