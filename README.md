# m2i

## Usage

```
$ ./m2i.py --help
usage: m2i.py [-h] [--memcached-host [MEMCACHED_HOST]]
              [--memcached-port [MEMCACHED_PORT]]
              [--memcached-timeout-seconds [MEMCACHED_TIMEOUT_SECONDS]]
              [--influxdb-host [INFLUXDB_HOST]]
              [--influxdb-port [INFLUXDB_PORT]] --influxdb-db-name
              INFLUXDB_DB_NAME [--influxdb-user INFLUXDB_USER]
              [--influxdb-password INFLUXDB_PASSWORD]
              [--stats-interval-seconds [STATS_INTERVAL_SECONDS]]
```

## Example

```
$ ./m2i.py
Requesting stats from memcached at [localhost:11211]
Reporting [0] requests per second
TODO: post to influxdb at [localhost:11211]
Requesting stats from memcached at [localhost:11211]
Reporting [16148000] requests per second
TODO: post to influxdb at [localhost:11211]
Requesting stats from memcached at [localhost:11211]
Reporting [10348000] requests per second
TODO: post to influxdb at [localhost:11211]
Requesting stats from memcached at [localhost:11211]
Reporting [0] requests per second
TODO: post to influxdb at [localhost:11211]
```

