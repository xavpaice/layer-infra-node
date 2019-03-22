import glob
import os
import shutil

from charmhelpers.core import hookenv, host
from charmhelpers.contrib.charmsupport import nrpe


class InfranodeHelper():
    def __init__(self):
        self.charm_config = hookenv.config()

    def action_function(self):
        ''' An example function for calling from an action '''
        return

    def add_nrpe_pacemaker(self, nrpe_setup, hostname):
        """Create NRPE checks for Corosync/Pacemaker

        :param nrpe_setup: nrpe.NRPE object
        :param hostname: hostname defined in nrpe
        :return: None
        """
        scripts_src = os.path.join(os.environ["CHARM_DIR"], "files",
                                   "nrpe")
        scripts_dst = "/usr/local/lib/nagios/plugins"
        if not os.path.exists(scripts_dst):
            os.makedirs(scripts_dst)
        for fname in glob.glob(os.path.join(scripts_src, "*")):
            if os.path.isfile(fname):
                shutil.copy2(fname,
                             os.path.join(scripts_dst, os.path.basename(fname)))

        sudoers_src = os.path.join(os.environ["CHARM_DIR"], "files",
                                   "sudoers")
        sudoers_dst = "/etc/sudoers.d"
        for fname in glob.glob(os.path.join(sudoers_src, "*")):
            if os.path.isfile(fname):
                shutil.copy2(fname,
                             os.path.join(sudoers_dst, os.path.basename(fname)))
        # corosync/crm checks
        nrpe_setup.add_check(
            'corosync_rings',
            'Check Corosync rings {}'.format(hostname),
            'check_corosync_rings')
        nrpe_setup.add_check(
            'crm_status',
            'Check crm status {}'.format(hostname),
            'check_crm')

        # process checks
        nrpe_setup.add_check(
            'corosync_proc',
            'Check Corosync process {}'.format(hostname),
            'check_procs -c 1:1 -C corosync'
        )
        nrpe_setup.add_check(
            'pacemakerd_proc',
            'Check Pacemakerd process {}'.format(hostname),
            'check_procs -c 1:1 -C pacemakerd'
        )
        nrpe_setup.write()

    def add_nrpe_disabled_juju(self, nrpe_setup):
        """Create NRPE checks for Juju commands

        We try to run Juju models with all commands disabled for safety.  This adds a NRPE check to ensure that is
        the case, will alert if commands are enabled.

        :param nrpe_setup: nrpe.NRPE object
        :return: None
        """
        nrpe_setup.add_check(
            'juju_disabled_commands',
            'Check that Juju commands are disabled',
            '/usr/local/lib/nagios/plugins/check_juju_disabled_commands -f /home/jujumanage/juju_commands_state.txt'
        )
        nrpe_setup.write()
        command = "/snap/bin/juju disabled-commands > ${HOME?}/juju_commands_state.txt"
        cronjob_cmd = (" * * * * * jujumanage timeout -k 10s -s SIGINT 60 "
                       "{command} 2>&1 | logger -p local0.notice\n")
        cronjob = cronjob_cmd.format(command=command)
        host.write_file('/etc/cron.d/juju_disabled_commands', cronjob)

    def create_nrpe_checks(self, nrpe_setup, hostname, current_unit):
        config = hookenv.config()
        services = ['maas-dhcpd', 'maas-rackd', 'bind9']
        nrpe.add_init_service_checks(nrpe_setup, services, current_unit)
        nrpe_setup.write()
        charm_file_dir = os.path.join(hookenv.charm_dir(), 'files')
        charm_plugin_dir = os.path.join(charm_file_dir, 'plugins')
        host.rsync(
            charm_plugin_dir,
            '/usr/local/lib/nagios/',
            options=['--executability']
            )

        if config.get('nagios_alert_if_juju_enabled'):
            self.add_nrpe_disabled_juju(nrpe_setup)
        if config.get('nagios_check_pacemaker'):
            self.add_nrpe_pacemaker(nrpe_setup, hostname)

        hookenv.status_set('active', 'NRPE configured')
