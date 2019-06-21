import collections
import logging
import os
import toml

from sawtooth_sdk.processor.exceptions import LocalConfigurationError

LOGGER = logging.getLogger(__name__)


def load_default_med_config():
    return MedConfig(
        connect = 'tcp://127.0.0.1:4004'
    )


def load_toml_med_config(filename):
    if not os.path.exists(filename):
        LOGGER.info(
            "Skipping transaction proccesor config loading from non-existent"
            " config file: %s", filename)
        return MedConfig()

    LOGGER.info("Loading transaction processor information from config: %s",filename)

    try:
        with open(filename) as fd:
            raw_config = fd.read()
    except IOError as e:
        raise LocalConfigurationError(
            "Unable to load transaction processor configuration file:"
            " {}".format(str(e)))

    toml_config = toml.loads(raw_config)
    invalid_keys = set(toml_config.keys()).difference(
        ['connect'])
    if invalid_keys:
        raise LocalConfigurationError(
            "Invalid keys in transaction processor config: "
            "{}".format(", ".join(sorted(list(invalid_keys)))))

    config = MedConfig(
        connect=toml_config.get("connect", None)
    )

    return config


def merge_med_config(configs):

    connect = None

    for config in reversed(configs):
        if config.connect is not None:
            connect = config.connect

    return MedConfig(
        connect=connect
    )


class MedConfig:
    def __init__(self, connect=None):
        self._connect = connect

    @property
    def connect(self):
        return self._connect

    def __repr__(self):
        return \
            "{}(connect={})".format(
                self.__class__.__name__,
                repr(self._connect),
            )

    def to_dict(self):
        return collections.OrderedDict([
            ('connect', self._connect),
        ])

    def to_toml_string(self):
        return str(toml.dumps(self.to_dict())).strip().split('\n')
