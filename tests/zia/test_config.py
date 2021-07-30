from restfly.utils import check


def test_config_status(zia):
    status = zia.config.status()
    check("status", status, str)


def test_config_activation(zia):
    status = zia.config.activate()
    check("status", status, str)
