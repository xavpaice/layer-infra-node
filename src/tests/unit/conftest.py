#!/usr/bin/python3

import mock
import pytest


# If layer options are used, add this to infranode
# and import layer in lib_infra_node
@pytest.fixture
def mock_layers(monkeypatch):
    import sys
    sys.modules['charms.layer'] = mock.Mock()
    sys.modules['reactive'] = mock.Mock()
    # Mock any functions in layers that need to be mocked here

    def options(layer):
        # mock options for layers here
        if layer == 'example-layer':
            options = {'port': 9999}
            return options
        else:
            return None

    monkeypatch.setattr('lib_infra_node.layer.options', options)


@pytest.fixture
def mock_hookenv_config(monkeypatch):
    import yaml

    def mock_config():
        cfg = {}
        yml = yaml.load(open('./config.yaml'))

        # Load all defaults
        for key, value in yml['options'].items():
            cfg[key] = value['default']

        # Manually add cfg from other layers
        # cfg['my-other-layer'] = 'mock'
        return cfg

    monkeypatch.setattr('lib_infra_node.hookenv.config', mock_config)


@pytest.fixture
def mock_remote_unit(monkeypatch):
    monkeypatch.setattr('lib_infra_node.hookenv.remote_unit', lambda: 'unit-mock/0')


@pytest.fixture
def mock_charm_dir(monkeypatch):
    monkeypatch.setattr('lib_infra_node.hookenv.charm_dir', lambda: '/mock/charm/dir')


@pytest.fixture
def infranode(tmpdir, mock_hookenv_config, mock_charm_dir, monkeypatch):
    from lib_infra_node import InfranodeHelper
    helper = InfranodeHelper()

    # Example config file patching
    cfg_file = tmpdir.join('example.cfg')
    with open('./tests/unit/example.cfg', 'r') as src_file:
        cfg_file.write(src_file.read())
    helper.example_config_file = cfg_file.strpath

    # Any other functions that load helper will get this version
    monkeypatch.setattr('lib_infra_node.InfranodeHelper', lambda: helper)

    return helper


@pytest.fixture
def mock_nrpe_setup(monkeypatch):
    mocked_nrpe_setup = mock.MagicMock()
    mocked_nrpe_setup.add_check.return_value = True
    mocked_nrpe_setup.write.return_value = True
    mocked_nrpe_setup.add_init_service_checks.return_value = True
    monkeypatch.setattr('charmhelpers.contrib.charmsupport.nrpe', mocked_nrpe_setup)
    return mocked_nrpe_setup


@pytest.fixture
def mock_host_write_file(monkeypatch):
    mocked_host_write_file = mock.Mock()
    monkeypatch.setattr('charmhelpers.core.host.write_file', mocked_host_write_file)
    return mocked_host_write_file


@pytest.fixture
def mock_environ(monkeypatch):
    environment_vars = {'CHARM_DIR': '.'}
    monkeypatch.setattr('os.environ',  environment_vars)


@pytest.fixture
def mock_os_makedirs(monkeypatch):
    def makedirs(dirs):
        return True
    monkeypatch.setattr('os.makedirs', makedirs)


@pytest.fixture
def mock_shutil_copy2(monkeypatch):
    def copy2(src, dst):
        return True
    monkeypatch.setattr('shutil.copy2', copy2)


@pytest.fixture
def mock_rsync(monkeypatch):
    def rsync(src, dst, **kwargs):
        return True
    monkeypatch.setattr('charmhelpers.core.host.rsync', rsync)
