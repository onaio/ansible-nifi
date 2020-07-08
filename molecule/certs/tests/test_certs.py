import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ensure_emqtt_cert_directories_are_present(host):
    certs_dir = host.file("/etc/ssl/certs/emqtt")
    assert certs_dir.exists
    assert certs_dir.is_directory


def test_ensure_emqtt_keystore_and_truststore_are_present(host):
    keystore = host.file("/etc/ssl/certs/emqtt/keystore.pkcs12")
    truststore = host.file("/etc/ssl/certs/emqtt/truststore.jks")
    assert keystore.exists
    assert truststore.exists
