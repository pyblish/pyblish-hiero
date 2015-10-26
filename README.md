# pyblish-hiero

This page will walk you through integrating Pyblish with Foundry Hiero.

### Prerequisities

Make sure you have installed Pyblish before continuing.

- See [Installing Pyblish](https://github.com/pyblish/pyblish/wiki/Installation)

### Introduction

The integration comes in the form of a menu-item called *"Publish"*, located directly under `File`.

Once clicked, it will display a Pyblish graphical user interface.

### Installation

Ensure Pyblish for Hiero is on your `PYTHONPATH` and run this within Hiero.

```python
import pyblish_hiero
pyblish_hiero.setup()
```

You can then show the Pyblish graphical user interface by calling `show()`.

```python
pyblish_hiero.show()
```

### Persistence

It is recommended that you allow Pyblish to load upon launching Hiero.
For this to work, add the `pyblish_hiero/hiero_plugin_path` directory to your `HIERO_PLUGIN_PATH`

(2) You can find your `pythonpath` directory here:

```bash
pyblish-hiero/pyblish_hiero/hiero_plugin_path
```

As you will find, this directory contains sub-directories leading to two python files; `pyblish_startup.py`, `active_project_tracker.py` and `selection_tracker.py`.

**pyblish_startup.py**

This sets up Pyblish similar to `pyblish_hiero.setup()`

**active_project_tracker.py**

This ensures that you can access the active project outside of Hiero, via `hiero.activeProject`. This is also injected into the context, so you can easily access the active project with `context.data('activeProject')`

**selection_tracker.py**

This ensures that you can access the active selection outside of Hiero, via `hiero.selection`. This is also injected into the context, so you can easily access the active selection with `context.data('selection')`
