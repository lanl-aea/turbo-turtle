#########
|project|
#########

.. include:: project_brief.txt

.. only:: html

   .. |pipeline| image:: https://img.shields.io/github/actions/workflow/status/lanl-aea/turbo-turtle/pages.yml?branch=main&label=GitHub-Pages
      :target: https://lanl-aea.github.io/turbo-turtle/

   .. |release| image:: https://img.shields.io/github/v/release/lanl-aea/turbo-turtle?label=GitHub-Release
      :target: https://github.com/lanl-aea/turbo-turtle/releases

   .. |conda-forge version| image:: https://img.shields.io/conda/vn/conda-forge/turbo_turtle
      :target: https://anaconda.org/conda-forge/turbo_turtle

   .. |conda-forge downloads| image:: https://img.shields.io/conda/dn/conda-forge/turbo_turtle.svg?label=Conda%20downloads
      :target: https://anaconda.org/conda-forge/turbo_turtle

   .. |zenodo| image:: https://zenodo.org/badge/855818315.svg
      :target: https://zenodo.org/doi/10.5281/zenodo.13787498

   |pipeline| |release| |conda-forge version| |conda-forge downloads| |zenodo|

.. raw:: latex

   \part{User Manual}

.. toctree::
   :maxdepth: 2
   :caption: User Manual

   installation
   user
   external_api
   cli
   gui

.. raw:: latex

   \part{Developer Manual}

.. toctree::
   :maxdepth: 1
   :caption: Developer Manual

   internal_api
   devops

.. raw:: latex

   \part{Reference}

.. toctree::
   :maxdepth: 1
   :caption: Reference

   license
   citation
   release_philosophy
   changelog
   zreferences
   README

.. raw:: latex

   \part{Indices and Tables}

.. only:: html

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
