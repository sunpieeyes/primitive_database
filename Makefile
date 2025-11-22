install:
\tpoetry install

project:
\tpoetry run project

build:
\tpoetry build

publish:
\tpoetry publish --dry-run

package-install:
\tpython3 -m pip install dist/*.whl

lint:
\tpoetry run ruff check .
