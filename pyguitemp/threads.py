"""
Contains all the machinery for dealing with threads.
"""
from __future__ import annotations

import threading
from typing import Any, Callable, Dict, Optional

import wx

from .logging import logger


class ThreadResult(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data: Any, event_type: int):
        """Initialises a result event for the thread.

        Args:
            data: The data to be passed to the main thread.
            event_type: The type of event.
        """
        wx.PyEvent.__init__(self)
        self.SetEventType(event_type)
        self.data = data


class WorkerThread(threading.Thread):
    """Worker Thread Class."""

    def __init__(
        self,
        target: Callable,
        on_abort: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        daemon: Optional[bool] = None,
    ):
        """Configures and start a new thread executing the target action.

        Args:
            target: The function to be executed
            on_abort: Function to be called if the thread aborts. Takes as only argument
                the output of the target function when that one aborts.
            on_complete: Function to be called if the thread finished normally. Takes as
                only argument the output of the target function when that one finishes.
            on_error: Function to be called if anything bad happens in the thread. Takes
                as only argument the exception catched.
        """
        super(WorkerThread, self).__init__(target=target, daemon=daemon)
        self._on_abort = on_abort
        self._on_complete = on_complete
        self._on_error = on_error
        self._event_on_abort = wx.NewEventType()
        self._event_on_complete = wx.NewEventType()
        self._event_on_error = wx.NewEventType()
        self.abort = False

    def connect_events(self, window: wx.Frame) -> None:
        """Connect the complete, abort and error events to the functions to execute.

        Args:
            window: The main window of the program.
        """
        window.Connect(-1, -1, self._event_on_abort, self.on_abort)
        window.Connect(-1, -1, self._event_on_complete, self.on_complete)
        window.Connect(-1, -1, self._event_on_error, self.on_error)

    def run(self):
        """Run worker thread and deals with the wrapping up accordingly."""
        try:
            result = self._target()

            if self.abort:
                ThreadPool().post_event(ThreadResult(result, self._event_on_abort))
            else:
                ThreadPool().post_event(ThreadResult(result, self._event_on_complete))

        except Exception as err:
            ThreadPool().post_event(ThreadResult(err.args[0], self._event_on_error))

    def on_abort(self, event: ThreadResult):
        """To execute when the thread execution is aborted.

        Args:
            event: The event object with the relevant output data
        """
        if self._on_abort is not None:
            self._on_abort(event.data)

    def on_complete(self, event: ThreadResult):
        """To execute when the thread execution is completed normally.

        Args:
            event: The event object with the relevant output data
        """
        if self._on_complete is not None:
            self._on_complete(event.data)

    def on_error(self, event: ThreadResult):
        """To execute when the thread ends with an error.

        Args:
            event: The exception raised
        """
        if self._on_error is not None:
            self._on_error(event.data)


class ThreadPool:

    _instance: Optional[ThreadPool] = None

    def __new__(cls, window: Optional[wx.Frame] = None):
        if window is None and cls._instance is None:
            raise ValueError(
                "The first time it is called, 'window' must be a wx.Frame object."
            )
        elif cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._window = window
            cls._instance._workers = {}
        return cls._instance

    def __init__(self, window: Optional[wx.Frame] = None):
        self._window: wx.Frame
        self._workers: Dict[int, WorkerThread]

    def run_thread(
        self,
        target: Callable,
        on_abort: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        daemon: Optional[bool] = None,
    ) -> int:
        """Runs a new thread executing the target callable on it.

        The thread will run until:
            - The 'target' function returns
            - An exception is raised

        The target function might finish because it has completed what it was doing. In
        that case, 'on_complete' is executed after returning from `target`.

        It might also finish because it is monitoring the value of
        `ThreadPool().query_abort()` and this is `True`. In that case, target should
        return with an appropriate value and `on_abort` is then executed.

        Finally, an exception might occur in the thread. In this case, the exception
        is caught and `on_error` is executed.

        `on_complete`, `on_abort` and `on_error` are all executed in the main thread.

        Args:
            target: The function to be executed in a separate thread.
            on_abort: The function to be executed when the target function is aborted.
                Takes as input the value returned by target.
            on_complete: The function to be executed when the target function is
                completed normally. Takes as input the value returned by target.
            on_error: The function to be executed when an exception is raised in the
                target. Takes as input the exception raised.
            daemon: If the function is a daemonic function.

        Returns:
            The id number for the thread, needed if it is to be aborted externally.
        """
        thread = WorkerThread(target, on_abort, on_complete, on_error, daemon)
        thread.connect_events(self._window)
        thread.start()
        self._workers[thread.ident] = thread
        return thread.ident

    def query_abort(self) -> bool:
        """Check if the current thread is to be aborted.

        Raises:
            KeyError: If the thread identifier is not in the ThreadPool
        """
        ident: int = threading.get_ident()

        try:
            return self._workers[ident].abort
        except KeyError as key_err:
            key_err_ = KeyError(f"Thread with index: {ident} is not in the ThreadPool.")
            logger.exception(key_err_)
            raise key_err_ from key_err

    def abort_thread(self, ident: int) -> None:
        """Flag the thread with `ident` to be aborted.

        Args:
            ident: Thread identifier

        Raises:
            KeyError: If the thread identifier is not in the ThreadPool
        """
        try:
            self._workers[ident].abort = True
        except KeyError as key_err:
            key_err_ = KeyError(f"Thread with index: {ident} is not in the ThreadPool.")
            logger.exception(key_err_)
            raise key_err_ from key_err

    def post_event(self, event: ThreadResult):
        """Adds an event to the event loop of the main thread."""
        wx.PostEvent(self._window, event)


def run_in_thread(
    target: Callable,
    on_abort: Optional[Callable] = None,
    on_complete: Optional[Callable] = None,
    on_error: Optional[Callable] = None,
    daemon: Optional[bool] = None,
) -> int:
    """Is an alias for ThreadPool().run_thread(...)."""
    return ThreadPool().run_thread(target, on_abort, on_complete, on_error, daemon)


def run_daemon(
    target: Callable,
    on_abort: Optional[Callable] = None,
    on_complete: Optional[Callable] = None,
    on_error: Optional[Callable] = None,
) -> int:
    """Is an alias for ThreadPool().run_thread(..., daemon=True)."""
    return ThreadPool().run_thread(target, on_abort, on_complete, on_error, daemon=True)


def abort_thread(ident: int) -> None:
    """Set thread with given identifier to abort.

    Args:
        ident: Thread identifier
    """
    ThreadPool().abort_thread(ident)


def should_abort() -> bool:
    """Return whether the thread with given identifier should abort or not."""
    return ThreadPool().query_abort()
