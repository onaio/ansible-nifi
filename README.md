NiFi
====

[![Build Status](https://travis-ci.org/onaio/ansible-nifi.svg?branch=master)](https://travis-ci.org/onaio/ansible-nifi)

Use this role to install, configure, and manage Apache NiFi.
Role has been tested with NiFi versions 1.1.x, 1.2.0, 1.3.0 and 1.4.0.

Requirements
------------

  - `molecule[docker]` v3 or compatible

Role Variables
--------------

### Required Variables
    nifi_version

If `nifi_is_secure` is `True` you must also include
    nifi_key_pass
    nifi_keystore_pass
    nifi_truststore_pass

### Variables that determine the nifi install location, and their default values:

    nifi_base_dir: /opt/nifi
    nifi_etc_dir: /etc/nifi
    nifi_log_dir: /var/log/nifi
    nifi_pid_dir: /var/run/nifi

### Other Default variables are listed below:

    # Whether to install the nifi toolkit utilities (required for backup/restore)
    nifi_install_toolkit: True
    
    # whether to restart nifi after making changes; default is True, for a cluster you may wish to disable
    nifi_perform_restart: True
    
    # whether to force a restart, useful if another role has made changes (such as updating a custom nar); default is False
    nifi_force_restart: False
    
    # A complete list of IP addresses for each nodes within the nifi cluster
    nifi_nodes_list: []
    
    # nifi_extra_args is a list of key/value pairs that are made available in NiFi, for example:
    nifi_extra_args:
      - file.encoding: "UTF-8"
      - environment: "{{ env }}"
    
    # List of directories for nifi to look in for additional nars.
    nifi_custom_nars: []
        
    nifi_node_jvm_memory: '1024m'
    nifi_java_command: 'java'
    
    # defaults file / directories for nifi
    nifi_database_repository: "{{ nifi_home }}/database_repository"
    nifi_flowfile_repository: "{{ nifi_home }}/flowfile_repository"
    nifi_content_repositories: [ "{{ nifi_home }}/content_repository" ]
    nifi_provenance_repositories: [ "{{ nifi_home }}/provenance_repository" ]
    
    # NiFi cluster settings
    nifi_single_node: True
    nifi_input_socket_host:
    nifi_input_socket_port:
    nifi_cluster_node_protocol_port:
    nifi_web_http_host: 127.0.0.1
    nifi_web_http_port: 8080
    
    # Queue swap settings
    nifi_queue_swap_threshold: 20000
    nifi_swap_in_threads: 1
    nifi_swap_out_threads: 4
    
    # Content Repository Settings
    nifi_content_claim_max_flow_files: 100
    nifi_content_claim_max_appendable_size: '10 MB'
    nifi_content_archive_max_retention_period: '12 hours'
    nifi_content_archive_max_usage_percentage: '50%'
    nifi_content_archive_enabled: 'false'
    nifi_content_always_sync: 'false'
     
    # Provenance settings: PersistentProvenanceRepository or VolatileProvenanceRepository
    nifi_provenance_implementation: PersistentProvenanceRepository
    nifi_provenance_max_storage_time: '24 hours'
    nifi_provenance_max_storage_size: '1 GB'
    nifi_provenance_rollover_time: '30 secs'
    nifi_provenance_rollover_size: '100 MB'
    nifi_provenance_query_threads: 2
    nifi_provenance_index_threads: 2
    nifi_provenance_repository_buffer_size: 100000
    nifi_provenance_indexed_fields: EventType, FlowFileUUID, Filename, ProcessorID, Relationship
    
    # Status repository settings
    nifi_components_status_repository_buffer_size: 1440
    nifi_components_status_snapshot_frequency: '1 min'
    
    # NiFi zookeeper settings
    nifi_zookeeper_servers: []
    nifi_zookeeper_dir: /data/zookeeper
    nifi_state_management_embedded_zookeeper_start: False
    nifi_zookeeper_root_node: '/nifi'
    nifi_zookeeper_session_timeout: '10 seconds'
    nifi_zookeeper_autopurge_purgeInterval: 24
    nifi_zookeeper_autopurge_snapRetainCount: 30
    
    # Security settings
    nifi_initial_admin:
    nifi_is_secure: False
    
    # Logback logging levels and settings
    nifi_log_app_file_retention: 10
    nifi_log_user_file_retention: 10
    nifi_log_boot_file_retention: 10
    nifi_log_level_root: INFO
    nifi_log_level_org_apache_nifi: INFO
    nifi_log_level_org_apache_nifi_processors: WARN
    nifi_log_level_org_apache_nifi_processors_standard_LogAttribute: INFO
    nifi_log_level_org_apache_nifi_controller_repository: WARN
    nifi_log_level_org_apache_nifi_controller_repository_StandardProcessSession: WARN
    nifi_log_level_org_apache_nifi_cluster: INFO
    nifi_log_level_org_apache_nifi_server_JettyServer: INFO
    nifi_log_level_org_eclipse_jetty: INFO
    nifi_log_level_org_apache_nifi_web_security: INFO
    nifi_log_level_org_apache_nifi_web_api_config: INFO
    nifi_log_level_org_apache_nifi_authorization: INFO
    nifi_log_level_org_apache_nifi_cluster_authorization: INFO
    nifi_log_level_org_apache_nifi_bootstrap: INFO
    nifi_log_level_org_apache_nifi_bootstrap_Command: INFO
    nifi_log_level_org_apache_nifi_web_filter_RequestLogger: INFO
    nifi_log_level_org_wali: WARN
    nifi_custom_log_levels: []

## Backup / Restore

Backup/Restore via duplicity is enabled by default - daily backups are performed and stored locally without any other configuration.  The variable which controls this is:

```yaml
nifi_backup_enabled: True
```

> In order to do a clean backup of the flowfile repository the nifi service must be taken offline - the default time period to do this is midnight. 

To store backups in S3 instead, something like the following should be set:

```yaml
nifi_backup_target: "s3://{{ vault_s3_aws_access_key }}:{{ vault_s3_aws_secret_key }}@s3.eu-west-1.amazonaws.com/{{ project_name }}-nifi-backup"
nifi_backup_schedule: "0 0 * * 0"
nifi_backup_max_age: "7D"
```

See [Stouts.backup](https://github.com/Stouts/Stouts.backup) for more information about the options available.

When enabled, `nifi-backup.sh` and `nifi-restore.sh` scripts are installed in the system `$PATH` to manually trigger a backup or restore.

### Restoring on a new server

To restore nifi onto a clean server, first deploy the nifi role with the appropriate backup target, creating the restore script.  Then just run `nifi-restore.sh` on the new server.

> The variable `nifi_backup_id` controls which backup files in a bucket that a server will use - if there is only one host in the `nifi` group it will always be `0`.  A project can also explicitly set `nifi_backup_id` to something more meaningful - the idea is to support multi-nifi deployments easily in the future. 

Dependencies
------------

NiFi requires java and Stouts.backup

Example Playbook
----------------

Install and configure NiFi

    - name: Install NiFi
      hosts: servers
      vars: 
          nifi_log_level_root: WARN
          nifi_node_jvm_memory: '10240M'
          nifi_custom_nars: [ '/opt/extra-nars' ]
          nifi_single_node: False
          nifi_nodes_list: ['nifi-node-1', 'nifi-node-2']
          nifi_backup_target: "s3://{{ vault_s3_aws_access_key }}:{{ vault_s3_aws_secret_key }}@s3.eu-west-1.amazonaws.com/project-nifi-backup"
      roles:
        - role: nifi
          nifi_version: 1.2.0

License
-------

MIT

Authors
-------

Update by [Ona Engineering](https://ona.io)

Based on [ansible-role-nifi](https://github.com/Asymmetrik/ansible-role-nifi)
