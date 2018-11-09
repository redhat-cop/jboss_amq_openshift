# Role Description

Install Active-MQ 6.3 in an OpenShift cluster using the Red Hat xPaaS image template
`amq63-ssl`. A certificate chain and a private key packaged into a
PKCS#12 file can be used. Otherwise the necessary self-signed certificates will be
generated.

This role should only be executed on `localhost` since it makes use of the `k8s` Ansible
module. Thus, inventory is not required.

## Requirements

- Ansible 2.7+
- Python OpenSSL module: `sudo pip install pyOpenSSL`

## Role Variables

- `openshift_namespace`
OpenShift project / namespace A-MQ should be installed in. Will be created if not already
present.

- `openshift_service_account`
OpenShift service account A-MQ should be configured to use. Will be created if not
already present.

- `pkcs12_file`
Path to PKCS#12 file containing certificate chain to use, including a private key. If not
defined self-signed certificates will automatically be generated and placed into a
generated PKCS#12 file.

- `pkcs12_alias`
Alias within the PKCS#12 file containing the desired certificate chain.

- `amq_keystore`
Java key store file name to import the certificate chain and private key into and is
used as an OpenShift secret.

- `amq_truststore`
Java trust store file name to import the certificate chain into and is used as an
OpenShift secret.

- `pkcs12_password`
PKCS#12 password. If not definted the password will be automatically generated. This is
typically only defined when an `pkcs12_file` is defined as most PKCS#12 files are
secured with a password.

- `keystore_password`
Java key store password. If not defined will be automatically generated.

- `truststore_password`
Java trust store password. If not defined will be automatically generated.

- `certificate_dn`
The distinguished name (DN) of the self-signed certificate to use.

## Dependencies

None.

## Example Playbooks
### Install using all defaults
````yaml
---
- hosts: localhost
  roles:
    - jboss_amq_openshift
````

### Install into a specific OpenShift project / namespace
````yaml
---
- hosts: localhost

  roles:
    - role: jboss_amq_openshift
      openshift_namespace: amq-dev
````

### Install and generate all certificates using a custom certificate DN
````yaml
---
- hosts: localhost

  roles:
    - role: jboss_amq_openshift
      certificate_dn:
        common_name: broker-amq
        country_name: US
        state_or_province_name: NC
        locality_name: Raleigh
        organization_name: Red Hat
        organizational_unit_name: Consulting
````

### Install using specific certificates
````yaml
---
- hosts: localhost

  roles:
    - role: jboss_amq_openshift
      pkcs12_file: /opt/rh/openshift/certicates/amq.p12
      pkcs12_paassword: changeit
      pkcs12_alias: openshift-amq
````

## Author Information

| Name                  | E-Mail
| ----                  | ------
| Christian J. Polizzi  | christian.polizzi@redhat.com
