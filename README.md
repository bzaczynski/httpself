# httpself

HTTP server over SSL/TLS with an automatically generated self-signed certificate.

## Usage

Serve static files from the current working directory:

```shell
$ https [-p/--port <NNNN>] [--public]
```

### Example #1

By default, the server runs on port number `443`, which requires superuser privileges. Note that the server will only be accessible from the `localhost`:

```shell
$ https
Running server at https://localhost:443
```

### Example #2

To specify an alternative port number:

```shell
$ https --port 8443
Running server at https://localhost:8443
```

### Example #3

To make the server accessible from other devices:

```shell
$ https --public
Running server at https://0.0.0.0:443
```

### Example #4

To run the server publicly on a custom port:

```shell
$ https --public -p 8443
Running server at https://0.0.0.0:8443
```

## Installation

```shell
$ pip install httpself
```
