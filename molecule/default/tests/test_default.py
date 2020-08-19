import os
import time

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service(host):
    pkg = host.service("nifi")

    assert pkg.is_running
    assert pkg.is_enabled


def test_deployed_service(host):
    time.sleep(120)
    assert host.socket("tcp://127.0.0.1:8080").is_listening


def test_file_permissions(host):
    nifiVersion = "1.11.4"
    nifiBaseDirName = "/opt/nifi"
    nifiInstalledVerDir = nifiBaseDirName + "/nifi-" + nifiVersion

    appCurrentVersionDir = host.file(nifiBaseDirName + "/nifi-current")
    assert appCurrentVersionDir.exists
    assert appCurrentVersionDir.user == "nifi"
    assert appCurrentVersionDir.group == "nifi"
    assert appCurrentVersionDir.is_symlink
    assert appCurrentVersionDir.linked_to == nifiInstalledVerDir

    appInstalledVersionDir = host.file(nifiInstalledVerDir)
    assert appInstalledVersionDir.exists
    assert appInstalledVersionDir.user == "nifi"
    assert appInstalledVersionDir.group == "nifi"
    assert appInstalledVersionDir.is_directory
    assert oct(appInstalledVersionDir.mode) == "0o755"
