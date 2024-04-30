.. _changelog:

#########
Changelog
#########

********************
v0.12.0 (unreleased)
********************

Breaking changes
================
- Remove the deprecated CLI builders prefixed with ``turbo_turtle_``. Replaced by more general builders in :ref:`0.11.0`
  (:issue:`127`, :merge:`156`). By `Kyle Brindley`_.
- Remove the deprecated ``--cubit`` CLI option. Replaced by ``--backend`` in :ref:`0.11.0` (:issue:`130`, :merge:`157`).
  By `Kyle Brindley`_.

********************
v0.11.3 (2024-04-29)
********************

New Features
============
- Expose the ``geometry-xyplot`` matplotlib figure generation function to the public API (:issue:`148`, :merge:`139`).
  By `Kyle Brindley`_.
- Add a ``fetch`` subcommand to retrieve user manual and tutorial files (:issue:`145`, :merge:`143`). By `Kyle
  Brindley`_.
- Lazy import of submodules (:merge:`152`). By `Kyle Brindley`_.

Bug fixes
=========
- Call to the ``main`` function in ``mesh_module.py`` needs to be in the ``except`` statement so the GUI-wrapper does
  not execute ``main`` (:issue:`165`, :merge:`154`). By `Thomas Roberts`_.
- Match the coordinate transformations of ``geometry`` subcommand in the ``geometry-xyplot`` subcommand (:issue:`156`,
  :merge:`134`). By `Kyle Brindley`_.
- Python 3.8 compatible type annotations (:issue:`162`, :merge:`149`). By `Kyle Brindley`_.

Documentation
=============
- Add a bibiliography and references section (:issue:`139`, :merge:`136`). By `Kyle Brindley`_.
- Update SCons example in user manual to build both available backends: Abaqus and Cubit (:issue:`158`, :merge:`142`).
  By `Kyle Brindley`_.
- Update man page and documentation to include full subcommand and API (:merge:`148`). By `Kyle Brindley`_.
- Update the GUI documentation describing how to run and get more information about a plug-in (:issue:`149`,
  :merge:`131`). By `Thomas Roberts`_.

Internal Changes
================
- Work-in-progress support for Abaqus CAE GUI meshing capability (:issue:`153`, :merge:`140`). By `Thomas Roberts`_.
- Work-in-progress support for Abaqus CAE GUI sphere capability (:issue:`152`, :merge:`133`). By `Thomas Roberts`_.
- Improved unit tests for the CLI builders (:issue:`151`, :merge:`135`). By `Kyle Brindley`_.
- Work-in-progress support for Abaqus CAE GUI cylinder capability (:issue:`150`, :merge:`132`). By `Thomas Roberts`_.
- Add the user manual SCons demo to the system tests (:issue:`144`, :merge:`141`). By `Kyle Brindley`_.
- Use the full Abaqus session object namespace (:issue:`140`, :merge:`144`). By `Kyle Brindley`_.
- Add PEP-8 partial style guide checks to CI jobs (:issue:`160`, :merge:`145`). By `Kyle Brindley`_.
- Add flake8 configuration file for easier consistency between developer checks and CI checks (:issue:`161`,
  :merge:`146`). By `Kyle Brindley`_.
- Use SCons task for flake8 style guide checks (:merge:`147`). By `Kyle Brindley`_.
- Add a draft SCons task for project profiling (:merge:`150`). By `Kyle Brindley`_.
- Add lazy loader package to CI environment (:issue:`163`, :merge:`151`). By `Kyle Brindley`_.
- Add partial submodule imports to cProfile SCons task (:merge:`153`). By `Kyle Brindley`_.

Enhancements
============
- Add an option to use equally scaled X and Y axes in ``geometry-xyplot`` subcommand (:issue:`157`, :merge:`138`). By
  `Kyle Brindley`_.

********************
v0.11.2 (2024-03-29)
********************

Documentation
=============
- Use built-in Abaqus/CAE plug-in documentation features to display GUI plug-in help messages and link to documentation
  in the Abaqus/CAE GUI (:issue:`142`, :merge:`129`). By `Thomas Roberts`_.
- Improve Abaqus geometry error message (:merge:`124`). By `Kyle Brindley`_.

Internal Changes
================
- Reduce duplicate logic in geometry and cylinder subcommand implementations (:issue:`123`, :merge:`126`). By `Kyle
  Brindley`_.
- Make the Abaqus python package importable and change the GUI behavior to be a plug-in rather than direct execution on
  a python module (:issue:`137`, :merge:`127`). By `Thomas Roberts`_.
- Work-in-progress support for Abaqus CAE GUI geometry capability (:issue:`138`, :merge:`128`). By `Thomas Roberts`_.

Enhancements
============
- Implement the numpy tolerance checks for the Cubit geometry and geometery-xyplot subcommands (:issue:`123`,
  :merge:`126`). By `Kyle Brindley`_.
- Add an option to add vertex index annotations to the geometery-xyplot subcommand (:issue:`147`, :merge:`130`). By
  `Kyle Brindley`_.

********************
v0.11.1 (2024-03-01)
********************

Internal Changes
================
- Work-in-progress support for Abaqus CAE GUI partitioning capability (:issue:`133`, :merge:`122`). By `Thomas Roberts`_.
- Dedicated Cubit imprint and merge function (:issue:`76`, :merge:`110`). By `Kyle Brindley`_.
- Dedicated Cubit local coordinate primary plane webcutting function (:issue:`77`, :merge:`111`). By `Kyle Brindley`_.
- Dedicated Cubit pyramidal volume creation and partitioning functions (:issue:`131`, :merge:`112`). By `Kyle
  Brindley`_.
- Unit test the pass through Abaqus Python CLI construction (:issue:`58`, :merge:`113`). By `Kyle Brindley`_.
- Unit test the pass through Cubit Python API unpacking (:issue:`91`, :merge:`114`). By `Kyle Brindley`_.
- Unit test the default argument values in the subcommand argparse parsers (:issue:`55`, :merge:`115`). By `Kyle
  Brindley`_.
- Report unit test coverage in Gitlab-CI pipelines (:merge:`116`). By `Kyle Brindley`_.
- Refact and unit test the coordinate modification performed by geometry subcommand (:issue:`102`, :merge:`117`). By
  `Kyle Brindley`_.
- Add a missing unit test for the Abaqus Python CLI merge construction (:merge:`118`). By `Kyle Brindley`_.
- Unit tests for Cubit curve and surface creation from coordinates (:merge:`119`, :merge:`120`). By `Kyle Brindley`_.
- Build coverage artifacts in build directory (:merge:`121`). By `Kyle Brindley`_.
- Fix the docs and print abaqus module unit tests (:issue:`136`, :merge:`123`). By `Kyle Brindley`_.

Enhancements
============
- Enforce positive floats and integers for CLI options requiring a positive value (:issue:`55`, :merge:`115`). By `Kyle
  Brindley`_.

.. _0.11.0:

********************
v0.11.0 (2024-02-15)
********************

Breaking changes
================
- Replace the ``--cubit`` flag with a ``--backend`` option that defaults to Abaqus (:issue:`126`, :merge:`108`). By
  `Kyle Brindley`_.

New Features
============
- SCons CLI builders for every subcommand (:issue:`125`, :merge:`107`). By `Kyle Brindley`_.

Documentation
=============
- Consistent required option formatting in CLI usage (:issue:`124`, :merge:`105`). By `Kyle Brindley`_.

Internal Changes
================
- Add a draft, general purpose SCons builder. Considered draft implementations in the *internal* interface until final
  design interface and behavior are stabilized(:merge:`106`). By `Kyle Brindley`_.

Enhancements
============
- Allow users to turn off vertex markers in the ``geometry-xyplot`` subcommand output (:merge:`104`). By `Kyle Brindley`_.

********************
v0.10.2 (2024-02-14)
********************

New Features
============
- ``geometry-xyplot`` subcommand to plot lines-and-splines coordinate breaks (:issue:`122`, :merge:`102`).
  By `Kyle Brindley`_.

Bug fixes
=========
- Only partition the requested part name(s) in the Cubit ``partition`` implementation (:issue:`110`, :merge:`88`). By
  `Kyle Brindley`_.

Internal Changes
================
- Remove duplication in CI environment creation logic (:issue:`121`, :merge:`101`). By `Kyle Brindley`_.

Enhancements
============
- Partition multiple parts found in a single input file in the ``partition`` subcommand (:issue:`110`, :merge:`88`). By
  `Thomas Roberts`_ and `Kyle Brindley`_.

********************
v0.10.1 (2024-02-12)
********************

Bug fixes
=========
- Pass the color map option from the image subcommand Python 3 CLI to the Abaqus Python CLI (:issue:`120`,
  :merge:`100`). By `Kyle Brindley`_.

Documentation
=============
- Document the re-git manual tag release step (:issue:`117`, :merge:`96`). By `Kyle Brindley`_.
- Add re-git badges (:issue:`116`, :merge:`95`). By `Kyle Brindley`_.

Internal Changes
================
- Update CLI description for the ``image`` subcommand to be consistent with changes from :issue:`92` (:issue:`111`,
  :merge:`89`). By `Thomas Roberts`_.
- Duplicate vertices Python 3 unit tests in Abaqus Python 2 (:issue:`60`, :merge:`90`). By `Kyle Brindley`_.
- Add boa to the CI environment for faster mambabuild packaging (:issue:`118`, :merge:`97`). By `Kyle Brindley`_.
- Build the package with boa and run the fast-test and conda-build jobs in parallel (:issue:`119`, :merge:`99`). By
  `Kyle Brindley`_.

Enhancements
============
- Allow for assembly image generation by optionally excluding ``--part-name`` when using the ``image`` subcommand
  (:issue:`92`, :merge:`74`). By `Thomas Roberts`_.

********************
v0.10.0 (2024-01-24)
********************

Enhancements
============
- Improved Abaqus partitioning algorithm for handling pre-existing features (:issue:`70`, :merge:`86`). By `Kyle
  Brindley`_ and `Thomas Roberts`_.

*******************
v0.9.1 (2024-01-24)
*******************

Bug fixes
=========
- Fix a part name variable in the ``image`` subcommand Abaqus implementation (:issue:`105`, :merge:`82`). By `Kyle
  Brindley`_.

Documentation
=============
- Match user manual ``export`` subcommand options to implementation (:issue:`109`, :merge:`84`). By `Kyle Brindley`_.

Internal Changes
================
- Draft SCons extensions for subcommand builders. Considered draft implementations in the *internal* interface until
  final design interface and behavior are stabilized (:issue:`103`, :merge:`80`). By `Kyle Brindley`_.
- Updated cubit partition scheme to identify surfaces relative to local coordinate system and principal planes
  (:issue:`104`, :merge:`81`). By `Paula Rutherford`_.
- Expose the SCons builders as part of the (future) public API (:issue:`106`, :merge:`83`). By `Kyle Brindley`_.

Enhancements
============
- Add capability for a solid sphere geometry generation (:issue:`97`, :merge:`79`). By `Paula Rutherford`_.

*******************
v0.9.0 (2024-01-02)
*******************

Breaking changes
================
- Cylinder subcommand generates a cylinder with a centroid on the global coordinate system origin for consistency with
  sphere subcommand (:issue:`93`, :merge:`76`). By `Kyle Brindley`_.
- Replace sphere subcommand center movement argument with a vertical offset movement for consistency with cylinder
  subcommand and the Abaqus axisymmetric compatible geometry generation design (:issue:`94`, :merge:`77`). By `Kyle
  Brindley`_.

Documentation
=============
- Clarify which ``image`` subcommand options are unused by Cubit implementation (:issue:`85`, :merge:`75`). By `Kyle
  Brindley`_.

Enhancements
============
- Add a vertical offset option to the cylinder subcommand (:issue:`93`, :merge:`76`). By `Kyle Brindley`_.
- Add a vertical offset option to the geometry subcommand (:issue:`95`, :merge:`78`). By `Kyle Brindley`_.

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
