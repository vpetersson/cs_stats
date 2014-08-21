# CloudSigma Stats Generator

A tool to generate rough statistics on spending based on tags for CloudSigma.

## Requirements

Before you begin, you will need to have [pycloudsigma](https://github.com/cloudsigma/pycloudsigma) up and running. With that installed, you also need to install the other Python requirements by running:

    pip install -r requirements.txt


## Gettings started

The idea of this project is to allow you to get a rough estimate on how you are spending your money across projects in [CloudSigma](https://www.cloudsigma.com).

The backbone in this tool is the [tags](https://cloudsigma-docs.readthedocs.org/en/2.10/tags.html) functionality. In order to not double count resources, the namespace `acc_` is used. Hence you need to tag all your servers in a given project with something like `acc_foo`. Once you've done this, your tagged server resources should show up in the table.


## Usage

    $ python report.py
    +------------+---------+---------+-------+---------+--------+---------+
    |    Tag     |   CPU   |   CPU%  |  RAM  |   RAM%  |  DISK  |  DISK%  |
    +------------+---------+---------+-------+---------+--------+---------+
    |  acc_foo   |  5Ghz   |  33.33  |  5G   |  33.33  |   5G   |  33.33  |
    |  acc_bar   |  10Ghz  |  66.66  |  10G  |  66.66  |  10G   |  66.66  |
    |   Total:   |  15Ghz  |   100   |  15G  |   100   |  15G   |   100   |
    +------------+---------+---------+-------+---------+--------+---------+

Please note that CPU%, RAM% and DISK% are percentages of the total, not utilization within the VMs.

## Known issues

Only server resources are counted. All other compute resources (such as licenses, network resources etc) are ignored.
