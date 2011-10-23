#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#     Original idea from : 
#       Maxime Biais <maxime@biais.org>
#     but has been nearly all rewritten since...
#    Marc Poulhiès <marc.poulhies@epfl.ch>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: latex2twiki.py,v 1.2 2005/07/27 12:40:53 poulhies Exp $

import sys, re

bullet_level=0
bdoc = None
end_line = 1

verbatim_mode = 0

def dummy():
    pass

def inc_bullet():
	global bullet_level
	bullet_level += 1

def dec_bullet():
	global bullet_level
	bullet_level -= 1

def start_doc():
	global bdoc;
	bdoc = 1

def do_not_el():
	global end_line
	end_line = None

def do_el():
	global end_line;
	end_line = 1

def decide_el():
	global end_line
	if bullet_level == 0:
		return "\n"
	else:
		return " "

def start_verbatim():
	global verbatim_mode
	verbatim_mode = 1

def end_verbatim():
	global verbatim_mode
	verbatim_mode = 0
	
conv_table = { '>':'&gt;',
			   '<':'&lt;'}

def translate_to_html(char):
	global verbatim_mode
	global conv_table
	if verbatim_mode == 0:
		return conv_table[char]
	else:
		return char

def header(i):
	offset = 1
	return r"---"+r'+' * (i+offset) + r" \1"

NONE = "__@NONE@__"

tr_list2 = [
	(r">", (lambda: translate_to_html('>')), dummy),
	(r"<", (lambda: translate_to_html('<')), dummy),
	(r"\\footnotesize", None, dummy),
	(r"\\small", None, dummy),
	(r"\\begin\{document}", None, start_doc),
	(r"\\\\$", (lambda : "\n\n"), dummy),
	(r"\\\$", (lambda : "$"), dummy),
	(r"\\emph{(.*?)}", (lambda : r"_\1_ "), dummy),
	(r"\\textit{(.*?)}", (lambda :r"_\1_ "), dummy),
	(r"\\texttt{(.*?)}", (lambda : r"=\1= "), dummy),
	(r"\\textbf{(.*?)}", (lambda : r"*\1* "), dummy),
	(r"\\begin{verbatim}", (lambda : "<verbatim>"), start_verbatim),
	(r"\\end{verbatim}", (lambda : "</verbatim>"), end_verbatim),
	(r"\\begin{itemize}", (lambda : "\n"), inc_bullet),
	(r"\\end{itemize}", None, dec_bullet),
	(r"\\item (.*?)", (lambda : r"\n" + (r"   " * bullet_level) + r"* \1"), dummy),
	(r"\\begin{.*?}", None, dummy),
	(r"\\end{.*?}", None, dummy),
	(r"``(.*?)''", (lambda :r'"\1"'), dummy),
	(r"\\subsubsection{(.*?)}", (lambda : header(3)), dummy),
	(r"\\subsection{(.*?)}", (lambda : header(2)), dummy),
	(r"\\section{(.*?)}", (lambda : header(1)), dummy),
	(r"\\_", (lambda :"_"), dummy),
	(r"\\tableofcontents",None, dummy),
	(r"\\null",None, dummy),
	(r"\\newpage",None, dummy),
	(r"\\thispagestyle{.*?}", None, dummy),
	(r"\\maketitle", None, dummy),
	(r"\n$", decide_el, dummy),
	(r"[^\\]?\{", None, dummy),
	(r"[^\\]?\}", None, dummy)
    ]

in_stream  = sys.stdin;
out_stream = sys.stdout

for i in in_stream.readlines():
	mystr = i

	for reg in tr_list2:
		p = re.compile(reg[0])

		if p.search(mystr):
			reg[2]()
		if reg[1] != None:
			mystr = p.sub(reg[1](), mystr)
		else:
			mystr = p.sub("", mystr)
			
	if bdoc != None:
		print >> out_stream, mystr,
