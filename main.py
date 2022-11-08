#!/usr/bin/env python3

import meraki
import csv

API_KEY = ""
dashboard = meraki.DashboardAPI(API_KEY)
organizations = dashboard.organizations.getOrganizations()


def get_uplinkdata(dashboard):
    print(organizations)
    network_list: list
    network_list = [network for network in dashboard.organizations.getOrganizationNetworks(organizations[0]['id'])
                   if 'appliance' in network['productTypes']]
    print(network_list)
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'WAN1uplink', 'WAN1downlink', 'WAN2uplink', 'WAN2downlink']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in network_list:
            # writer.writerow({'name': row['name'], 'serial': row['serial'], 'model': row['model'],
            #                  'address': row['address']})
            response = dashboard.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(row['id'])
            writer.writerow({'name': row['name'], 'WAN1uplink': response['bandwidthLimits']['wan1']['limitUp'],
                             'WAN1downlink': response['bandwidthLimits']['wan1']['limitDown'],
                             'WAN2uplink': response['bandwidthLimits']['wan2']['limitUp'],
                             'WAN2downlink': response['bandwidthLimits']['wan2']['limitDown']
                             })


if __name__ == '__main__':
    get_uplinkdata(dashboard)
