def test_logger(caplog):
    from guikit.logging import app_dir, logger

    msg = "Some function executed."

    def some_func():
        logger.info(msg)

    some_func()
    assert caplog.records[-1].levelname == "INFO"
    assert caplog.records[-1].message == msg

    log_dir = app_dir() / "logs"
    last_log = sorted(log_dir.glob("*.log"))[-1]
    with last_log.open() as f:
        log = list(f)

    assert "INFO" in log[-1]
    assert msg in log[-1]
