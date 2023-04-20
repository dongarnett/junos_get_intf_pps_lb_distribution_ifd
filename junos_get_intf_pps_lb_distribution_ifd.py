import argparse, os, paramiko, re, sys, time
from pprint import pprint
from lib_ssh_connectivity import Device
from lib_junos_sys_chassis import call_and_parse_packet_cnt_input_ifd
from lib_junos_sys_chassis import call_and_parse_packet_cnt_output_ifd
from lib_junos_sys_chassis import call_and_parse_pps_output_ifd
from lib_junos_sys_chassis import call_and_parse_pps_input_ifd
from lib_junos_sys_chassis import validate_lag_load_balancing
from lib_backend_functions import determine_list_average
from lib_backend_functions import determine_list_highest_value



'''The following code can be used to execute this script file on 1 device under test.'''
cli_args = sys.argv[1:]
dut_ip = cli_args[0]
dut_user = cli_args[1]
dut_pass = cli_args[2]
lag_id = cli_args[3]
intf_list_arg = cli_args[4]


'''DUT Login parameters'''
host_ip = dut_ip
user = dut_user
passwd = dut_pass
timeout = 30


def main():
    intf_list = intf_list_arg.split(" ")
    link_cnt = len(intf_list)
    end_cnt = link_cnt +1
    print(f'Processing for LAG {lag_id}. Member port count {link_cnt}: {intf_list}')

    dut_host = Device(host_ip, user, passwd)
    input_intf_pps_list = call_and_parse_pps_input_ifd(dut_host, intf_list)
    output_intf_pps_list = call_and_parse_pps_output_ifd(dut_host, intf_list)
    i = 0
    print("###########################################")
    print("##### PER INTERFACE INPUT/OUTPUT PPS ######")
    print("###########################################")
    for intf in intf_list:
        print(f'Interface {intf_list[i]} - Input PPS: {input_intf_pps_list[i]}')
        print(f'Interface {intf_list[i]} - Output PPS: {output_intf_pps_list[i]}')
        i += 1
    dict_intf_stats = validate_lag_load_balancing(lag_id, intf_list, link_cnt, input_intf_pps_list, output_intf_pps_list)


if __name__ == '__main__':
    main()
