.. -*- coding: utf-8; mode: rst; -*-

.. reStructuredText Markup Specification https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
   
.. For the Python documentation, 
   this convention is used which you may follow:
    • # with overline, for parts
    • * with overline, for chapters
    • =, for sections
    • -, for subsections
    • ^, for subsubsections
    • ", for paragraphs


Style Guide
===========

For the Python code, follow
`pep-0008 <https://www.python.org/dev/peps/pep-0008/>`_.


Naming Convensions
------------------

Condensed naming convensions from
`pep-0008 Naming Conventions <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_:

* **Packages** should have short, all-lowercase names,
  although the use of underscores is discouraged.

* **Modules** should have short, all-lowercase names.
  Underscores can be used in the module name
  if it improves readability. 

* **Class** names should normally use the CapWords convention.
  
  Note:
    When using acronyms in CapWords, capitalize all the letters of the acronym.
    Thus `HTTPServerError` is better than `HttpServerError`.


* **Function** names should be lowercase,
  with words separated by underscores as necessary to improve readability.

* **Variable** names should be lowercase, with
  words separated by underscores as necessary to improve readability.

* **Constants** names should be all capital letters with underscores separating words.
  Constants are usually defined on a module level. 

  
Docstring guide
---------------

For Doc strings, follow the
`numpy docstring guide <https://numpydoc.readthedocs.io/en/latest/format.html>`_
