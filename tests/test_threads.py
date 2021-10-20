from unittest.mock import MagicMock, patch

from pytest import mark


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
