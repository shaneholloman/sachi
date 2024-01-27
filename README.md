# sachi

Sachi is a series and movie TUI (?) renamer. It aims to replace FileBot.

## Getting Started

**Requirements:** Python 3.12 and [mediainfo](https://mediaarea.net/en/MediaInfo)

```sh
git clone https://github.com/NextFire/sachi.git
cd sachi/
poetry install
poetry run sachi --help
```

## Features

Development is still in early stages, here's what's implemented so far:

- File selection
- TVDB series search (requires an API key)
- Filename jinja2 templating

In progress:

- FileBot context (https://www.filebot.net/naming.html)

A GUI is not planned. You are asked instead to edit multiple TOML files during the renaming process.

The global configuration can be edited with `sachi config` (also a TOML file).
