.. target-start-do-not-remove

.. _turbo-turtle: https://re-git.lanl.gov/tproberts/turbo-turtle
.. _AEA Gitlab Group: https://re-git.lanl.gov/aea
.. _Gitlab CI/CD: https://docs.gitlab.com/ee/ci/
.. _AEA Compute Environment: https://re-git.lanl.gov/aea/developer-operations/aea_compute_environment
.. _Bash rsync: https://re-git.lanl.gov/aea/developer-operations/aea_compute_environment

.. _`Kyle Brindley`: kbrindley@lanl.gov
.. _`Thomas Roberts`: tproberts@lanl.gov
.. _`Matthew Fister`: mwfister@lanl.gov
.. _`Paula Rutherford`: pmiller@lanl.gov

.. target-end-do-not-remove

############
Turbo Turtle
############

.. |pipeline| image:: https://re-git.lanl.gov/aea/python-projects/turbo-turtle/badges/main/pipeline.svg?key_text=re-git+tests&key_width=80
   :target: https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/pipelines

.. |release| image:: https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/badges/release.svg?key_text=re-git+release
   :target: https://re-git.lanl.gov/aea/python-projects/turbo-turtle/-/releases

|pipeline|

|release|

.. inclusion-marker-do-not-remove

***********
Description
***********

.. description-start-do-not-remove

A collection of solid body modeling tools for 2D sketched, 2D axisymmetric, and 3D revolved models. It also contains
general purpose meshing and image generation utilities appropriate for any model, not just those created with this
package. The initial implementation focuses and relies on Abaqus for all subcommands. Cubit subcommand implementations
are also available.

As much as possible, the work for each subcommand is performed in Python 3 to minimize solution approach duplication in
third-party tools. As much as possible, the third-party scripting interface is only accessed when creating the final
tool specific objects and output. The tools contained in this project can be expanded to drive other meshing utilities
in the future, as needed by the user community.

This project derives its name from the origins as a sphere partitioning utility following the turtle shell (or soccer
ball) pattern.

.. description-end-do-not-remove

Documentation
=============

* https://aea.re-pages.lanl.gov/python-projects/turbo-turtle/

Author Info
===========

* `Kyle Brindley`_
* `Thomas Roberts`_

.. user-start-do-not-remove

***********
Quick Start
***********

This project is now packaged with a thin Python 3 wrapper. It is no longer necessary to clone the project when working
on AEA RHEL (linux) servers.

1. Load the AEA compute environment

   .. code-block::

      $ module use /projects/aea_compute/aea-conda
      $ module load aea-beta

2. View the CLI usage

   .. code-block::

      $ turbo-turtle -h
      $ turbo-turtle docs -h
      $ turbo-turtle geometry -h
      $ turbo-turtle cylinder -h
      $ turbo-turtle sphere -h
      $ turbo-turtle partition -h
      $ turbo-turtle mesh -h
      $ turbo-turtle image -h
      $ turbo-turtle merge -h
      $ turbo-turtle export -h

.. user-end-do-not-remove

**********************
Developer Instructions
**********************

Cloning the Repository
======================

.. cloning-the-repo-start-do-not-remove

Cloning the repository is very easy, simply refer to the sample session below. Keep in mind that you get to choose the
location of your local `turbo-turtle`_ clone. Here we use ``/projects/roppenheimer/repos`` as an example.

.. code-block:: bash

    [roppenheimer@sstelmo repos]$ git clone ssh://git@re-git.lanl.gov:10022/aea/python-projects/turbo-turtle.git

.. cloning-the-repo-end-do-not-remove

Compute Environment
===================

.. compute-env-start-do-not-remove

This repository requires Abaqus and Cubit to be installed and on the system ``PATH``. If you use an AEA linux computer,
then the project continuous-integration environment is available as a development environment.

On an AEA Linux Machine
-----------------------

.. code-block:: bash

   [roppenheimer@sstbigbird turbo-turtle]$ module use /projects/aea_compute/modulefiles
   [roppenheimer@sstbigbird turbo-turtle]$ module load turbo-turtle-dev
   (aea-beta) [roppenheimer@sstbigbird]$ which abq2023
   /apps/abaqus/Commands/abq2023
   (aea-beta) [roppenheimer@sstbigbird]$ which cubit
   /apps/Cubit16.12/cubit

Local development environment
-----------------------------

You can also create a local environment with the Conda package manager as

.. code-block::

   [roppenheimer@mymachine turbo-turtle]$ conda env create --file environment.yml --name turbo-turtle-dev
   [roppenheimer@mymachine turbo-turtle]$ conda activate turbo-turtle-dev

.. compute-env-end-do-not-remove

Testing
=======

.. testing-start-do-not-remove

This project now performs CI testing on AEA compute servers. The up-to-date test commands can be found in the
``.gitlab-ci.yml`` file. The full regression suite includes the documentation builds, Python 3 unit tests, Abaqus Python
unit tests, and the system tests.

.. code-block::

    $ pwd
    /home/roppenheimer/repos/turbo-turtle
    $ scons regression

.. testing-end-do-not-remove

*******************
Legacy Instructions
*******************

Using turboTurtle
=================

``turboTurtle`` can be executed in Abaqus CAE or by using the script's command line interface (CLI).

Abaqus CAE
----------

.. abaqus-cae-start-do-not-remove

When executing ``turboTurtle`` from Abaqus cae, ``turboTurtle`` will attempt to partition the part that is in the
current session's viewport. Execute ``turboTurtle`` in either of two ways:

*Run Script Menu*

Click File --> Run Script --> /projects/roppenheimer/turbo-turtle/turbo_turtle/_partition.py

*Python Terminal*

In the Abaqus CAE Python terminal, use the ``execPyFile`` function

.. code-block:: Python

   >>> execPyFile('/projects/roppenheimer/repos/turbo-turtle/turbo_turtle/_partition.py')

*Interactive Input*

``turboTurtle`` will pop up a dialoge box where you can specify various parameters for partitioning the part in your
current session's viewport. Enter the relevant information, such as ``center`` and points on the ``x`` and ``z`` axis.
Click **OK** to run ``turboTurtle``.

Upon successful parsing of input parameters, ``turboTurtle`` will print the parameters you used to the Python terminal
in a specific format that ``turboTurtle`` understands. Should you wish to re-use a set of previously entered parameters
(i.e. partitioning multiple parts whose centers are all offset from the origin in the same way), you can simply copy and
paste those parameters into the "Copy and Paste Parameters" text box. In this case, all other values in the text boxes
above will be ignored, even if you modify them. Note, do not copy the header text underlined with ``---``.

.. abaqus-cae-end-do-not-remove
