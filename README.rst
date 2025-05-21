.. target-start-do-not-remove

.. _`Turbo-Turtle`: https://lanl-aea.github.io/turbo-turtle/index.html
.. _`Turbo-Turtle repository`: https://re-git.lanl.gov/aea/python-projects/turbo-turtle
.. _`AEA Gitlab Group`: https://re-git.lanl.gov/aea
.. _`Gitlab CI/CD`: https://docs.gitlab.com/ee/ci/
.. _`AEA Compute Environment`: https://re-git.lanl.gov/aea/developer-operations/aea_compute_environment
.. _`AEA Conda channel`: https://aea.re-pages.lanl.gov/developer-operations/aea_compute_environment/aea_compute_environment.html#aea-conda-channel
.. _`Bash rsync`: https://re-git.lanl.gov/aea/developer-operations/aea_compute_environment
.. _Conda: https://docs.conda.io/en/latest/
.. _Conda installation: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
.. _Conda environment management: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
.. _SCons: https://scons.org/

.. _`Kyle Brindley`: kbrindley@lanl.gov
.. _`Thomas Roberts`: tproberts@lanl.gov
.. _`Matthew Fister`: mwfister@lanl.gov
.. _`Paula Rutherford`: pmiller@lanl.gov

.. target-end-do-not-remove

############
Turbo Turtle
############

.. |pipeline| image:: https://img.shields.io/github/actions/workflow/status/lanl-aea/turbo-turtle/pages.yml?branch=main&label=GitHub-Pages
   :target: https://lanl-aea.github.io/turbo-turtle/

.. |release| image:: https://img.shields.io/github/v/release/lanl-aea/turbo-turtle?label=GitHub-Release
   :target: https://github.com/lanl-aea/turbo-turtle/releases

.. |conda-forge version| image:: https://img.shields.io/conda/vn/conda-forge/turbo_turtle
   :target: https://anaconda.org/conda-forge/turbo_turtle

.. |conda-forge downloads| image:: https://img.shields.io/conda/dn/conda-forge/turbo_turtle.svg?label=Conda%20downloads
   :target: https://anaconda.org/conda-forge/turbo_turtle

.. |pypi version| image:: https://img.shields.io/pypi/v/turbo-turtle?label=PyPI%20package
   :target: https://pypi.org/project/turbo-turtle/

.. |pypi downloads| image:: https://img.shields.io/pypi/dm/turbo-turtle?label=PyPI%20downloads
   :target: https://pypi.org/project/turbo-turtle/

.. |zenodo| image:: https://zenodo.org/badge/855818315.svg
   :target: https://zenodo.org/doi/10.5281/zenodo.13787498

|pipeline| |release| |conda-forge version| |conda-forge downloads| |pypi version| |pypi downloads| |zenodo|

.. inclusion-marker-do-not-remove

***********
Description
***********

.. description-start-do-not-remove

`Turbo-Turtle`_ (LANL code O4765) is a collection of solid body modeling tools for 2D sketched, 2D axisymmetric, and 3D
revolved models. It also contains general purpose meshing and image generation utilities appropriate for any model, not
just those created with this package. Implemented for Abaqus and Cubit as backend modeling and meshing software. Orginal
implementation targeted Abaqus so most options and descriptions use Abaqus modeling concepts and language.

Turbo-Turtle makes a best effort to maintain common behaviors and features across each third-party software's modeling
concepts. As much as possible, the work for each subcommand is performed in Python 3 to minimize solution approach
duplication in third-party tools. The third-party scripting interface is only accessed when creating the final tool
specific objects and output. The tools contained in this project can be expanded to drive other meshing utilities in the
future, as needed by the user community.

This project derives its name from the origins as a sphere partitioning utility following the turtle shell (or soccer
ball) pattern.

.. description-end-do-not-remove

Documentation
=============

* GitHub: https://lanl-aea.github.io/turbo-turtle/
* LANL: https://aea.re-pages.lanl.gov/python-projects/turbo-turtle/

Author Info
===========

* `Kyle Brindley`_
* `Thomas Roberts`_

************
Installation
************

.. installation-start-do-not-remove

`Turbo-Turtle`_ can be installed in a `Conda`_ environment with the `Conda`_ package manager. See the `Conda
installation`_ and `Conda environment management`_ documentation for more details about using `Conda`_.

.. code-block::

   $ conda install --channel conda-forge turbo_turtle

.. installation-end-do-not-remove

***********
Quick Start
***********

.. user-start-do-not-remove

1. View the CLI usage

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

****************
Copyright Notice
****************

.. copyright-start-do-not-remove

Copyright (c) 2024, Triad National Security, LLC. All rights reserved.

This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL),
which is operated by Triad National Security, LLC for the U.S.  Department of Energy/National Nuclear Security
Administration. All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of
Energy/National Nuclear Security Administration. The Government is granted for itself and others acting on its behalf a
nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare derivative works, distribute
copies to the public, perform publicly and display publicly, and to permit others to do so.

.. copyright-end-do-not-remove

**********************
Developer Instructions
**********************

Cloning the Repository
======================

.. cloning-the-repo-start-do-not-remove

Cloning the repository is very easy, simply refer to the sample session below. Keep in mind that you get to choose the
location of your local `Turbo-Turtle repository`_ clone. Here we use ``/projects/roppenheimer/repos`` as an example.

.. code-block:: bash

    [roppenheimer@sstelmo repos]$ git clone ssh://git@re-git.lanl.gov:10022/aea/python-projects/turbo-turtle.git

.. cloning-the-repo-end-do-not-remove

Compute Environment
===================

.. compute-env-start-do-not-remove

This project uses `Conda`_ to manage most of the compute environment. Some software, e.g. Abaqus and Cubit, can not be
installed with `Conda`_ and must be installed separately.

`SCons`_  can be installed in a `Conda`_ environment with the `Conda`_ package manager. See the `Conda installation`_
and `Conda environment management`_ documentation for more details about using `Conda`_.

1. Create the environment if it doesn't exist

   .. code-block::

      $ conda env create --name berms-env --file environment.yml

2. Activate the environment

   .. code-block::

      $ conda activate berms-env

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

There is also a separate style guide check run as

.. code-block::

    $ scons flake8 black-check

The full list of available aliases can be found as ``scons -h``.

.. testing-end-do-not-remove
