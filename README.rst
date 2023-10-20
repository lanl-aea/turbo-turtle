.. target-start-do-not-remove

.. _turbo-turtle: https://re-git.lanl.gov/tproberts/turbo-turtle
.. _AEA Gitlab Group: https://re-git.lanl.gov/aea
.. _Gitlab CI/CD: https://docs.gitlab.com/ee/ci/
.. _AEA Compute Environment: https://re-git.lanl.gov/aea/developer-operations/aea_compute_environment
.. _Bash rsync: https://re-git.lanl.gov/aea/developer-operations/aea_compute_environment

.. target-end-do-not-remove

############
Turbo Turtle
############

***********
Description
***********

This repository houses a script for partitioning hollow, spherical bodies using a turtle shell (otherwise known as
soccer ball) partitioning scheme. Turbo Turtle can be used in Abaqus CAE or as a command line utility to partition entire
spheres or any fraction of the sphere.

Documentation
=============

Until more in depth documentation is available, this README serves as the Turbo Turtle documentation.

Author Info
===========

* Thomas Roberts: tproberts@lanl.gov
* Kyle Brindley: kbrindley@lanl.gov

***************
Getting Started
***************

Coloning the Repository
=======================

.. cloning-the-repo-start-do-not-remove

Cloning the repository is very easy, simply refer to the sample session below. Keep in mind that you get to choose the
location of your local `turbo-turtle`_ clone. Here we use ``/projects/roppenheimer/repos`` as an example.

.. code-block:: bash

    [roppenheimer@sstelmo]$ pwd
    /projects/roppenheimer/repos
    [roppenheimer@sstelmo]$ git clone ssh://git@re-git.lanl.gov:10022/aea/python-projects/turbo-turtle.git
    <output truncated>
    [roppenheimer@sstelmo]$ ls -d
    other-repos    turbo-turtle

.. cloning-the-repo-end-do-not-remove

Compute Environment
===================

.. compute-env-start-do-not-remove

This repository is dependent on the access to an Abaqus kernel either through Abaqus CAE or through the command line. If
you are using a computer mapped to the W-13 NFS file shares (e.g. ``/home``, ``/projects``, ``/apps``), then access to
the Abaqus executable is trivial.

On an AEA Linux Machine
=======================
.. code-block:: Bash

   [roppenheimer@sstbigbird]$ module use /projects/aea_compute/modulefiles
   [roppenheimer@sstbigbird]$ module load aea-beta
   (aea-beta) [roppenheimer@sstbigbird]$ which abq2023
   /apps/abaqus/Commands/abq2023

.. compute-env-end-do-not-remove

*****************
Using turboTurtle
*****************

``turboTurtle`` can be executed in Abaqus CAE or by using the script's command line interface (CLI).

Abaqus CAE
==========

.. abaqus-cae-start-do-not-remove

When executing ``turboTurtle`` from Abaqus cae, ``turboTurtle`` will attempt to partition the part that is in the
current session's viewport. Execute ``turboTurtle`` in either of two ways:

Run Script Menu
---------------
Click File --> Run Script --> /projects/roppenheimer/turbo-turtle/turbo_turtle/_abaqus.py

Python Terminal
---------------
In the Abaqus CAE Python terminal, use the ``execPyFile`` function

.. code-block:: Python

   >>> execPyFile('/projects/roppenheimer/repos/turbo-turtle/turbo_turtle/_abaqus.py')

Interactive Input
-----------------
``turboTurtle`` will pop up a dialoge box where you can specify various parameters for partitioning the part in your
current session's viewport. Enter the relevant information, such as ``center`` and points on the ``x`` and ``z`` axis.
Click **OK** to run ``turboTurtle``.

Upon successful parsing of input parameters, ``turboTurtle`` will print the parameters you used to the Python terminal
in a specific format that ``turboTurtle`` understands. Should you wish to re-use a set of previously entered parameters
(i.e. partitioning multiple parts whose centers are all offset from the origin in the same way), you can simply copy and
paste those parameters into the "Copy and Paste Parameters" text box. In this case, all other values in the text boxes
above will be ignored, even if you modify them. Note, do not copy the header text underlined with ``---``.

.. abaqus-cae-end-do-not-remove

Command Line Execution
======================

.. command-line-execution-start-do-not-remove

This package has a thin Python 3 wrapper. It is no longer necessary to execute via Abaqus Python.

.. code-block::

   [roppenheimer@sstelmo]$ pwd
   /projects/roppenheimer/repos/turbo-turtle
   [roppenheimer@sstbigbird]$ module use /projects/aea_compute/modulefiles
   [roppenheimer@sstbigbird]$ module load aea-beta
   (aea-beta) [roppenheimer@sstbigbird]$ python -m turbo_turtle.main --help

The legacy instructions for executing the Abaqus Python interface directly have been updated below for reference.

``turboTurtle`` can be executed via CLI on any computer with Abaqus available via the command line. This README assumes
that a W-13 linux machine is used, so Abaqus 2021 is available at ``/apps/abaqus/Commands/abq2023``.

When using the ``turboTurtle`` CLI, an Abaqus CAE database with the unpartitioned geometry must already exist. The
sample terminal output below shows a directory structure that demonstrates the location of both an existing Abaqus CAE
database and a local clone of the `turbo-turtle`_ repository.

.. code-block:: Bash

   [roppenheimer@sstelmo]$ pwd
   /projects/roppenheimer
   [roppenheimer@sstelmo]$ ls -d
   example_turboTurtle    repos
   [roppenheimer@sstelmo]$ ls -d repos
   other-repos    turbo-turtle
   [roppenheimer@sstelmo]$ ls example_turboTurtle
   example_geometry.cae

From the directory structure shown above, ``turboTurtle`` can be executed from the command line using minimal required
arguments.

.. code-block:: bash

   [roppenheimer@sstelmo]$ /apps/abaqus/Commands/abq2023 cae -noGui repos/turbo-turtle/turbo_turtle/_abaqus.py -- --input-file example_turbotTurtle/example_geometry.cae --model-name example_model_name --part-name example_part_name example_model

Note that all parameters available through the Abaqus CAE GUI dialogue box are also available as command line arguments.
You can also print the ``turboTurtle`` CLI help message to the most recent ``abaqus.rpy`` file in your current working
directory with the ``-h`` flag.

.. code-block:: Bash

   [roppenheimer@sstelmo]$ /apps/abaqus/Commands/abq2021 cae -noGui repos/turbo-turtle/turbo_turtle/_abaqus.py -- -h

.. command-line-execution-end-do-not-remove

*******
Testing
*******

.. testing-start-do-not-remove

This project now performs CI testing on AEA compute servers. The up-to-date test commands can be found in the
``.gitlab-ci.yml`` file. The legacy testing instructions are show below, but may be out-of-date as the package works
towards a Python 3 deployment.

The `turbo-turtle`_ repository contains three Abaqus Python scripts for testing and demonstrating the ``turboTurtle``
capability.

.. code-block:: Bash

   [roppenheimer@sstelmo]$ pwd
   /projects/roppenheimer/repos/turbo-turtle
   [roppenheimer@sstelmo]$ ls turbo_turtle/tests
   tests_geometry.py  tests_main.py  tests_partition.py

* ``tests_geometry.py`` contains multiple functions for generating example geometry, such as a hollow sphere, fractions
  of a hollow sphere, and even a hollow sphere with assorted holes through the thickness (like a ball of swiss cheese).
* ``tests_partition.py`` containts multiple driver functions that call the ``turboTurtle.main`` function using the
  geometries created using ``tests_geometry.py``
* ``tests_main.py`` is the driver script for the tests.

To test ``turboTurtle`` via the command line:

.. code-block:: Bash

   [roppenheimer@sstelmo]$ pwd
   /projects/roppenheimer/repos/turbo-turtle/turbo_turtle/tests
   [roppenheimer@sstelmo]$ /apps/abaqus/Commands/abq2021 cae -noGui tests_main.py
   <output truncated>

If all tests are successful, Abaqus will return not return an error code, and your repo directory will contain some new
files.

.. code-block:: Bash

   [roppenheimer@sstelmo]$ ls *.{cae,jnl,rpy}
   abaqus.rpy  Turbo-Turtle-Tests.cae  Turbo-Turtle-Tests.jnl

All outputs from executing ``tests_main`` are printed to the most recent ``abaqus.rpy`` file in your working directory.
Open the ``Turbo-Turtle-Tests.cae`` Abaqus CAE database and inspect the parts to confirm that ``turboTurtle`` worked as
expected.

.. testing-end-do-not-remove

********************
Developer Operations
********************

.. developer-operations-start-do-not-remove

At the moment, the `turbo-turtle`_ repository is not part of the `AEA Gitlab Group`_, so `Gitlab CI/CD`_ cannot yet be
used to deploy `turbo-turtle`_ to the W-13 NFS file share Python project directories. In addition, this repository
contains code that is reliant on an Abaqus kernel (Abaqus version of Python 2). So, `turbo-turtle`_ cannot be Conda
packaged and deployed to the `AEA Compute Environment`_ like other Python 3 packages.

Deployment to a common location for W-13 users is currently a manual process. Deployment is done by using the `Bash
rsync`_ command to syncronize files between a local clone of the `turbo-turtle`_ repository and the deploy directory
``/projects/aea_compute/aea-abaqus-python/turbo-turtle``. The ``DEPLOY.sh`` script is included in this repository for
convenience. This script uses the `Bash rsync`_ command against all files in the repository that are not related to Git
(i.e. ``.git/`` and ``.gitignore`` are excluded from the ``rsync`` command) and the ``DEPLOY.sh`` script itself.

Manual deployment can be done from the Developer's terminal:

.. code-block:: Bash

   [developer@sstelmo]$ pwd
   /projects/developer/repos/turbo-turtle
   [developer@sstelmo]$ bash DEPLOY.sh

.. developer-operations-end-do-not-remove
