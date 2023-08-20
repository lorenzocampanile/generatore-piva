# Esegui la build del pacchetto
pip-compile pyproject.toml && python -m pip install -e . && python -m pip install build && python -m build