#!/usr/bin/env python

import argparse
import getpass
import signal
import sys
import telnetlib
import threading

# Parse argument list
parser = argparse.ArgumentParser()
parser.add_argument('--memcached-host', dest="memcached_host", type=str, nargs="?", default="localhost")
parser.add_argument('--memcached-port', dest="memcached_port", type=int, nargs="?", default=11211)
parser.add_argument('--influxdb-host', dest="influxdb_host", type=str, nargs="?", default="localhost")
parser.add_argument('--influxdb-port', dest="influxdb_port", type=int, nargs="?", default=8086)
parser.add_argument('--stats-interval-seconds', dest="stats_interval_seconds", nargs="?", default=1)
args = parser.parse_args()

memcached_host = args.memcached_host
memcached_port = args.memcached_port
influxdb_host = args.influxdb_host
influxdb_port = args.influxdb_port
stats_interval_seconds = args.stats_interval_seconds

print """
m2i.py

memcached_host         : {}
memcached_port         : {}
influxdb_host          : {}
influxdb_port          : {}
stats_interval_seconds : {}
""".format(
    memcached_host,
    memcached_port,
    influxdb_host,
    influxdb_port,
    stats_interval_seconds)

# Global state
global_time = 0
global_total_requests = 0

def get_raw_stats():
    global memcached_host, memcached_port

    tn = telnetlib.Telnet(memcached_host, memcached_port)
    tn.write("stats\n")
    tn.write("quit\n")
    raw = tn.read_all()
    tn.close()
    return raw

def parse_raw_stats(raw_stats):
    stats = {}
    lines = raw_stats.splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) == 3 and parts[0] == "STAT":
            stat_name = parts[1]
            stat_value = parts[2]
            stats[stat_name] = stat_value
    return stats

def extract_rps(raw_stats):
    global global_time, global_total_requests

    stats = parse_raw_stats(raw_stats)

    # Sum commands completed
    request_stats = ["cmd_get", "cmd_set", "cmd_flush", "cmd_touch"]
    total_requests = 0
    for r_stat in request_stats:
        total_requests += int(stats[r_stat])

    sample_time = int(stats["time"])

    # Copy previous values
    prev_time = global_time
    prev_total_requests = global_total_requests

    # Skip this iteration early if the sample has the previous timestamp
    if prev_time == sample_time:
        return None

    # Save current values
    global_time = sample_time
    global_total_requests = total_requests

    # Skip sample computation if this is the priming sample
    if prev_time == 0:
        return None

    # Compute requests per second
    delta_commands = global_total_requests - prev_total_requests
    delta_time = global_time - prev_time

    # Throw away nonsense values
    if delta_commands < 0 or delta_time < 0:
        return None

    requests_per_second = delta_commands / delta_time
    return requests_per_second

def post_to_influxdb(rps):
    global memcached_host, memcached_port

    print "TODO: post to influxdb at [{}:{}]".format(
        memcached_host, memcached_port)
    # TODO

def collect_sample():
    print "Requesting stats from memcached at [{}:{}]".format(
        memcached_host,
        memcached_port)
    raw_stats = get_raw_stats()
    rps = extract_rps(raw_stats)
    if rps is None:
        print "Skipping requests-per-second report for this sample"
        return
    print "Reporting [{}] requests per second".format(rps)
    post_to_influxdb(rps)

def schedule(interval_seconds, f):
    def wrapped_f():
        f()
        timer = threading.Timer(interval_seconds, wrapped_f).start()
    threading.Timer(interval_seconds, wrapped_f).start()

# Schedule sample collection
print "Scheduling sample collection for every [{}] seconds".format(
    stats_interval_seconds)

schedule(stats_interval_seconds, collect_sample)

# Await Ctrl + C
signal.signal(signal.SIGINT, sys.exit(0))
signal.pause()
