pip check
cd %SP_DIR%\%PKG_NAME%
pytest -vvv -n 4 --ignore=_abaqus_python
abq2024 python -m unittest discover _abaqus_python\turbo_turtle_abaqus --verbose
