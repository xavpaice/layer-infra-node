from charms.reactive import when, when_not, set_flag
from charmhelpers import fetch
from charmhelpers.contrib.charmsupport import nrpe
from lib_infra_node import InfranodeHelper

helper = InfranodeHelper()


@when_not('infra-node.installed')
def install_infra_node():
    set_flag('infra-node.installed')


@when('nrpe-external-master.available')
def update_nrpe_config():
    # python-dbus is used by check_upstart_job
    fetch.apt_install('python-dbus', fatal=True)
    hostname = nrpe.get_nagios_hostname()
    current_unit = nrpe.get_nagios_unit_name()
    nrpe_setup = nrpe.NRPE(hostname=hostname)
    helper.create_nrpe_checks(nrpe_setup, hostname, current_unit)
