from ansible.module_utils.basic import *
from OpenSSL import crypto

def x509name_str(x509name):
    return ", ".join("%s=%s" % tup for tup in x509name.get_components())

def x509cert_decode(cert):
    c = {
        "certificate": crypto.dump_certificate(crypto.FILETYPE_PEM, cert),
        "fingerprint": {
                "algorithm": "SHA1",
                "digest": cert.digest("SHA1"),
            },
        "has_expired": cert.has_expired(),
        "issuer": x509name_str(cert.get_issuer()),
        "issuer_dc": dict(cert.get_issuer().get_components()),
        "serial_number": cert.get_serial_number(),
        "signature_algorithm": cert.get_signature_algorithm(),
        "subject": x509name_str(cert.get_subject()),
        "subject_dc": dict(cert.get_subject().get_components()),
        "validity": {
                "not_after": cert.get_notAfter(),
                "not_before": cert.get_notBefore(),
            },
        "version": cert.get_version() + 1,
    }
    c["name"] = c["subject_dc"]["CN"]

    return c

def main():
    args = {
        "src": { "required": True, "type": "str" },
        "passphrase": { "required": False, "type": "str" },
    }

    module = AnsibleModule(argument_spec=args)

    # Load PKCS#12 file
    p12 = crypto.load_pkcs12(open(module.params["src"], 'rb').read(), module.params["passphrase"])
    chain = list()

    # Obtain the signed certificate
    c = x509cert_decode(p12.get_certificate())
    chain.append(c)

    # Obtain CA certificate chain
    if p12.get_ca_certificates() is not None:
        for cert in p12.get_ca_certificates():
            c = x509cert_decode(cert)
            chain.append(c)

    chain.reverse()
    module.exit_json(changed=True, certificates=chain)

if __name__ == '__main__':
    main()
