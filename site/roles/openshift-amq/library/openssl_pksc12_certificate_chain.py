from ansible.module_utils.basic import *
from OpenSSL import crypto

#
# TODO
#   - `cert_number` is a quick workaround to provide a unique name for the certificate
#   - `chain[i].name` is  quick workaroud to to provide the name for the certificate
#        o This should be replaced by the CN of the certificate, or:
#            * provide a dictionary of the certificate subject (and issuer) for each name compoenent
#

def x509name_str(x509name):
    return ", ".join("%s=%s" % tup for tup in x509name.get_components())

def main():
    args = {
        "src": { "required": True, "type": "str" },
        "passphrase": { "required": False, "type": "str" },
    }

    module = AnsibleModule(argument_spec=args)

    #### MODULE LOGIC

    # Load PKCS#12 file
    p12 = crypto.load_pkcs12(open(module.params["src"], 'rb').read(), module.params["passphrase"])

    chain = list()
    cert_number = 1   # TODO See module note above

    # Obtain the signed certificate
    cert = p12.get_certificate()
    c = {
        "certificate": crypto.dump_certificate(crypto.FILETYPE_PEM, cert),
        "fingerprint": {
                "algorithm": "SHA1",
                "digest": cert.digest("SHA1"),
            },
        "has_expired": cert.has_expired(),
        "issuer": x509name_str(cert.get_issuer()),
        "serial_number": cert.get_serial_number(),
        "signature_algorithm": cert.get_signature_algorithm(),
        "subject": x509name_str(cert.get_subject()),
        "validity": {
                "not_after": cert.get_notAfter(),
                "not_before": cert.get_notBefore(),
            },
        "version": cert.get_version() + 1,
    }
    c["name"] = "cert-{}".format(cert_number) # TODO See module note above
    cert_number += 1
    chain.append(c)

    # Obtain CA certificate chain
    if p12.get_ca_certificates() is not None:
        for cert in p12.get_ca_certificates():
            c = {
                "certificate": crypto.dump_certificate(crypto.FILETYPE_PEM, cert),
                "fingerprint": {
                        "algorithm": "SHA1",
                        "digest": cert.digest("SHA1"),
                    },
                "has_expired": cert.has_expired(),
                "issuer": x509name_str(cert.get_issuer()),
                "serial_number": cert.get_serial_number(),
                "signature_algorithm": cert.get_signature_algorithm(),
                "subject": x509name_str(cert.get_subject()),
                "validity": {
                        "not_after": cert.get_notAfter(),
                        "not_before": cert.get_notBefore(),
                    },
                "version": cert.get_version() + 1,
            }
            c["name"] = "cert-{}".format(cert_number) # TODO See module note above
            cert_number += 1
            chain.append(c)

    chain.reverse()
    module.exit_json(changed=True, certificates=chain)

if __name__ == '__main__':
    main()
