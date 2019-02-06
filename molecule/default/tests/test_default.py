import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service(host):
    pkg = host.service("nifi")

    assert pkg.is_running
    # assert pkg.version.startswith("")


def test_deployed_service(host):
    assert host.socket("tcp://0.0.0.0:8080").is_listening