#########
|project|
#########

.. include:: project_brief.txt

.. raw:: latex

   \part{User Manual}

.. toctree::
   :hidden:
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
   :hidden:
   :maxdepth: 1
   :caption: Developer Manual

   internal_api
   devops

.. raw:: latex

   \part{Reference}

.. toctree::
   :hidden:
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

   |

   .. grid:: 1 2 2 2
      :gutter: 2
      :margin: 2

      .. grid-item-card:: :octicon:`download` Installation
         :link: installation
         :link-type: ref

         Installation with conda-forge or PyPI

      .. grid-item-card:: :octicon:`rocket` Quickstart
         :link: quickstart
         :link-type: ref

         Minimal working examples of command line interface

      .. grid-item-card:: :octicon:`code-square` API
         :link: external_api
         :link-type: ref

         Public application program interface (API)

      .. grid-item-card:: :octicon:`command-palette` CLI
         :link: turbo_turtle_cli 
         :link-type: ref

         Public command line interface (CLI)
