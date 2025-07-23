.. _changelog:

#########
Changelog
#########

*******************
v1.3.0 (unreleased)
*******************

*******************
v1.2.7 (2025-07-23)
*******************

Documentation
=============
- Landing page re-design for ease of access and reduced clutter. By `Kyle Brindley`_.

Internal Changes
================
- Match Conda-forge recipe more closely for easier diffs during package recipe updates. By `Kyle Brindley`_.
- Use full default Flake8 checks. By `Kyle Brindley`_.

Bug fixes
=========
- Fix element type assignment in Cubit Python backend implementation of the export subcommand. By `Kyle Brindley`_.
- Fix conversion of exception messages to exit error messages. Previously used an exception attribute that was
  deprecated in Python 2.6, so the bug was a Python 2/3 incompatibility when Abaqus 2024 finally introduced Python 3
  (:issue:`256`, :merge:`259`). By `Kyle Brindley`_.

*******************
v1.2.6 (2025-05-21)
*******************

Documentation
=============
- Add PyPI shields to README and HTML documentation (:issue:`255`). By `Kyle Brindley`_.

Internal Changes
================
- Cleanup internal conda-build deployment logic. By `Kyle Brindley`_.

*******************
v1.2.5 (2025-05-21)
*******************

Internal Changes
================
- Automated PyPI deploy workflow from GitHub.com. By `Kyle Brindley`_.

*******************
v1.2.4 (2025-05-21)
*******************

Documentation
=============
- Match short descriptions across PyPI and conda packages. By `Kyle Brindley`_.

*******************
v1.2.3 (2025-05-21)
*******************

Documentation
=============
- Fix README targets checked by twine/PyPi during upload. By `Kyle Brindley`_.

*******************
v1.2.2 (2025-05-21)
*******************

Internal Changes
================
- Update URLs for external package builds to use the external GitHub.com URLs. By `Kyle Brindley`_.

*******************
v1.2.1 (2025-05-21)
*******************

Internal Changes
================
- Fix Gitlab-CI pip build artifacts. By `Kyle Brindley`_.

*******************
v1.2.0 (2025-05-21)
*******************

Documentation
=============
- Update release procedure for a merge-commit style feature-branch workflow. By `Kyle Brindley`_.

Internal Changes
================
- Fix the SCons extensions builder unit test of builder keyword arguments. By `Kyle Brindley`_.
- Require WAVES>=0.12.6 for tutorials and system tests that run SCons workflows. By `Kyle Brindley`_.
- SCons build and install aliases for more consistent packaging and deployment scripts (:issue:`252`, :merge:`253`). By
  `Kyle Brindley`_.
- Require WAVES v0.13 or newer for building and runtime (:issue:`252`, :merge:`253`). By `Kyle Brindley`_.
- Overhaul Gitlab-CI job environments for reduced Conda environment collisions and improved job artifact cleanup (:issue:`254`,
  :merge:`254`). By `Kyle Brindley`_.
- Overhaul GitHub-Actions job definitions for common environment definitions with Gitlab-CI environments (:issue:`254`,
  :merge:`254`). By `Kyle Brindley`_.

*******************
v1.1.5 (2025-03-28)
*******************

Enhancements
============
- Suppress Cubit journal file output. Output is incomplete and all relevant meta data is also reported to STDOUT, which
  the user can choose to capture. Cubit can reach a self-imposed journal file count and throw errors until journal files
  are manually removed. This causes problems in large automated workflows (:issue:`250`, :merge:`250`). By `Kyle
  Brindley`_.

*******************
v1.1.4 (2025-03-17)
*******************

Internal Changes
================
- Handle proxy server changes for AEA RHEL CI builds (:issue:`247`, :merge:`247`). By `Kyle Brindley`_.
- System test against Abaqus Python 2/3 update (Abaqus 2023/2024) during MR pipelines (:issue:`248`, :merge:248`). By
  `Kyle Brindley`_.

Enhancements
============
- Abaqus Python 2/3 compatible print to shell's STDERR stream (:issue:`245`, :merge:`245`, :issue:`246`, :merge:`246`).
  By `Kyle Brindley`_.

*******************
v1.1.3 (2025-02-24)
*******************

Bug fixes
=========
- Update incorrect ``abaqusConstants`` value for two-dimensional planar parts in ``geometry`` subcommand
  (:issue:`242`, :merge:`242`). By `Thomas Roberts`_.

*******************
v1.1.2 (2024-12-02)
*******************

Bug fixes
=========
- Add pytest package to documentation build (:merge:`239`). By `Kyle Brindley`_.

*******************
v1.1.1 (2024-12-02)
*******************

Bug fixes
=========
- Fix internal import paths for docs and fetch subcommands (:merge:`238`). By `Kyle Brindley`_.

*******************
v1.1.0 (2024-12-02)
*******************

Documentation
=============
- Package internal HTML documentation for internal Conda package distribution (:issue:`235`, :merge:`230`). By `Kyle
  Brindley`_.
- Change Sphinx theme to ``sphinx-book-theme`` (:issue:`228`, :merge:`234`). By `Kyle Brindley`_.

Internal Changes
================
- Run the unit tests against a matrix of Abaqus and Cubit versions (:issue:`141`, :merge:`224`). By `Kyle Brindley`_.
- Run both unit and system tests against a matrix of Abaqus and Cubit versions during scheduled CI tests (:issue:`233`,
  :merge:`225`, :merge:`227`). By `Kyle Brindley`_.
- Add a scheduled CI job to test all support Python versions (:issue:`236`, :merge:`229`). By `Kyle Brindley`_.
- Remove the experimental, semi-private API builders in favor of the public CLI builder design (:issue:`234`,
  :merge:`231`).  By `Kyle Brindley`_.
- Autoformat and perform style checks with black and flake8 together (:issue:`231`, :merge:`235`). By `Kyle Brindley`_.

Enhancements
============
- Update docs subcommand implementation for more robust error messages (:issue:`232`, :merge:`232`). By `Kyle
  Brindley`_.

*******************
v1.0.0 (2024-10-21)
*******************

New Features
============
- Work-in-progress Gmsh cylinder subcommand implementation (:issue:`208`, :merge:`208`). By `Kyle Brindley`_.
- Work-in-progress Gmsh geometry subcommand implementation (:issue:`209`, :merge:`210`). By `Kyle Brindley`_.
- Work-in-progress Gmsh sphere subcommand implementation. Incorrect pre-existing, ``--input-file``, model handling.
  Solid spheres do not revolve correctly (:issue:`210`, :merge:`211`). By `Kyle Brindley`_.
- Work-in-progress Gmsh image subcommand implementation. Missing model name, part name, and image size behavior
  (:issue:`214`, :merge:`212`). By `Kyle Brindley`_.
- Work-in-progress Gmsh mesh subcommand implementation. Missing model name, part name, element type, and edge seed
  behaviors. Performs global tri- and tet-meshing globally to all models and parts. (:issue:`214`, :merge:`212`). By `Kyle
  Brindley`_.

Bug fixes
=========
- Fix temporary file handling for Windows (:issue:`224`, :merge:`214`). By `Kyle Brindley`_.
- Partition 2D models with Abaqus backend (:issue:`181`, :merge:`217`). By `Thomas Roberts`_.

Internal Changes
================
- Add Gmsh Python API to CI environment (:merge:`207`). By `Kyle Brindley`_.
- Update system tests and example scons extensions to use WAVES v0.11.0 syntax (:issue:`225`, :merge:`215`). By `Kyle
  Brindley`_.
- Add missing package to GitHub-CI environments (:issue:`226`, :merge:`219`). By `Kyle Brindley`_.
- Drop Python 3.8 support as end-of-life by the end of October, 2024 (:issue:`211`, :merge:`220`). By `Kyle Brindley`_.
- Set maximum ``sphinx_rtd_theme`` version because v3 removed the display version in sidebar support unless the
  documentation is actually hosted on Read the Docs. Temporary solution to finding a new documentation theme
  (:merge:`221`). By `Kyle Brindley`_.

*********************
v0.12.12 (2024-09-26)
*********************

Documentation
=============
- Add GitHub shields to HTML documentation (:issue:`198`, :merge:`197`). By `Kyle Brindley`_.
- Add GitHub-Pages documentation URL to README and documentation (:issue:`199`, :merge:`198`). By `Kyle Brindley`_.
- Add Zenodo DOI shields and citations (:issue:`168`, :merge:`199`). By `Kyle Brindley`_.
- Add conda-forge installation instructions and shields (:issue:`167`, :merge:`205`). By `Kyle Brindley`_.

Internal Changes
================
- Multi-OS compatible Conda package build and test scripts (:issue:`168`, :merge:`199`). By `Kyle Brindley`_.
- Test the external recipe during Gitlab-CI jobs (:issue:`168`, :merge:`199`). By `Kyle Brindley`_.
- Update setuptools version specs to match current setuptools_scm documentation (:issue:`201`, :merge:`200`). By `Kyle
  Brindley`_.
- Update recipes to match conda-forge recommendations (:issue:`202`, :merge:`201`). By `Kyle Brindley`_.
- Remove unnecessary fast test job from CI deployment pipelines (:issue:`203`, :merge:`202`). By `Kyle Brindley`_.
- Clean up PIP and Conda package builds to exclude project version control files (:issue:`204`, :merge:`203`). By `Kyle
  Brindley`_.
- Separate system tests that require third-party software from those that do not. Run external recipe builds with a
  single pytest command instead of hardcoding the CLI tests in the recipe test script (:issue:`205`, :merge:`206`). By
  `Kyle Brindley`_.

Enhancements
============
- Bundle built HTML and man page documentation with Gitlab PyPI registry package (:issue:`207`, :merge:`204`). By `Kyle
  Brindley`_.

*********************
v0.12.11 (2024-09-12)
*********************

Bug fixes
=========
- Better unit test patch for missing Cubit package, e.g. on conda-forge CI servers (:merge:`196`). By `Kyle Brindley`_.

*********************
v0.12.10 (2024-09-11)
*********************

Bug fixes
=========
- Fix package manifest for builds with newer conda-build/setuptools packages (:issue:`192`, :merge:`188`). By `Kyle
  Brindley`_.
- Remove system tests from external recipe(s) because they can not pass on CI servers without Abaqus and Cubit installed
  (:issue:`193`, :merge:`189`). By `Kyle Brindley`_.
- Fix the conda package entry points (:issue:`195`, :merge:`190`). By `Kyle Brindley`_.
- Better OS (Windows) path handling in test expectations (:issue:`197`, :merge:`192`). By `Kyle Brindley`_.
- Mock Cubit module during pytesting when Cubit is not available (:issue:`194`, :merge:`193`). By `Kyle Brindley`_.

Documentation
=============
- Point the README shields to the open-source release (:issue:`191`, :merge:`194`). By `Kyle Brindley`_.

Internal Changes
================
- Add Windows compatible build script for external conda package recipes (:issue:`196`, :merge:`191`). By `Kyle
  Brindley`_.
- Add GitHub-CI Windows build/test workflow (:issue:`196`, :merge:`191`). By `Kyle Brindley`_.

********************
v0.12.9 (2024-09-11)
********************

Documentation
=============
- Add the LANL software release number to the README (:merge:`187`). By `Kyle Brindley`_.

********************
v0.12.8 (2024-09-11)
********************

Bug fixes
=========
- Fix the GitHub pages build environment (:issue:`190`, :merge:`186`). By `Kyle Brindley`_.

********************
v0.12.7 (2024-08-27)
********************

Bug fixes
=========
- Handle the first target emitter name change for WAVES v0.10/v0.11 (:issue:`189`, :merge:`184`). By `Kyle Brindley`_.

Internal Changes
================
- Use common AEA Conda channel downstream deployment pipeline (:issue:`188`, :merge:`183`). By `Kyle Brindley`_.

********************
v0.12.6 (2024-07-11)
********************

Internal Changes
================
- Add twine package for Gitlab PyPI registry deployment (:merge:`182`). By `Kyle Brindley`_.

********************
v0.12.5 (2024-07-11)
********************

Internal Changes
================
- Experimental Gitlab PyPI registry deployment (:issue:`187`, :merge:`181`). By `Kyle Brindley`_.

********************
v0.12.4 (2024-07-10)
********************

Bug fixes
=========
- Preserve white space in set masks of Abaqus pass-through wrapper of the sets subcommand (:issue:`185`, :merge:`179`).
  By `Kyle Brindley`_.

Documentation
=============
- Edge seeds are implemented in Cubit. Remove "not yet implemented" statement from CLI usage help (:issue:`179`,
  :merge:`175`). By `Kyle Brindley`_.
- Add developer notes about package structure and interface designs (:issue:`135`, :merge:`178`). By `Kyle Brindley`_.

Internal Changes
================
- Remove indexing of the shared conda channel from CI deployment job. Can't use a project specific CI environment and
  manage the shared conda channel (:issue:`184`, :merge:`176`). By `Kyle Brindley`_.

********************
v0.12.3 (2024-06-26)
********************

Bug fixes
=========
- Match revolution direction of Abaqus and Cubit to the +Y axis (:issue:`183`, :merge:`174`). By `Kyle Brindley`_.

Enhancements
============
- Accept negative revolution angles to change revolution direction in Abaqus implementation (:issue:`183`,
  :merge:`174`). By `Kyle Brindley`_.

********************
v0.12.2 (2024-06-20)
********************

New Features
============
- Abaqus partitioning algorithm for 2D-axisymmetric parts (:issue:`181`, :merge:`217`). By `Thomas Roberts`_.
- Abaqus implementation of a ``sets`` subcommand for programmatic set creation (:issue:`164`, :merge:`161`). By `Kyle
  Brindley`_.
- Abaqus implementation of an edge seed option in the ``mesh`` subcommand (:issue:`173`, :merge:`164`). By `Kyle
  Brindley`_.
- Add ``sets`` subcommand CLI builder (:issue:`171`, :merge:`165`). By `Kyle Brindley`_.
- Cubit implementation of a ``sets`` subcommand and ``--edge-sets`` ``mesh`` option (:issue:`170`, :merge:`166`). `Kyle
  Brindley`_.

Bug fixes
=========
- Sphere module was missing an ``if`` statement that protected GUI execution from hitting the ``sys.exit(main(...))``
  statement and crashing the GUI session (:issue:`176`, :merge:`169`). By `Thomas Roberts`_.

Documentation
=============
- Break long API function signatures into multiple lines for better readability (:issue:`178`, :merge:`172`) By `Kyle
  Brindley`_.

Internal Changes
================
- Work-in-progress support for Abaqus CAE GUI export capability (:issue:`154`, :merge:`171`). By `Thomas Roberts`_.
- Work-in-progress support for Abaqus CAE GUI image capability (:issue:`155`, :merge:`170`). By `Thomas Roberts`_.
- Internal utility for constructing string delimited lists (:merge:`162`). By `Kyle Brindley`_.
- Add system tests for Abaqus implementation of sets subcommand (:issue:`172`, :merge:`163`). By `Kyle Brindley`_.
- Begin converting internal API error handling to exceptions. Limit conversion to system exit and error codes to the
  main implementation (:issue:`175`, :merge:`167`). By `Kyle Brindley`_.
- Activate project CI environment directly. Fixes errors related to conda-build/boa/mambabuild during packaging
  (:merge:`168`). By `Kyle Brindley`_.

Enhancements
============
- Collect and report specific set name/mask failures in the ``sets`` subcommand (:issue:`182`, :merge:`173`). By `Kyle
  Brindley`_.

********************
v0.12.1 (2024-04-30)
********************

Documentation
=============
- Add BSD-3 license text and files. Add placeholder citation files (:issue:`166`, :merge:`159`). By `Kyle Brindley`_.

Internal Changes
================
- Add GitHub actions and external conda package build recipe (:issue:`169`, :merge:`160`). By `Kyle Brindley`_.

********************
v0.12.0 (2024-04-30)
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
