from pathlib import Path
from typing import List

import wx
import wx.adv

from guikit.plugins import MenuTool, PluginBase

from ... import VERSION


class AboutDialogPlugin(PluginBase):
    def menu_entries(self) -> List[MenuTool]:
        return [
            MenuTool(
                menu="About",
                id=wx.ID_ABOUT,
                text="About",
                description="Some info about this app",
                callback=self.OnAboutBox,
            ),
        ]

    def OnAboutBox(self, e):
        with (Path(__file__).parent / "description").open("r") as f:
            description = f.read()

        with (Path(__file__).parent / "license").open("r") as f:
            licence = f.read()

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(
            wx.Icon(str(Path(__file__).parent / "logo.png"), wx.BITMAP_TYPE_PNG)
        )
        info.SetName("PyGUItemp")
        info.SetVersion(VERSION)
        info.SetDescription(description)
        info.SetCopyright("(C) Imperial College London")
        info.SetWebSite("https://imperialcollegelondon.github.io/python-gui-template/")
        info.SetLicence(licence)
        info.AddDeveloper("Diego Alonso Álvarez")
        info.AddDocWriter("Diego Alonso Álvarez")

        wx.adv.AboutBox(info)
