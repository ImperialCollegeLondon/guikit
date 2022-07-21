# The Plugin System

`guikit`'s plugin system is designed to simplify adding new functionality to the
application. It makes some "reasonable" assumptions of what the GUI should look like,
what elements it should have and where they should be located.

These plugins can bring to the application not just new components for the interface,
but also other business functionality via, e.g. [accessors for pandas DataFrames](https://pandas.pydata.org/docs/development/extending.html#extending-pandas) or
[listeners for a messaging system](https://pypubsub.readthedocs.io).

## How to add a `guikit` plugin

If there is a plugin in `guikit` that does what you need - or somethig close to it
that you can customize - the shortest approach to bring that plugin to your project is
with the command:

```bash
python -m guikit plugin -n PLUGIN_NAME -t my_app/extensions
```

This assumes you are in the root directory of your application and that there is a
subfolder called `extensions`, which is the structure you should get when you follow the
steps described in the [using guikit section](using_guikit.md). The command above
will take the code for the chosen plugin from `guikit`'s source code and will copy it
to the chosen location. You can check the plugins available in the documentation on the
web or with:

```bash
python -m guikit plugin -l
```

After copying the plugin, just add it to the `config.py` file:

```python
# config.py
#...
PLUGINS = ["my_app.extensions.PLUGIN_NAME"]
#...
```

Multiple plugins can be added at once separating them with a comma (`,`):

```bash
python -m guikit plugin -n PLUGIN_1,PLUGIN_2,PLUGIN_3 -t my_app/extensions
```

## How to add a custom plugin

To add a custom plugin, follow these steps:

1. Create a subpackage (i.e. a folder with an `__init__.py` within) somewhere in the
   code structure to hold your plugin. Typically, this will be within the `extensions`
   package, for example in `my_app/extensions/new_plugin`.
1. Add that location, replacing slashes by periods `.`, to the `config.PLUGINS` list.
1. Subclass `guikit.plugins.PluginBase` somewhere within your plugin. This is
   the class that will provide the specific components of the GUI that this plugin
   contributes with. More on this below.
1. Import that subclass in the `__init__.py` file of your plugin.

In the end, your directory structure and file content should look something similar to
the following:

```bash
- my_app
    |- config.py
    |- extensions
        |- new_plugin
        |   - __init__.py
        |   - view.py
        |...
    |...
```

```python
# config.py
#...
PLUGINS = ["my_app.extensions.new_plugin"]
#...
```

```python
# new_plugin.__init__.py
from .view import NewPlugin
```

```python
# new_plugin.view.py
from guikit.plugins import PluginBase

class NewPlugin(PluginBase):
    pass
```

## The plugin class

Any new GUI element that the plugin provides need to be incorporated into a subclass of
PluginBase. This class provides 4 methods that you should override so they output the
elements you want (by default, output is either `None` or `[]`).

Each of the 4 methods deals with one type of component of the GUI: a menu item, a tool
bar item, a tab or a central widget. You can override only one of them, all, or anything
in between depending on what functionality the plugin is providing.

### Adding menu entries

This is done with the `menu_entries` method fo the class. Override this method if your
plugin provides new entires for the menu bar of the application. The output must be a
list of `guikit.plugin.MenuTool` objects, which is just a dataclass with some fields
to complete.

For example, the following bit of code will add two entries, one for loading data and
another one for saving it, in both cases within a `File` menu:

```python
# new_plugin.view.py
from guikit.plugins import PluginBase, MenuTool

class NewPlugin(PluginBase):

    def menu_entries(self):
        save = MenuTool(
            menu="File",
            text="Save data",
            description="Save selected data into disk",
            callback=save_data
        )
        load = MenuTool(
            menu="File",
            text="Load data",
            description="Load new data from disk",
            callback=load_data
        )
        return [save, load]

def save_data(_):
    pass

def load_data(_):
    pass
```

### Adding tools

This is done with the `toolbar_items` method. This method is very similar to the
`menu_entries` one, but provides content to the toobar just under the menu bar. The
output must also be a list of `guikit.plugin.MenuTool` objects, but it has some extra
entries, a `short_help` for the tooltip and `bitmap`, which is mandatory as it is the
icon to display.

For example, the following bit of code will add the same two entries for loading and
saving data, but now to the toolbar. We use some standard icons provided by wxPython,
but you can use your own bitmaps, too. See
[`wx.ArtProvider`](https://wxpython.org/Phoenix/docs/html/wx.ArtProvider.html) for more
information about this.

```python
# new_plugin.view.py
from guikit.plugins import PluginBase, MenuTool

class NewPlugin(PluginBase):

    def toolbar_items(self):
        save = MenuTool(
            menu="File",
            text="Save data",
            description="Save selected data into disk",
            short_help="Save selected data into disk",
            bitmap=wx.ArtProvider.GetBitmap(
                    wx.ART_FILE_SAVE, wx.ART_TOOLBAR, wx.Size(50, 50)
                ),
            callback=save_data
        )
        load = MenuTool(
            menu="File",
            text="Load data",
            description="Load new data from disk",
            short_help="Load new data from disk",
            bitmap=wx.ArtProvider.GetBitmap(
                    wx.ART_FILE_OPEN, wx.ART_TOOLBAR, wx.Size(50, 50)
                ),
            callback=load_data
        )
        return [save, load]

def save_data(_):
    pass

def load_data(_):
    pass
```

### Adding tabs

One of the design decisions made for `guikit` is that it can either provide a single
central widget (see below) or a notebook with tabs. The `tabs` methods is used for the
latter. This method should return a list of `guikit.plugin.Tab` objects, each of them
representing a different tab of the notebook.

The `Tab` object is also just a dataclass with some fields to fill, like the name and
the order of the tab within the notebook. The most important option is the `page`, an
object of `wx.Window` type (or subclass of it) that will fill the entire tab. Pretty
much anything in `wxPython` is a `wx.Window`, so you can use almost anything as the
`page` option. You might have plots, tables, buttons arranged in rows and columns,
entries, etc. The most common candidate for the `page` is a `wx.Panel` that you populate
with whatever you want. See [this tutorial on
ZetCode](https://zetcode.com/wxpython/widgets/) for some detailed examples.

In the following example, we just create two text areas to write into, which will fill
the entire tab.

```python
# new_plugin.view.py
from guikit.plugins import PluginBase, Tab
import wx

class NewPlugin(PluginBase):

    def tabs(self, parent):
        text1 = Tab(
            page=wx.TextCtrl(parent, style=wx.TE_MULTILINE),
            text="Text area",
        )
        text2 = Tab(
            page=wx.TextCtrl(parent, style=wx.TE_MULTILINE),
            text="A second text area",
        )
        return [text1, text2]
```

In order to use the notebook layout, you will need to indicate so in the `config.py`
file with:

```python
# config.py
#...
NOTEBOOK_LAYOUT = True
#...
```

### Adding a central widget

The `central` method provides one `wx.Window` object as ouput, which will replace the
notebook. This can be anythinng thay you could use as a `page` in the `tabs` case above.

In order to use the central widget layout, you will need to disable the notebook one in
the `config.py` file with:

```python
# config.py
#...
NOTEBOOK_LAYOUT = False
#...
```

It should be noted that the central widget must be unique across all the plugins used
in the application. If the notebook layout is disabled, `guikit` will expect one and
only one plugin with a `central` method returning not `None`. If that happens, an error
will be raised.

TIn the following example, a single text area is used as central widget.

```python
# new_plugin.view.py
from guikit.plugins import PluginBase
import wx

class NewPlugin(PluginBase):

    def central(self, parent):
        return wx.TextCtrl(parent, style=wx.TE_MULTILINE)
```
