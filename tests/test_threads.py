from unittest.mock import MagicMock, patch

from pytest import mark, raises


def test_thread_result():
    from guikit.threads import ThreadResult

    result = ThreadResult("some data", 1)
    assert result.data == "some data"
    assert result.GetEventType() == 1


class TestWorkerThread:
    def test_connect_events(self, window):
        from guikit.threads import WorkerThread

        window.Connect = MagicMock()
        worker = WorkerThread(lambda: None)

        worker.connect_events(window)
        assert window.Connect.call_count == 3

    def test_run(self):
        class Pool:
            post_event = MagicMock()

        with patch("guikit.threads.ThreadResult", MagicMock()), patch(
            "guikit.threads.ThreadPool", Pool
        ):
            from guikit.threads import ThreadResult, WorkerThread

            result = "some result"
            worker = WorkerThread(lambda: result)

            worker.run()
            ThreadResult.assert_called_once_with(result, worker._event_on_complete)
            ThreadResult.reset_mock()

            worker.abort = True
            worker.run()
            ThreadResult.assert_called_once_with(result, worker._event_on_abort)
            ThreadResult.reset_mock()

            def error():
                raise ValueError("Error msg")

            worker = WorkerThread(error)
            worker.run()
            ThreadResult.assert_called_once_with("Error msg", worker._event_on_error)

    @mark.parametrize("callback", ["on_abort", "on_complete", "on_error"])
    def test_callbacks(self, callback):
        from guikit.threads import WorkerThread

        class Event:

            _data = MagicMock()

            @property
            def data(self):
                return self._data()

        event = Event()
        worker = WorkerThread(lambda: None)
        getattr(worker, callback)(event)
        event._data.assert_not_called()

        worker = WorkerThread(lambda: None, **{callback: MagicMock()})
        getattr(worker, callback)(event)
        event._data.assert_called_once()


class Worker:
    ident = 42
    abort = False
    connect_events = MagicMock()
    start = MagicMock()


class TestThreadPool:
    def test_run_thread(self, window):

        with patch("guikit.threads.WorkerThread", MagicMock(return_value=Worker)):
            from guikit.threads import ThreadPool

            pool = ThreadPool(window)
            pool.run_thread(lambda: None)

        assert Worker.ident in pool._workers

    def test_query_abort(self, window):
        with patch(
            "guikit.threads.WorkerThread", MagicMock(return_value=Worker)
        ), patch("guikit.threads.logger", MagicMock()), patch(
            "guikit.threads.threading.get_ident",
            MagicMock(return_value=Worker.ident + 1),
        ):
            from guikit.threads import ThreadPool, logger

            pool = ThreadPool(window)

            with raises(KeyError) as key_err:
                pool.query_abort()

            key_err_str = str(key_err.value)
            assert (
                f"Thread with index: {Worker.ident+1} is not in the ThreadPool."
                in key_err_str
            )
            assert logger.exception.call_count == 1

    def test_abort_thread(self, window):
        with patch(
            "guikit.threads.WorkerThread", MagicMock(return_value=Worker)
        ), patch("guikit.threads.logger", MagicMock()):
            from guikit.threads import ThreadPool, logger

            pool = ThreadPool(window)

            with raises(KeyError) as key_err:
                pool.abort_thread(Worker.ident + 1)
            key_err_str = str(key_err.value)
            assert (
                f"Thread with index: {Worker.ident+1} is not in the ThreadPool."
                in key_err_str
            )
            assert logger.exception.call_count == 1

        pool.abort_thread(Worker.ident)
        assert pool._workers[Worker.ident].abort

    def test_post_event(self, window):
        class WX:
            PostEvent = MagicMock()

        with patch("guikit.threads.wx", WX):
            from guikit.threads import ThreadPool

            pool = ThreadPool(window)
            pool.post_event(None)
            WX.PostEvent.assert_called_once()


def test_run_in_thread():
    with patch("guikit.threads.ThreadPool", MagicMock()):
        from guikit.threads import ThreadPool, run_in_thread

        def target():
            pass

        run_in_thread(target)
        assert ThreadPool().run_thread.call_count == 1
        ThreadPool().run_thread.assert_called_once_with(target, None, None, None, None)


def test_run_daemon():
    with patch("guikit.threads.ThreadPool", MagicMock()):
        from guikit.threads import ThreadPool, run_daemon

        run_daemon(lambda: None)
        ThreadPool().run_daemon_called_once_with(None, None, None, None, True)


def test_abort_thread():
    with patch("guikit.threads.ThreadPool", MagicMock()):
        from guikit.threads import ThreadPool, abort_thread

        abort_thread(43)
        ThreadPool().abort_thread.called_once_with(43)


def test_should_abort():
    with patch("guikit.threads.ThreadPool", MagicMock()):
        from guikit.threads import ThreadPool, should_abort

        should_abort()
        ThreadPool().query_abort.called_once_with()
