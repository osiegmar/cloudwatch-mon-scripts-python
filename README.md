cloudwatch-mon-scripts-python
=============================

Linux monitoring scripts for CloudWatch.


Requirements
------------

- Python >= 2.6
- Boto >= 2.33.0


Installation
------------

To install the required Boto library, please see [Installing Boto](http://boto.readthedocs.org/en/latest/getting_started.html#installing-boto).

    wget -O cloudwatch-mon-scripts-python.tar.gz \
        https://github.com/osiegmar/cloudwatch-mon-scripts-python/archive/master.tar.gz

    tar xvfz cloudwatch-mon-scripts-python.tar.gz

    ./cloudwatch-mon-scripts-python-master/bin/mon-put-instance-data.py

    ./mon-put-instance-data.py --help
    ./mon-get-instance-data.py --help


Examples
--------

To perform a simple test run without posting data to Amazon CloudWatch

    ./mon-put-instance-data.py --mem-util --verify --verbose

Report memory and disk space utilization to Amazon CloudWatch

    ./mon-put-instance-data.py --mem-util --disk-space-util --disk-path=/

To get utilization statistics for the last 12 hours

    ./mon-get-instance-data.py --recent-hours=12


Configuration
-------------

To allow an EC2 instance to post metric data to Amazon CloudWatch, this
IAM policy is required:

    {
      "Statement": [
        {
          "Action": [
            "cloudwatch:PutMetricData"
          ],
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }

If the _--autoscaling_ option is used, this IAM policy is required:

    {
      "Statement": [
        {
          "Action": [
            "cloudwatch:PutMetricData",
            "autoscaling:DescribeAutoScalingInstances"
          ],
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }

If the policy is configured via an IAM role that is assigned to the EC2
server this script runs on, you're done.

Otherwise you can configure the policy for a user account and export
the credentials before running the script:

    export AWS_ACCESS_KEY_ID=[Your AWS Access Key ID]
    export AWS_SECRET_ACCESS_KEY=[Your AWS Secret Access Key]

Third option is to create a _~/.boto_ file with this content:

    [Credentials]
    aws_access_key_id = Your AWS Access Key ID
    aws_secret_access_key = Your AWS Secret Access Key


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
