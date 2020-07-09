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

    # Nifi custom scripts repositories. An array
    nifi_git_scripts:
     - git_repo: # The repository to download from
       git_branch: # The branch/version to download
       git_key: # Optional ssh key to use to clone the repository
       destination: # the destination in the Nifi Home folder to copy the downloaded repository to

    # NiFi parameter contexts
    nifi_set_parameter_contexts: true
    nifi_java_home: /usr/lib/jvm/java-8-openjdk-amd64/jre
    nifi_all_parameter_contexts_result_file: /tmp/all_parameter_contexts_result.json
    nifi_api_base_url: http://localhost:8080/nifi-api
    nifi_parameter_contexts:
    nifi_emqtt_certificate_authority_cert:
    nifi_emqtt_certificate_authority_key:
    nifi_emqtt_secure_password:
    nifi_emqtt_cert_dir:
    nifi_create_mqtt_certs: false
    certificate_attributes: "/C=SC/ST=Some State/L=Some City/O=Some Company/OU=Some Department/CN=example.com"

Setting Parameter Contexts
--------------------------

You can set NiFi parameter contexts like so:

```yml
nifi_set_parameter_contexts: true
nifi_java_home: /usr/lib/jvm/java-8-openjdk-amd64/jre
nifi_all_parameter_contexts_result_file: /tmp/all_parameter_contexts_result.json
nifi_api_base_url: http://localhost:8080/nifi-api
nifi_parameter_contexts:
  - name: "Test Group"
    description: "Just testing"
    parameters:
      - name: "variable1"  # this is the parameter name
        description: "what is this?"  # this is the parameter description
        value: "secret"  # this is the parameter value
        sensitive: "true"  # this indicates if the parameter is sensitive - either "true" or "false"
      - name: "variable2"
        description: "what is this?"
        value: "secret"
        sensitive: "true"  # either "true" or "false"
```

The above will create a parameter context named "Test Group" which will then have the variables "variable1" and "variable2" with values as defined above.

Backup / Restore
----------------

Backup/Restore via duplicity is enabled by default - daily backups are performed and stored locally without any other configuration.  The variable which controls this is:

```yaml
nifi_backup_enabled: True
```

> By default, unsafe backups are taken of nifi at midnight system time every day.  Because nifi stays online, there is a small chance the flowfiles or even the flows
> could be corrupted in the backup if they're being modified at the same time.
> In order to do a safe backup of the flowfile repository the nifi service must be taken offline - this is disruptive so is scheduled for just once-a-week.
> The default time period to do safe backups is every Monday at 9PM system time, which is a weekday and outside working hours in most of the world assuming GMT.
> To disable safe backups set `nifi_safe_backup_schedule` to `false` or `null`.

To store backups in S3 instead, something like the following should be set:

```yaml
nifi_backup_target: "s3://{{ vault_s3_aws_access_key }}:{{ vault_s3_aws_secret_key }}@s3.eu-west-1.amazonaws.com/{{ project_name }}-nifi-backup"
nifi_backup_schedule: "0 0 * * *" # Midnight
nifi_backup_max_age: "7D"

nifi_safe_backup_schedule: "0 21 * * 1" # 9PM Monday
nifi_safe_backup_max_age: "30D"
```

See [Stouts.backup](https://github.com/Stouts/Stouts.backup) for more information about the options available.

When enabled, `nifi-backup.sh` and `nifi-restore.sh` scripts are installed in the system `$PATH` to manually trigger a backup or restore.

### Restoring on a new server

To restore nifi onto a clean server, first deploy the nifi role with the appropriate backup target, creating the restore script.  Then just run `nifi-restore.sh` on the new server.

> The variable `nifi_backup_id` controls which backup files in a bucket that a server will use - if there is only one host in the `nifi` group it will always be `0`.  A project can also explicitly set `nifi_backup_id` to something more meaningful - the idea is to support multi-nifi deployments easily in the future. 

Creating EMQTT truststore and keystore
--------------------------------------
The KeyStore is used for client(NiFi) authentication to the emqtt server, while the TrustStore is used to authenticate NiFi server in SSL authentication with the emqtt server.

These two can be generated by setting the following variables:

```yml
    nifi_create_mqtt_certs: true
    nifi_emqtt_certificate_authority_cert: "{{ nifi_emqtt_certificate_authority_cert }}" # root certificate contents in a string
    nifi_emqtt_certificate_authority_key: "{{ nifi_emqtt_certificate_authority_key }}" # certificate key in a string
    nifi_emqtt_secure_password: "{{ nifi_emqtt_secure_password }}" 
    nifi_emqtt_cert_dir: "{{ nifi_emqtt_cert_dir }}" # directory to keep the generated trustore and keystore
```

The above will create `truststore.jks` and `keystore.pkcs12` in the `nifi_emqtt_cert_dir` directory.

Dependencies
------------

- Java >=8 for NiFi
- Stouts.backup for backups

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
