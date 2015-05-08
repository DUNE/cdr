#!/usr/bin/env python

import os

top='.'

def configure(cfg):
    cfg.find_program('dune-params', var='DUNEPARAMS')
    cfg.load('tex')
    pass


def build(bld):

    paramsxls = bld.path.find_resource('data/parameters.xls')
    paramspy = bld.path.find_resource('python/parameters.py')
    os.environ['PYTHONPATH'] = paramspy.parent.abspath()


    # generate files from parameter templates
    for tmpl in bld.path.ant_glob('**/templates/*.tex.j2'):
        tmp = tmpl.parent.parent
        gen_dir = tmp.make_node('generated')
        target = gen_dir.make_node(str(tmpl.change_ext('.tex', '.tex.j2')))
        rule='${DUNEPARAMS} render -f parameters.filter -t ${SRC[1].abspath()} -o ${TGT[0].abspath()} ${SRC[0].abspath()}'
        bld(rule=rule,
            source = [paramsxls, tmpl, paramspy], # last ones just for dependencies
            target = target, 
            shell = True)


    for tex in bld.path.ant_glob('*.tex', excl=['*-indiv.tex']):
        # do latex'ing
        bld(features='tex',
            type='pdflatex',
            source = tex,
            outs = 'pdf',
            )
        bld.install_files('${PREFIX}',tex.change_ext('.pdf', '.tex'))
    return


