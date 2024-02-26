=====
Clone
=====

.. include:: README.txt
   :start-after: cloning-the-repo-start-do-not-remove
   :end-before: cloning-the-repo-end-do-not-remove

===================
Compute Environment
===================

.. include:: README.txt
   :start-after: compute-env-start-do-not-remove
   :end-before: compute-env-end-do-not-remove

=======
Testing
=======

.. include:: README.txt
   :start-after: testing-start-do-not-remove
   :end-before: testing-end-do-not-remove

======================================
Abaqus Python Module Naming Convention
======================================

The :meth:`turbo_turtle.main._print_abaqus_module_location` function assumes that subcommands have a matching
Abaqus python module with an identical name existing in the ``_settings.abaqus_python_abspath`` directory.
:issue:`134` is scoped to remove this dependency and allow more flexibility in naming of subcommands and the
corresponding Abaqus python modules.
