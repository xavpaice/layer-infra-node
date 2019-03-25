# Overview

This charm provides a principal Juju unit so that we relate things like nrpe,
landscape-client, etc., to service the hosts used to provide Maas and other
infrastructure for a cloud installation.

# Usage

First, ensure you have ssh keys exchanged or passwords for a user with sudo on
the Maas host you wish to add.  You will need to confirm you can ssh from the
CLI you're working on and from the Juju controller machines.  Let's assume that
our ssh url is ubuntu@10.245.88.140.  Add the machine:
```
juju add-machine ssh:ubuntu@10.245.88.140
```

In this case, that came back as machine number 14.

Now deploy the charm:
```
juju deploy cs:~canonical-bootstack/infra-node --to 14
```

Now you can add relations etc to have nrpe.

# TODO

There's opportunities here to deliver some of the currently manual steps for
general day to day maintenance for a cloud.  The base stuff we're including
with this charm is just a few snaps, but we can be much more ambitious in the
future.

# Bugs


https://bugs.launchpad.net/layer-infra-node