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
\RequirePackage[table,usenames,dvipsnames]{xcolor}
\RequirePackage{todonotes}
\RequirePackage{menukeys}
\newcommand{\hlfix}[2]{\texthl{#1}\todo{#2}}


% Fancier tables
\RequirePackage{booktabs}
% from http://tex.stackexchange.com/questions/4811/make-first-row-of-table-all-bold:
\newcolumntype{$}{>{\global\let\currentrowstyle\relax}}
%$
\newcolumntype{^}{>{\currentrowstyle}}
\newcommand{\rowstyle}[1]{\gdef\currentrowstyle{#1}%
  #1\ignorespaces
}

\newcolumntype{L}{%
  >{\raggedright
    \bfseries
    \boldmath
  }l}%

\newcommand{\rowtitlestyle}{
  \rowcolor{Apricot}
  \rowstyle{\bfseries \boldmath} 
}

\newcommand{\colhline}{
  \arrayrulecolor{red}
  \specialrule{0.5pt}{0pt}{1pt}
  \arrayrulecolor{black}
}

\newcommand{\toprowrule}{
  \arrayrulecolor{red}
  \specialrule{1.2pt}{0pt}{1pt}
  \arrayrulecolor{black}
}

%%% originals come from booktabs
% \renewcommand{\toprule}{
%   \arrayrulecolor{red}
%   \specialrule{1.5pt}{2pt}{0pt}
%   \arrayrulecolor{black}
% }

% \renewcommand{\midrule}{
%   \arrayrulecolor{red}
%   \specialrule{1pt}{1pt}{1pt}
%   \arrayrulecolor{black}
% }

% \renewcommand{\bottomrule}{
%   \arrayrulecolor{red}
%   \specialrule{1.5pt}{0pt}{2pt}
%   \arrayrulecolor{black}
% }

% \newcommand{\cdrtablabel}{}

% \newenvironment{cdrtable}[2]{%
%   \gdef{\cdrtablabel}{#1}%
%   \begin{table}[hbtp]%
%     \centering%
%     \begin{tabular}{#2}%
% }{%      
%     \bottomrule%
%     \end{tabular}%
%     \caption{caption}%
%     \label{\cdrtablabel}%
%   \end{table}%
% }

\newcommand{\cdrtablabel}{}% stores the label
\newcommand{\cdrtabcaption}{}% stores the caption
\newcommand{\cdrtabcaptionshort}{}% stores an optional short caption
\newenvironment{cdrtable}[4][]
{
  \if\relax\detokenize{#1}\relax
  \gdef\cdrtabcaptionshort{\relax}
  \else
  \gdef\cdrtabcaptionshort{#1}
  \fi

  \gdef\cdrtablabel{#3}
  \gdef\cdrtabcaption{#4}

  \begin{table}[hbtp]
    \centering
      \caption[\cdrtabcaptionshort]{\cdrtabcaption}
      \begin{tabular}{#2}
        \toprule
        \rowtitlestyle
}
{
        \bottomrule
      \end{tabular}
      \label{tab:\cdrtablabel}
  \end{table}
}

\newcommand{\cdrfiglabel}{}% stores the label
\newcommand{\cdrfigcaption}{}% stores the caption
\newcommand{\cdrfigcaptionshort}{}% stores an optional short caption
\newenvironment{cdrfigure}[3][]
{
  \if\relax\detokenize{#1}\relax
  \gdef\cdrfigcaptionshort{\relax}
  \else
  \gdef\cdrfigcaptionshort{#1}
  \fi

  \gdef\cdrfiglabel{#2}
  \gdef\cdrfigcaption{#3}

  \begin{figure}[hbtp]
    \centering
}
{
      \caption[\cdrfigcaptionshort]{\cdrfigcaption}
      \label{fig:\cdrfiglabel}
  \end{figure}
}
