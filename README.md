cloudwatch-mon-scripts-python
=============================

[![PyPI version](https://badge.fury.io/py/cloudwatchmon.svg)](https://badge.fury.io/py/cloudwatchmon)

> [!WARNING]
> **This project is archived and no longer maintained.**
>
> I haven't personally used these scripts in nearly a decade and am no longer
> in a position to maintain them. The codebase still targets Python 2.6+ and
> the legacy `boto` SDK (not `boto3`), and will not receive further updates,
> fixes, or releases.
>
> The repository remains available in read-only form for reference, and the
> existing `cloudwatchmon` package stays on PyPI. If you'd like to continue
> the work, you are very welcome to fork it — a modernized version targeting
> Python 3 and `boto3` would be the right path forward.

Linux monitoring scripts for the [AWS CloudWatch Service](https://aws.amazon.com/de/cloudwatch/).

Initially, this project was created, because the
original [AWS monitoring scripts](https://aws.amazon.com/code/8720044071969977)
lacked support for the eu-central-1 (Frankfurt) region for about 4 months
(2014-10-23 to 2015-02-25).

Now, this project has a couple of additional features (compared to v1.1.0 of
the original AWS monitoring scripts):

- Memory monitoring incl. buffers
- Load monitoring (overall and per CPU core)
- Monitoring of disk inode usage
- Process monitoring
- Fewer dependencies
- Simpler installation


Requirements
------------

- Python 2 (>= 2.6) or Python 3 (>= 3.3)
- Boto >= 2.33.0


Installation
------------

Optionally create a virtual environment and activate it. Then just run
`pip install cloudwatchmon`. Install the scripts in `/usr/local/bin` folder.

For script usage, run:

    mon-put-instance-stats.py --help


Examples
--------

To perform a simple test run without posting data to Amazon CloudWatch:

    mon-put-instance-stats.py --mem-util --verify --verbose

Report memory and disk space utilization to Amazon CloudWatch:

    mon-put-instance-stats.py --mem-util --disk-space-util --disk-path=/

To get utilization statistics for the last 12 hours:

    mon-get-instance-stats.py --recent-hours=12


Configuration
-------------

To allow an EC2 instance to read and post metric data to Amazon CloudWatch,
this IAM policy is required:

```json
{
  "Statement": [
    {
      "Action": [
        "cloudwatch:ListMetrics",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:PutMetricData",
        "autoscaling:DescribeAutoScalingInstances"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

If the policy is configured via an IAM role that is assigned to the EC2
server this script runs on, you're done.

Otherwise you can configure the policy for a user account and export
the credentials before running the script:

```sh
export AWS_ACCESS_KEY_ID=[Your AWS Access Key ID]
export AWS_SECRET_ACCESS_KEY=[Your AWS Secret Access Key]
```

Third option is to create a _~/.boto_ file with this content:

```
[Credentials]
aws_access_key_id = Your AWS Access Key ID
aws_secret_access_key = Your AWS Secret Access Key
```

Copyright
---------

Copyright 2015 Oliver Siegmar

Based on Perl-Version of CloudWatch Monitoring Scripts for Linux -
Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
