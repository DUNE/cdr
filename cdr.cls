% -*- latex -*-
%
% Document class for Conceptual Design Report

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cdr}[2015/02/02]
\LoadClass[12pt,letterpaper,twoside]{report}

% Set margins
\setlength{\oddsidemargin}{0.25in}
\setlength{\evensidemargin}{-0.25in}
\setlength{\topmargin}{-2.0cm} 
\setlength{\marginparwidth}{0in}
\setlength{\marginparsep}{0in}

% Required values and their setters
\newcommand\thevolumetitle{Conceptual Design Report}
\newcommand\thevolumesubtitle{}


% Provide finer-grained sectioning.
\newcounter{subsubsubsection}[subsubsection]
\def\subsubsubsectionmark#1{}
\def\thesubsubsubsection {\thesubsubsection
     .\arabic{subsubsubsection}}
\def\subsubsubsection{\@startsection
     {subsubsubsection}{4}{\z@} {-3.25ex plus -1
     ex minus -.2ex}{1.5ex plus .2ex}{\bf\normalsize\sffamily}}
\def\l@subsubsubsection{\@dottedtocline{4}{4.8em}
     {4.2em}}


% List of other packages required, add as needed.
% Some basic packages
\RequirePackage{color,soul}
\RequirePackage{graphicx}
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}

% Smart end-of-macro spacing
\RequirePackage{xspace}
% Must use units properly and consistently
\RequirePackage[detect-all=true,group-digits=true,group-separator={,},group-minimum-digits=4]{siunitx}

%%%FIXME: need to make this part respond to a class option
% show \label and other keys in the margin to make it easier for
% editors to add \ref and other references.
\RequirePackage[color]{showkeys}
% show line numbers
\RequirePackage[pagewise]{lineno}
\linenumbers

%% todonotes for "fixmes"
\RequirePackage[table]{xcolor}
\RequirePackage{todonotes}
\RequirePackage{menukeys}
\newcommand{\hlfix}[2]{\texthl{#1}\todo{#2}}
