pip check
cd $SP_DIR/$PKG_NAME
pytest -vvv -n 4 --ignore=_abaqus_python --abaqus-command /apps/abaqus/Commands/abq2023 --cubit-command /apps/Cubit-16.16/cubit
/apps/abaqus/Commands/abq2023 abq2023 python -m unittest discover _abaqus_python/turbo_turtle_abaqus --verbose
