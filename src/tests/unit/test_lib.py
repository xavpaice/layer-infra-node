#!/usr/bin/python3


class TestLib():
    def test_pytest(self):
        assert True

    def test_infranode(self, infranode):
        """See if the helper fixture works to load charm configs """
        assert isinstance(infranode.charm_config, dict)

    # Include tests for functions in lib_infra_node

    def test_add_nrpe_pacemaker(self, infranode, mock_nrpe_setup, mock_environ, mock_os_makedirs, mock_shutil_copy2):
        infranode.add_nrpe_pacemaker(mock_nrpe_setup, 'unittest')
        mock_nrpe_setup.add_check.assert_called()
        mock_nrpe_setup.write.assert_called()

    def test_add_nrpe_disabled_juju(self, infranode, mock_nrpe_setup, mock_host_write_file):
        infranode.add_nrpe_disabled_juju(mock_nrpe_setup)
        mock_nrpe_setup.add_check.assert_called()
        mock_nrpe_setup.write.assert_called()

    def test_create_nrpe_checks(self, infranode, mock_nrpe_setup, mock_rsync):
        infranode.create_nrpe_checks(mock_nrpe_setup, 'mock_hostname', 'mock_unit/0')
        mock_nrpe_setup.add_check.assert_called()
        mock_nrpe_setup.write.assert_called()
