"""Adapted from ZetCode wxPython tutorial

https://zetcode.com/wxpython/dialogs/

In this example, we create an
about dialog box.

author: Jan Bodnar
website: www.zetcode.com
last modified: July 2020
"""
from pathlib import Path
from typing import List

import wx
import wx.adv

from ...plugins import MenuTool, PluginBase


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

        with (Path(__file__).parent / "licence").open("r") as f:
            licence = f.read()

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(
            wx.Icon(str(Path(__file__).parent / "logo.png"), wx.BITMAP_TYPE_PNG)
        )
        info.SetName("File Hunter")
        info.SetVersion("1.0")
        info.SetDescription(description)
        info.SetCopyright("(C) 2007 - 2021 Jan Bodnar")
        info.SetWebSite("http://www.zetcode.com")
        info.SetLicence(licence)
        info.AddDeveloper("Jan Bodnar")
        info.AddDocWriter("Jan Bodnar")
        info.AddArtist("The Tango crew")
        info.AddTranslator("Jan Bodnar")

        wx.adv.AboutBox(info)
