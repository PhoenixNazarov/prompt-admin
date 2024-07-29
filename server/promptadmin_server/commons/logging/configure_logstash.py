import logging

from logstash_async.formatter import LogstashFormatter
from logstash_async.transport import HttpTransport
from logstash_async.handler import AsynchronousLogstashHandler
from settings import SETTINGS


def configure_loggers():
    if SETTINGS.logstash_logger is None:
        return
    host = SETTINGS.logstash_logger.host
    port = SETTINGS.logstash_logger.port

    if host is None or port is None:
        return

    transport = HttpTransport(
        host,
        port,
        timeout=5.0,
        ssl_enable=False,
        username=SETTINGS.logstash_logger.username,
        password=SETTINGS.logstash_logger.password
    )

    environment = SETTINGS.logstash_logger.environment
    if environment is None:
        environment = 'development'


    # Setup defaults
    for name, source in SETTINGS.logstash_logger.system_loggers.items():
        logger = logging.getLogger(name)
        configure_logger(logger, host, port, transport, source, environment)

    for name, source in SETTINGS.logstash_logger.config_loggers.items():
        logger = logging.getLogger(name)
        configure_logger(logger, host, port, transport, source, environment)


def configure_logger(logger: logging.Logger, host: str, port: int, transport, source: str, environment: str, cmd=True):
    logger.setLevel(logging.INFO)

    handler = AsynchronousLogstashHandler(
        host,
        port,
        transport=transport,
        database_path=None
    )

    logstash_formatter = LogstashFormatter(
        message_type='python-logstash',
        extra_prefix='dev',
        extra=dict(
            application=SETTINGS.app,
            source=source,
            environment=environment
        )
    )

    handler.setFormatter(logstash_formatter)
    logger.addHandler(handler)
    if cmd:
        logger.addHandler(logging.StreamHandler())
