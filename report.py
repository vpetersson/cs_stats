from __future__ import division
from hurry.filesize import size
from prettytable import PrettyTable
import cloudsigma

drive = cloudsigma.resource.Drive()
server = cloudsigma.resource.Server()
tag = cloudsigma.resource.Tags()


def get_disk_size(drives):
    total_disk = 0

    for d in drives:
        drive_uuid = d['drive']['uuid']
        drive_size = drive.get(drive_uuid)['size']
        total_disk += drive_size

    return drive_size


def get_server_resources(uuid):

    get_server = server.get(uuid)

    name = get_server['name']
    disk = get_disk_size(get_server['drives'])

    if get_server['status'] == 'running':
        cpu = get_server['cpu']
        ram = get_server['mem']
    else:
        cpu = False
        ram = False

    s = {'name': name, 'cpu': cpu, 'ram': ram, 'disk': disk}

    return s


def get_tags():
    get_tags = tag.get()

    tags = {}

    for t in get_tags:

        # Only count tags starting with 'acc_'.
        # This is to avoid double counting resource.
        if 'acc_' not in t['name']:
            break

        total_cpu = 0
        total_ram = 0
        total_disk = 0

        for r in t['resources']:

            if r['res_type'] == 'servers' and r['uuid']:
                s = get_server_resources(r['uuid'])
                total_cpu += s['cpu']
                total_ram += s['ram']
                total_disk += s['disk']

        tags[t['name']] = {
            'cpu': total_cpu,
            'ram': total_ram,
            'disk': total_disk
        }
    return tags


def process_result(tags_data):

    agg_cpu = 0
    agg_ram = 0
    agg_disk = 0

    # Compute totals
    for s in tags_data.keys():
        agg_cpu += tags_data[s]['cpu']
        agg_ram += tags_data[s]['ram']
        agg_disk += tags_data[s]['disk']

    # Print out result in CSV-style
    x = PrettyTable(['Tag', 'CPU', 'CPU%', 'RAM', 'RAM%', 'DISK', 'DISK%'])
    x.padding_width = 2
    for r in tags_data.keys():
        cpu = tags_data[r]['cpu']
        human_cpu = '%dGhz' % (cpu / 1000)
        cpu_share = round(cpu / agg_cpu * 100, 2)
        ram = tags_data[r]['ram']
        human_ram = size(ram)
        ram_share = round(ram / agg_ram * 100, 2)
        disk = tags_data[r]['disk']
        human_disk = size(disk)
        disk_share = round(disk / agg_disk * 100, 2)

        x.add_row([
            r,
            human_cpu,
            cpu_share,
            human_ram,
            ram_share,
            human_disk,
            disk_share
        ])

    x.add_row([
        'Total:', '%dGhz' % (agg_cpu / 1000),
        100,
        size(agg_ram),
        100,
        size(agg_disk),
        100
    ])
    return x

if __name__ == "__main__":
    tag_data = get_tags()
    print process_result(tag_data)
