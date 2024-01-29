# sachi

Sachi is a series and movie TUI renamer made with [Textual](https://github.com/textualize/textual/) which aims to replace FileBot.

## Getting Started

**Requirements:** Python 3.12 and [mediainfo](https://mediaarea.net/en/MediaInfo)

```sh
git clone https://github.com/NextFire/sachi.git
cd sachi/
poetry install
poetry run sachi --help
```

Or, with Docker:

```sh
docker run --rm -it \
  -v /path/to/config:/root/.config/sachi \
  -v /path/to/media:/media \
  ghcr.io/nextfire/sachi:main --help
```

## Features

Development is still in early stages, here's what's implemented so far:

- File selection
- TVDB series search (requires an API key)
- Filename jinja2 templating

In progress:

- FileBot context (https://www.filebot.net/naming.html)

The global configuration can be edited with `sachi config`.
