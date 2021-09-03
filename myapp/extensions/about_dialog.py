from typing import List

import wx

from ..plugins import MenuTool, PluginBase


class AboutDialog(PluginBase):
    def menu_entries(self) -> List[MenuTool]:
        return [
            MenuTool(
                menu="About",
                id=wx.ID_ABOUT,
                text="About",
                description="Some info about this app",
                callback=self.dialog,
            ),
        ]

    @staticmethod
    def dialog(event):
        """A message dialog box with an OK button.

        wx.OK is a standard ID in wxWidgets.
        """
        #
        dlg = wx.MessageDialog(None, "A GUI example", "About the GUI", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.
