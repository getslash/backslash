# Installation and Deployment

Backslash is best deployed using Docker.

## Installing via a Source Checkoug

You can deploy using `docker-compose` directly from a cloned copy of the repository:

```
$ git clone https://github.com/getslash/backslash
$ docker-compose -p backslash -f docker/docker-compose.yml up --build
```

## Installing from a Locally Hosted Image

Alternatively, you can build your own image of Backslash, and store it on a Docker repository of your choice:

```
$ docker build --no-cache -t your.repo/backslash -f docker/Dockerfile .
$ docker push your.repo/backslash
```

And then use the resulting image in your own `docker-compose` configuration or other providers (e.g. Kubernetes).
Refer to the provided `docker-compose.yml` for more information on how to configure the various containers for use.

## Docker Environment Variables

The following environment variables are respected when running in Docker:

* `BACKSLASH_HOSTNAME`: the name of the host running backslash (fully qualified)
* `BACKSLASH_USE_SSL`: set to non-empty to indicate SSL should be used (in which case relevant certificates must be found under `/conf/certificate.crt` and `/conf/server.key`
