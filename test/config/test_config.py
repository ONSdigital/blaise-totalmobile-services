from config import Config, ConfigError
import pytest


def test_config_validate():
    config = Config("foo", "bar", "fwibble", "fish")
    config.validate()


def test_config_validate_err():
    config = Config("", "", "fwibble", "fish")
    with pytest.raises(ConfigError) as err:
        config.validate()
    assert (
        str(err.value)
        == "Config fields not set: ['totalmobile_url', 'totalmobile_instance']"
    )
