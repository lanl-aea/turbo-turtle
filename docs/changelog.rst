.. _changelog:

#########
Changelog
#########

*******************
v0.4.4 (unreleased)
*******************

Bug fixes
=========
- Call the correct Abaqus Python script with the ``export`` subcommand (:issue:`25`, :merge:`22`). By `Kyle Brindley`_.

Documentation
=============
- Add a PDF build of the documentation (:issue:`31`, :merge:`20`). By `Kyle Brindley`_.

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
