from typing import List

from pyguitemp.plugins import PluginBase, Tab

from .view import DataLoaderTab


class DataPlugin(PluginBase):
    def tabs(self, parent=None) -> List[Tab]:
        data_loader_tab = DataLoaderTab(parent)
        return [Tab(page=data_loader_tab, text="Data", order=0)]
