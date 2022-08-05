import sys

import pytest


@pytest.mark.skipif(
    sys.platform == "darwin", reason="Cause segmentation fault for unknown reasons."
)
class TestDialog:
    def test_constructor(self, mocker, window):
        from guikit.progress import Dialog

        spy_set_range = mocker.spy(Dialog, "SetRange")
        spy_subscribe = mocker.spy(Dialog, "subscribe_for_updates")

        with Dialog(maximum=200) as dlg:
            spy_set_range.assert_called_once_with(dlg, 200)
            spy_subscribe.assert_called_once()

    def test_set_range(self, window):
        from guikit.progress import Dialog

        # No using 'steps'
        with Dialog(maximum=200, every=2) as dlg:
            assert dlg.Range == 200
            assert dlg.every == 2

            dlg.SetRange(300)
            assert dlg.Range == 300
            assert dlg.every == 2

        # Using steps
        with Dialog(maximum=200, steps=20) as dlg:
            assert dlg.Range == 200
            assert dlg.every == 200 // 20

            dlg.SetRange(300)
            assert dlg.Range == 300
            assert dlg.every == 300 // 20

    def test_update(self, mocker, window):
        from guikit.progress import Dialog

        spy_set_range = mocker.spy(Dialog, "SetRange")

        maximum = 100
        with Dialog(maximum=maximum, every=2) as dlg:

            # If value is not an integer, raise error
            with pytest.raises(ValueError):
                dlg.Update(value=2.2, maximum=100)

            spy_set_range.call_count == 2

            # If the vallue is higher than the maximum, raise error
            with pytest.raises(ValueError):
                dlg.Update(value=maximum + 1)

            # If not a multiple of 'every' not update
            assert dlg.Update(value=1)
            assert dlg.GetValue() == 0

            # If a multiple of 'every', update
            assert dlg.Update(value=2)
            assert dlg.GetValue() == 2

            # When getting to the last value, hide the dialog
            if sys.platform != "win32":
                assert dlg.IsShownOnScreen()
            assert dlg.Update(value=100)
            assert dlg.GetValue() == 100
            if sys.platform != "win32":
                assert not dlg.IsShownOnScreen()

            # If it is hidden and a new value is given, show it again
            assert dlg.Update(value=0)
            assert dlg.GetValue() == 0
            if sys.platform != "win32":
                assert dlg.IsShownOnScreen()

    def test_subscribe_for_updates(self, mocker, window):
        from pubsub import pub

        from guikit.progress import Dialog

        spy_subscribe = mocker.spy(pub, "subscribe")

        with Dialog() as dlg:
            dlg.subscribe_for_updates()
            spy_subscribe.assert_not_called()

            dlg.channel = "my_channel"
            dlg.subscribe_for_updates()
            spy_subscribe.assert_called_once()

    def test_broadcast_abort(self, mocker, window):
        from pubsub import pub

        from guikit.progress import Dialog

        spy_send = mocker.spy(pub, "sendMessage")

        with Dialog() as dlg:
            dlg.broadcast_abort()
            spy_send.assert_not_called()

            dlg.channel = "my_channel"
            dlg.broadcast_abort()
            spy_send.assert_called_once()
