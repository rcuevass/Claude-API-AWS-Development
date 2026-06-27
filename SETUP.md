# Setup instructions

This markdown captures the basic instructions to create a virtual uv environment needed for the proper functioning of the code in this repository.

Gitbash on a Windows machine is assumed througout.

#### Install all required packages from `pyproject.toml`

`uv sync --active`


#### Activate the environment

`source .venv/Script/activate`

#### Updating/syncing .toml

Whenever a new library has to be added to .toml, just add the library and sync the env with the command `uv sync`. This will also update the `uv.lock` file