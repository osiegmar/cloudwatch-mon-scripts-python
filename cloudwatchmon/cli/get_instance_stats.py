#!/usr/bin/env python

# Copyright 2015 Oliver Siegmar
#
# Based on Perl-Version of CloudWatch Monitoring Scripts for Linux -
# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from cloudwatchmon.cloud_watch_client import *

import argparse
import boto
import boto.ec2.cloudwatch
import datetime
import sys

CLIENT_NAME = 'CloudWatch-GetInstanceStats'
FileCache.CLIENT_NAME = CLIENT_NAME


def config_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
  Queries Amazon CloudWatch for statistics on CPU, memory, swap, and
  disk space utilization within a given time interval. This data is
  provided for the Amazon EC2 instance on which this script is executed.
''', epilog='''
For more information on how to use this utility, see project home on GitHub:
https://github.com/osiegmar/cloudwatch-mon-scripts-python
    ''')

    parser.add_argument('--recent-hours',
                        type=int,
                        default=1,
                        help='Specifies the number of recent hours to report.')
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Displays details of what the script is doing.')
    parser.add_argument('--version',
                        action='store_true',
                        help='Displays the version number and exits.')

    return parser


def print_metric_stats(region, instance_id, namespace, metric, title,
                       recent_hours, verbose, xdims=None, conn=None):
    boto_debug = 2 if verbose else 0

    if not conn:
        # TODO add timeout
        conn = boto.ec2.cloudwatch.connect_to_region(region, debug=boto_debug)

        if not conn:
            raise IOError('Could not establish connection to CloudWatch service')

    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=recent_hours)
    dims = {'InstanceId': instance_id}
    if xdims:
        dims.update(xdims)
    metrics = conn.get_metric_statistics(300, start_time, end_time,
                                         metric, namespace,
                                         ['Average', 'Maximum', 'Minimum'],
                                         dims)

    print(title)

    if metrics:
        max_val = max(m['Maximum'] for m in metrics)
        min_val = min(m['Minimum'] for m in metrics)
        avg_val = sum(m['Average'] for m in metrics) / float(len(metrics))

        print("    Average: {0:.2f}%, Minimum: {1:.2f}%, Maximum: {2:.2f}%\n"
              .format(avg_val, min_val, max_val))
    else:
        print("    Average: N/A, Minimum: N/A, Maximum: N/A\n")


def print_filesystem_stats(region, instance_id, namespace, metric, title,
                           recent_hours, verbose):
    boto_debug = 2 if verbose else 0

    # TODO add timeout
    conn = boto.ec2.cloudwatch.connect_to_region(region, debug=boto_debug)

    if not conn:
        raise IOError('Could not establish connection to CloudWatch service')

    dims = {'InstanceId': instance_id, 'MountPath': '/'}
    metrics = conn.list_metrics(None, dims, metric, namespace)

    if metrics:
        file_system = metrics[0].dimensions['Filesystem']
        xdims = {'MountPath': '/', 'Filesystem': file_system}
        print_metric_stats(region, instance_id,
                           namespace,
                           metric, title,
                           recent_hours, verbose, xdims, conn)


def main():
    parser = config_parser()

    args = parser.parse_args()

    if args.version:
        print(CLIENT_NAME + ' version ' + VERSION)
        return 0

    try:
        metadata = get_metadata()

        if args.verbose:
            print('Instance metadata: ' + str(metadata))

        region = metadata['placement']['availability-zone'][:-1]
        instance_id = metadata['instance-id']

        unit = 'hours' if args.recent_hours > 1 else 'hour'
        print('Instance {0} statistics for the last {1} {2}.\n'
              .format(instance_id, args.recent_hours, unit))

        print_metric_stats(region, instance_id,
                           'AWS/EC2',
                           'CPUUtilization', 'CPU Utilization',
                           args.recent_hours, args.verbose)
        print_metric_stats(region, instance_id,
                           'System/Linux',
                           'MemoryUtilization', 'Memory Utilization',
                           args.recent_hours, args.verbose)
        print_metric_stats(region, instance_id,
                           'System/Linux',
                           'SwapUtilization', 'Swap Utilization',
                           args.recent_hours, args.verbose)
        print_filesystem_stats(region, instance_id,
                               'System/Linux',
                               'DiskSpaceUtilization', 'Disk Space Utilization',
                               args.recent_hours, args.verbose)
    except Exception as e:
        log_error(str(e), False)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
