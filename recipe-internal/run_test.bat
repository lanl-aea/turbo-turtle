pip check
cd %SP_DIR%\%PKG_NAME%
pytest -vvv -n 4 --ignore=_abaqus_python -m "not require_third_party"
