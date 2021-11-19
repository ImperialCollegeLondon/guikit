from unittest.mock import MagicMock, patch

from pytest import mark, raises


def test_thread_result():
    from pyguitemp.threads import ThreadResult

    result = ThreadResult("some data", 1)
    assert result.data == "some data"
    assert result.GetEventType() == 1


class TestWorkerThread:
    def test_connect_events(self, window):
        from pyguitemp.threads import WorkerThread

        window.Connect = MagicMock()
        worker = WorkerThread(lambda: None)

        worker.connect_events(window)
        assert window.Connect.call_count == 3

    def test_run(self):
        class Pool:
            post_event = MagicMock()

        with patch("pyguitemp.threads.ThreadResult", MagicMock()), patch(
            "pyguitemp.threads.ThreadPool", Pool
        ):
            from pyguitemp.threads import ThreadResult, WorkerThread

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
        from pyguitemp.threads import WorkerThread

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


class TestThreadPool:
    def test_run_thread(self, window):
        class Worker:
            ident = 42
            abort = False
            connect_events = MagicMock()
            start = MagicMock()

        with patch("pyguitemp.threads.WorkerThread", MagicMock(return_value=Worker)):
            from pyguitemp.threads import ThreadPool

            pool = ThreadPool(window)
            pool.run_thread(lambda: None)

        assert Worker.ident in pool._workers

    def test_query_abort(self, window):
        import threading

        class Worker:
            ident = threading.get_ident()
            abort = False
            connect_events = MagicMock()
            start = MagicMock()

        with patch("pyguitemp.threads.WorkerThread", MagicMock(return_value=Worker)):
            from pyguitemp.threads import ThreadPool

            pool = ThreadPool(window)
            pool.run_thread(lambda: None)

        assert not pool.query_abort()

    def test_abort_thread(self, window):
        import threading

        class Worker:
            ident = threading.get_ident()
            abort = False
            connect_events = MagicMock()
            start = MagicMock()

        with patch("pyguitemp.threads.WorkerThread", MagicMock(return_value=Worker)):
            from pyguitemp.threads import ThreadPool

            pool = ThreadPool(window)
            ident = pool.run_thread(lambda: None)

        pool.abort_thread(ident)
        assert pool._workers[ident].abort

    def test_post_event(self, window):
        class WX:
            PostEvent = MagicMock()

        with patch("pyguitemp.threads.wx", WX):
            from pyguitemp.threads import ThreadPool

            pool = ThreadPool(window)
            pool.post_event(None)
            WX.PostEvent.assert_called_once()


def test_run_in_thread():
    with patch("pyguitemp.threads.ThreadPool", MagicMock()):
        from pyguitemp.threads import ThreadPool, run_in_thread

        def target():
            pass

        run_in_thread(target)
        assert ThreadPool().run_thread.call_count == 1
        ThreadPool().run_thread.assert_called_once_with(target, None, None, None, None)


def test_run_daemon():
    with patch("pyguitemp.threads.ThreadPool", MagicMock()):
        from pyguitemp.threads import ThreadPool, run_daemon

        run_daemon(lambda: None)
        ThreadPool().run_daemon_called_once_with(None, None, None, None, True)


def test_abort_thread():
    window = MagicMock()

    class Worker:
        ident = 123
        abort = False
        connect_events = MagicMock()
        start = MagicMock()

    with patch("pyguitemp.threads.WorkerThread", MagicMock(return_value=Worker)), patch(
        "pyguitemp.threads.logger", MagicMock()
    ):

        from pyguitemp.threads import ThreadPool, abort_thread, logger, should_abort

        pool = ThreadPool(window)
        pool.run_thread(lambda: None)
        abort_thread(123)
        assert should_abort(123) is True

        with raises(KeyError) as key_err:
            abort_thread(124)
        key_err_str = str(key_err.value)
        assert "Thread with index: 124 is not in the ThreadPool." in key_err_str
        assert logger.exception.call_count == 1

        with raises(KeyError) as key_err:
            should_abort(125)
        key_err_str = str(key_err.value)
        assert "Thread with index: 125 is not in the ThreadPool." in key_err_str
        assert logger.exception.call_count == 2
