############
Turbo Turtle
############

***********
Description
***********

This repository houses a script for partitioning hollow, spherical bodies using a turtle shell (otherwise known as 
soccer ball) partitioning scheme. Turbo Turtle can be used in Abaqus CAE or as a command line utlity to partition entire 
spheres or any fraction of the sphere.

Documentation
=============

Until more in depth documentation is available, this README serves as the Turbo Turtle documentation.

Author Info
===========

* Thomas Roberts: tproberts@lanl.gov


***************
Getting Started
***************

Coloning the Repository
=======================

.. cloning-the-repo-start-do-not-remove

Cloning the repository is very easy, simply refer to the sample session below. Keep in mind that you get to choose the 
``/path/to/repos``.

.. code-block:: bash

    [roppenheimer@sstelmo]$ pwd
    /path/to/repos
    [roppenheimer@sstelmo]$ git clone ssh://git@re-git.lanl.gov:10022/tproberts/turbo-turtle.git
    <output truncated>
    [roppenheimer@sstelmo]$ ls
    turbo-turtle    other-repos

.. cloning-the-repo-end-do-not-remove

Compute Environment
===================

.. compute-env-start-do-not-remove

This repository is dependent on the access to an Abaqus kernel either through Abaqus CAE or through the command line. If 
you are using a computer mapped to the W-13 NFS file shares (e.g. ``/home``, ``/projects``, ``/apps``), then access to 
the Abaqus executable is trivial.

**At the moment, this repository has only been tested using Abaqus 2021**

On a Linux Machine
******************

.. code-block:: Bash

   [roppenheimer@sstelmo]$ whereis abq2021
   abq2021: /apps/abaqus/Commands/abq2021

.. compute-env-end-do-not-remove

