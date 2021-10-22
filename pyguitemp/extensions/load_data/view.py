from pathlib import Path

import wx
from pubsub import pub


class DataLoaderTab(wx.Window):
    def __init__(self, parent):
        super(DataLoaderTab, self).__init__(parent)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        open_btn = wx.Button(self, label="Load data file")
        self.filename_lbl = wx.StaticText(self, label="No data loaded")
        hbox.Add(open_btn, flag=wx.EXPAND | wx.ALL, border=10)
        hbox.Add(self.filename_lbl, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)

        self.Bind(wx.EVT_BUTTON, self.on_open, source=open_btn)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(hbox)

        self.SetSizer(main_sizer)

    def on_open(self, _):
        with wx.FileDialog(
            self,
            "Open data file",
            wildcard="CSV files (*.CSV)|*.csv",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as dlg:

            if dlg.ShowModal() == wx.ID_CANCEL:
                # the user changed their mind
                return

            # Proceed loading the file chosen by the user
            filename = Path(dlg.GetPath()).name
            self.filename_lbl.SetLabelText(filename)
            pub.sendMessage("data.load", data_path=dlg.GetPath())
