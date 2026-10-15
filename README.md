Welcome to hawking-tools!

## Running the tool (uv)

### Installation
To get started, install [uv](https://docs.astral.sh/uv/getting-started/installation/)
* ```curl -LsSf https://astral.sh/uv/install.sh | sh```  

For more info on uv, visit https://docs.astral.sh/uv/getting-started/installation/

After installing uv, simply run ```uv run hawking``` and you will be prompted for your username and password.
* uv will take care of installing any required dependencies (& python versions) automatically.


## How to build the Hawking cli

You will need to have [pyinstaller](https://pyinstaller.org/en/stable/) installed to build the cli (It is part of the dev dependencies). You can install it with uv by running the following command in the root directory of the project:

```bash
uv sync --all-groups
```

Then, you can build the cli by running the following command in the root directory of the project:
```bash
uv run pyinstaller --clean --noconfirm hawking.spec
```

The `hawking` executable will be created in the `dist` directory. You can run it from there or move it to a directory in your PATH for easier access.