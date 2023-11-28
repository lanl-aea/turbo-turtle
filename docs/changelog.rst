.. _changelog:

#########
Changelog
#########

*******************
v0.8.1 (unreleased)
*******************

*******************
v0.8.0 (2023-11-28)
*******************

Breaking changes
================
- Exclude the opening/closing assembly scope keywords in the ``--assembly`` option of the ``export`` subcommand. More
  consistent with the orphan mesh export behavior, which excludes the part/instance scope keywords. Allows users to more
  easily modify the assembly scope without post-facto text file modification and with straight-forward ``*include``
  keywords.  (:issue:`90`, :merge:`73`). By `Kyle Brindley`_.

*******************
v0.7.2 (2023-11-28)
*******************

New Features
============
- Draft implementation of ``image`` subcommand with Cubit (:issue:`81`, :merge:`68`). By `Kyle Brindley`_.
- Draft implementation of ``export`` subcommand with Cubit (:issue:`79`, :issue:`88`, :merge:`69`, merge:`70`). By `Kyle
  Brindley`_.
- Add ability to export Genesis files from ``export`` subcommand with Cubit (:issue:`87`, :merge:`71`). By `Kyle
  Brindley`_.
- Draft implementation of ``merge`` subcommand with Cubit (:issue:`82`, merge:`72`). By `Kyle Brindley`_.

*******************
v0.7.1 (2023-11-27)
*******************

New Features
============
- Draft implementation of ``cylinder`` subcommand with Cubit (:issue:`63`, :merge:`61`). By `Kyle Brindley`_.
- Draft implementation of ``sphere`` subcommand with Cubit (:issue:`71`, :merge:`62`). By `Kyle Brindley`_.
- Draft implementation of ``partition`` subcommand with Cubit (:issue:`72`, :merge:`66`). By `Kyle Brindley`_.
- Draft implementation of ``mesh`` subcommand with Cubit (:issue:`78`, :merge:`67`). By `Kyle Brindley`_.

Bug fixes
=========
- Fix pass through of ``rtol`` and ``atol`` arguments in ``geometry`` subcommand (:merge:`60`). By `Kyle Brindley`_.
- Fix Cubit bin search and PYTHONPATH append behavior on MacOS (:merge:`63`). By `Kyle Brindley`_.

Internal Changes
================
- Separate the sphere arc point calculation from the abaqus python specific sphere module (:issue:`62`, :merge:`63`).
  By `Kyle Brindley`_.

Enhancements
============
- Regularize revolved solids in Cubit to remove the sketch seam in 360 degree revolutions (:merge:`63`). By `Kyle
  Brindley`_.

*******************
v0.7.0 (2023-11-20)
*******************

Breaking changes
================
- Partition refactor for reduction in duplicate code and interface updates to match implementation. Replaces
  ``--[xz]point`` with ``--[xz]vector``. Removes the various ``partition`` options in favor of user defined local xz
  plane from ``--center`` and ``--[xz]vector`` (:issue:`66`, :merge:`59`).  By `Kyle Brindley`_.

Enhancements
============
- Expose numpy tolerance to geometry subcommand interface to control the vertical/horizontal line check precision
  (:issue:`68`, :merge:`58`). By `Kyle Brindley`_.

*******************
v0.6.1 (2023-11-15)
*******************

New Features
============
- Draft implementation of ``geometry`` subcommand with Cubit (:issue:`44`, :merge:`50`). By `Kyle Brindley`_.

Bug fixes
=========
- Fix the ``--euclidean-distance`` option of the ``geometry`` subcommand (:issue:`67`, :merge:`56`). By `Kyle
  Brindley`_.

Documentation
=============
- Developer documentation for the mixed Python 2/3 modules and testing with both Python 3 and Abaqus Python
  (:issue:`51`, :merge:`48`). By `Kyle Brindley`_.

Internal Changes
================
- Move export subcommand Python 2/3 compatible functions to a Python 3 re-usable module and unit test in both Python 3
  and Abaqus Python (:issue:`51`, :merge:`48`). By `Kyle Brindley`_.
- Move merge subcommand Python 2/3 compatible functions to a Python 3 re-usable module and unit test in both Python 3
  and Abaqus Python (:issue:`53`, :merge:`49`). By `Kyle Brindley`_.
- Drive the system tests with pytest to reduce hardcoded duplication in test definitions between repository and
  conda-build recipe (:issue:`61`, :merge:`52`). By `Kyle Brindley`_.
- Move the element type substitution function to a common Python 2/3 compatible module (:issue:`59`, :merge:`55`). By
  `Kyle Brindley`_.

Enhancements
============
- Support MacOS Cubit execution (:issue:`64`, :merge:`53`). By `Kyle Brindley`_.

*******************
v0.6.0 (2023-11-13)
*******************

Breaking changes
================
- Consistent angle of revolution command line argument between subcommands: ``sphere`` now accepts
  ``--revolution-angle`` instead of ``--angle``. (:issue:`57`, :merge:`47`). By `Kyle Brindley`_.

*******************
v0.5.2 (2023-11-13)
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
- Add a version controlled CI and development environment (:issue:`13`, :merge:`38`). By `Kyle Brindley`_.
- Python 2/3 compatible 2D polar coordinate to 2D XY coordinate converter. By `Kyle Brindley`_.
- Move Abaqus Python geometry functions that are Python 3 compatible to a dedicated Python 2/3 compatible utilities
  module (:issue:`52`, :merge:`43`). By `Kyle Brindley`_.

Enhancements
============
- Raise an error if the provided Abaqus command is not found (:issue:`48`, :merge:`40`). By `Kyle Brindley`_.
- Better error reporting on STDERR when running Abaqus Python scripts (:issue:`52`, :merge:`43`). By `Kyle Brindley`_.
- Enforce positive floats in the CLI when they are expected (:merge:`44`). By `Kyle Brindley`_.

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
