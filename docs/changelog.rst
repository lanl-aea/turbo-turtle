.. _changelog:

#########
Changelog
#########

*******************
v0.5.2 (unreleased)
*******************

New Features
============
- Draft assembly keyword block exporter in export subcommand (:issue:`38`, :merge:`36`). By `Kyle Brindley`_.

Internal Changes
================
- Separate the splines logic from the geometry Abaqus Python script and unit test it (:issue:`41`, :merge:`37`). By
  `Kyle Brindley`_.
- Unit test the coordinate generation for the axisymmetric cylinder subcommand (:issue:`50`, :merge:`39`). By `Kyle
  Brindley`_.

*******************
v0.5.1 (2023-11-09)
*******************

New Features
============
- Add a cylinder subcommand (:issue:`40`, :merge:`31`). By `Kyle Brindley`_.
- Add a ``merge`` subcommand to combine multiple Abaqus models together (:issue:`37`, :merge:`26`). By `Thomas Roberts`_
  and `Kyle Brindley`_.

Documentation
=============
- Update project description and scope (:issue:`36`, :merge:`32`). By `Kyle Brindley`_.
- Add the Abaqus Python parsers to the internal API (:issue:`47`, :merge:`34`). By `Kyle Brindley`_.

Internal Changes
================
- Replace duplicate Python 2/3 parsers with shared parsers compatible with both Abaqus Python and Python 3 (:issue:`4`,
  :merge:`28`). By `Kyle Brindley`_.
- Move the Python 3 wrapper functions to a dedicated module for re-use in SCons builders (:issue:`35`, :merge:`30`). By
  `Kyle Brindley`_.

Enhancements
============
- Add color map argument to the image subcommand (:issue:`45`, :merge:`35`). By `Kyle Brindley`_.

*******************
v0.5.0 (2023-11-07)
*******************

Breaking changes
================
- Update the ``export`` subcommand to allow for multiple orphan mesh files to be exported from the same Abaqus model and
  also allow for element type changes. This change removed the ``output_file`` command line argument in favor of naming
  orphan mesh files after the part names (:issue:`23`, :merge:`24`). By `Thomas Roberts`_.

New Features
============
- Add a ``geometry`` subcommand to draw 2D planar, 2D axisymmetric, or 3D bodies of revolution from a text file of x-y
  points (:issue:`16`, :merge:`25`). By `Thomas Roberts`_.

Bug fixes
=========
- Call the correct Abaqus Python script with the ``export`` subcommand (:issue:`25`, :merge:`22`). By `Kyle Brindley`_.

Documentation
=============
- Add a PDF build of the documentation (:issue:`31`, :merge:`20`). By `Kyle Brindley`_.
- Add a higher resolution PNG image for the Turbo Turtle logo (:issue:`32`, :merge:`23`). By `Thomas Roberts`_.

Internal Changes
================
- Reduce hardcoded duplication and use Python built-ins for coordinate handling in sphere subcommand implementation
  (:merge:`21`). By `Kyle Brindley`_ and `Matthew Fister`_.
- Run the pytests with the regression suite (:issue:`25`, :merge:`22`). By `Kyle Brindley`_.

Enhancements
============
- Fail with a non-zero exit code on Abaqus Python CLI errors (:issue:`25`, :merge:`22`). By `Kyle Brindley`_.

*******************
v0.4.3 (2023-10-24)
*******************

New Features
============
- Add a subcommand to mesh parts with a global seed (:issue:`30`, :merge:`19`). By `Kyle Brindley`_.
- Add a subcommand to export a part as an orphan mesh (:issue:`29`, :merge:`18`). By `Kyle Brindley`_.

Documentation
=============
- Add two of the system tests to the user manual as examples (:issue:`24`, :merge:`17`). By `Kyle Brindley`_.

*******************
v0.4.2 (2023-10-24)
*******************

New Features
============
- Add a subcommand to open the package's installed documentation (:issue:`15`, :merge:`11`). By `Kyle Brindley`_.
- Add a subcommand to create hollow sphere geometry (:issue:`8`, :merge:`13`). By `Kyle Brindley`_.
- Add a subcommand to create assembly image (:issue:`18`, :merge:`16`). By `Kyle Brindley`_.

Documentation
=============
- Package HTML documentation and man page (:issue:`11`, :merge:`8`). By `Kyle Brindley`_.

Internal Changes
================
- Consolidate in-repository system tests with the ``regression`` alias (:issue:`15`, :merge:`11`). By `Kyle Brindley`_.
- Reduce duplication in system test geometry creation (:issue:`17`, :merge:`12`). By `Kyle Brindley`_.
- Improved file handling for sphere and partition creation (:issue:`6`, :merge:`15`). By `Kyle Brindley`_.

Enhancements
============
- Create 2D axisymmetric part when provided a revolution angle of zero (:issue:`21`, :merge:`14`). By `Kyle Brindley`_.

*******************
v0.4.1 (2023-10-20)
*******************

Bug fixes
=========
- Fix partition abaqus CAE command construction (:issue:`9`, :merge:`7`). By `Kyle Brindley`_.

Internal Changes
================
- Move abaqus imports internal to the partition function to allow future re-use of the parser (:issue:`9`, :merge:`7`).
  By `Kyle Brindley`_.

*******************
v0.4.0 (2023-10-20)
*******************

Breaking changes
================
- Move existing behavior to the ``partition`` subcommand to make room for additional common utilities (:issue:`14`,
  :merge:`5`). By `Kyle Brindley`_.

*******************
v0.3.0 (2023-10-20)
*******************

Documentation
=============
- Gitlab-Pages hosted HTML documentation (:issue:`1`, ;merge:`4`). By `Kyle Brindley`_.

*******************
v0.2.0 (2023-10-19)
*******************

New Features
============
- Package with Conda. By `Kyle Brindley`_.

*******************
v0.1.0 (2023-10-19)
*******************

Breaking changes
================

New Features
============

Bug fixes
=========

Documentation
=============

Internal Changes
================

Enhancements
============
