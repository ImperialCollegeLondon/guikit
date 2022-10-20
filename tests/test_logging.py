def test_logger(caplog):
    from platformdirs import user_log_path

    from guikit import APP_NAME
    from guikit.logging import logger

    msg = "Some function executed."

    def some_func():
        logger.info(msg)

    some_func()
    assert caplog.records[-1].levelname == "INFO"
    assert caplog.records[-1].message == msg

    last_log = sorted(user_log_path(APP_NAME).glob("*.log"))[-1]
    with last_log.open() as f:
        log = list(f)

    assert "INFO" in log[-1]
    assert msg in log[-1]
