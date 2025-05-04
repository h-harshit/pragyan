import logging
import logging.config

logging.config.fileConfig("common/logging_config.conf")

LOGGER = logging.getLogger("appLogger")
