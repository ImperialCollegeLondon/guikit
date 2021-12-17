from typing import Optional

import wx
from pubsub import pub


class Dialog(wx.ProgressDialog):
    """Opens a modal progress dialog.

    This pogress dialog is pretty much identical to the wx.ProgressDialog it inherits
    except that it predefines the style of the dialog (making it modal, including an
    abort button, the elapsed and remaining time), and enables updating the progress -
    as well as informing of the abort condition - via the pubsub messaging system.

    For the pubsub messaging system, the dialog will be:

    - Subscribed to '<channel>.update_progress_dialog', with the same inputs as the
      progres dialog method 'Update': current step and, optionally, a new value for
      maximum and a message.
    - Broadcast the abort condition via '<channel>.abort_process' if the abort button is
      pressed, with no input arguments.

    If the 'channel' input argument is None, then the pubsub messaging system is not
    used.

    This dialog also gives finer control on when it should be updated - either the
    number of times it should be updated over the whole process in total or the number
    of steps that should happen after updating it. This is important because updating
    the progress dialog adds some overhead to the process, which might be significant if
    it is updated too often.

    Example of use:

    If the loop the dialog is informing about is immediately accessible, then a direct
    call to Update can be used. For example:

    ```python
    with Dialog() as dlg:
        for i in range(dlg.Range + 1):
            dlg.Update(i)
            # do something
    ```

    If that is not the case and the loop or recursive function is defined somewhere
    else, possibly in another module, then the messaging system can be used to
    communicate with the dialog:

    ```python
    def some_function():
        maximum=300
        pub.sendMessage("my_process.update_progress_dialog", value=0, maximum=maximum)
        for i in range(maximum + 1):
            pub.sendMessage("my_process.update_progress_dialog", value=i)
            # do something

    with Dialog(channel="my_process") as dlg:
        some_function()
    ```

    Args:
        - title: Title of the dialog window.
        - message: Brief message describing the process to be carried.
        - channel: Root channel in which to broadcast/listen for event using the pubsub
        package.
        - maximum: The maximum number of steps.
        - every: The number of steps required to update the dialog.
        - steps: The number of times the dialog will be updated in total. If provided,
        'every' is overwritten by the calculated new value based on the 'maximum' and
        the 'steps'.
    """

    def __init__(
        self,
        title: str = "",
        message: str = "",
        channel: Optional[str] = None,
        maximum=100,
        every: int = 1,
        steps: Optional[int] = None,
    ):
        super(Dialog, self).__init__(
            title,
            message,
            style=wx.PD_APP_MODAL
            | wx.PD_AUTO_HIDE
            | wx.PD_CAN_ABORT
            | wx.PD_ELAPSED_TIME
            | wx.PD_REMAINING_TIME,
            maximum=maximum,
        )
        self.channel = channel
        self.every = every
        self.steps = steps

        self.SetRange(maximum)
        self.subscribe_for_updates()

    def SetRange(self, maximum: int) -> None:
        """Sets a new maximum value for the progress dialog."""
        super(Dialog, self).SetRange(maximum)

        if self.steps is not None:
            self.every = maximum // min(maximum, self.steps)

    def Update(
        self,
        value: int,
        msg: str = "",
        maximum: Optional[int] = None,
    ) -> bool:
        """Updates the progress dialog.

        A meesage is broadcast via the <channel>.abort_process if the abort button is
        clicked and 'channel' was set.

        Args:
            - value: Current step in the process.
            - msg: Message to send to the dialog.
            - maxium: An optional new number of maximum steps.

        Raises:
            - ValueError if 'value' is not an integer or is larger than maximum.

        Returns:
            A bool value indicating if the process should NOT be cancelled.
            - True indicates that the process should continue normally.
            - False indicates that the process should be halted.
        """
        if maximum is not None:
            self.SetRange(maximum)

        if type(value) != int:
            raise ValueError("The new 'value' must be an integer")
        elif value > self.Range:
            raise ValueError(
                f"Current step larger than the maximum: {value}>{self.Range}"
            )

        if not self.IsShownOnScreen():
            self.Show()

        if (value % self.every) != 0:
            return True

        msg = f"{value}/{self.Range}" if msg == "" else f"{msg} - {value}/{self.Range}"
        continue_progress, _ = super(Dialog, self).Update(value, msg)

        if not continue_progress:
            self.broadcast_abort()

        return continue_progress

    def subscribe_for_updates(self) -> None:
        """Subscribe the Update method to the relevant pubsub channel."""
        if self.channel is None:
            return

        pub.subscribe(self.Update, f"{self.channel}.update_progress_dialog")

    def broadcast_abort(self) -> None:
        """Broadcast the message that the process should be aborted."""
        if self.channel is None:
            return

        pub.sendMessage(f"{self.channel}.abort_process")
