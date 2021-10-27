from typing import List

from pyguitemp.plugins import PluginBase, Tab

from .model import load_data
from .view import DataLoaderTab, FileDialogCustom


class DataPlugin(PluginBase):
    def tabs(self, parent=None) -> List[Tab]:
        data_loader_tab = DataLoaderTab(parent, select_file)
        return [Tab(page=data_loader_tab, text="Data", order=0)]


def select_file() -> None:
    """Loads a text file from disk."""
    with FileDialogCustom() as dlg:
        if not dlg.open():
            # the user changed their mind
            return

        filename = dlg.GetPath()

    load_data(filename)
