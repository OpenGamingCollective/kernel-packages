# kernel-packages

Build system for the OGC Kernel, providing signed OCI images of various kernel package formats

## Secure Boot

In the repository a stub secure boot private key is included to avoid failing when building locally.

That private key has been generated with the following commands:

```sh
openssl req -new -x509 -newkey rsa:2048 -subj "/CN=tutorial's kernel-signing key/" -keyout db.key -out db.crt -days 3650 -nodes -sha256

openssl x509 -outform DER -in db.crt -out db.cer
```

__WARNING__ As the included private key is public from a security standpoint a kernel compiled
with such a key is as secure as an unsigned one.
