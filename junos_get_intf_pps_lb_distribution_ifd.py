import argparse, os, paramiko, re, sys, time
from pprint import pprint
from lib_ssh_connectivity import Device
from lib_junos_sys_chassis import call_and_parse_packet_cnt_input_ifd
from lib_junos_sys_chassis import call_and_parse_packet_cnt_output_ifd
from lib_junos_sys_chassis import call_and_parse_pps_output_ifd
from lib_junos_sys_chassis import call_and_parse_pps_input_ifd
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



# def main():
#     intf_list = intf_list_arg.split(" ")
#     lag_cnt = len(intf_list)
#     print(f'Processing for LAG {lag_id}. Member port count {lag_cnt}: {intf_list}')
#
#     dut_host = Device(host_ip, user, passwd)
#     input_intf_pps_list = call_and_parse_pps_input_ifd(dut_host, intf_list)
#     output_intf_pps_list = call_and_parse_pps_output_ifd(dut_host, intf_list)
#     i = 0
#     print("###########################################")
#     print("##### PER INTERFACE INPUT/OUTPUT PPS ######")
#     print("###########################################")
#     for intf in intf_list:
#         print(f'Interface {intf_list[i]} - Input PPS: {input_intf_pps_list[i]}')
#         print(f'Interface {intf_list[i]} - Output PPS: {output_intf_pps_list[i]}')
#         i += 1
#
#     # DETERMINE LOAD BALANCING DISTRIBUTION
#     '''Obtain combined input and output PPS rates for LAG member ports in order to:
#         1. Determine ideal load balancing distribution among member ports
#         2. Determine actual load balancing distribution among member ports
#     '''
#     combined_input_pps = 0
#     i = 0
#     for intf in intf_list:
#         combined_input_pps = int(input_intf_pps_list[i]) + combined_input_pps
#         i += 1
#     combined_output_pps = 0
#     i = 0
#     for intf in intf_list:
#         combined_output_pps = int(output_intf_pps_list[i]) + combined_output_pps
#         i += 1
#     print("###########################################")
#     print("####### COMBINED INPUT/OUTPUT PPS #########")
#     print("###########################################")
#     print(f'LAG {lag_id} combined member port input pps rate: {combined_input_pps}')
#     print(f'LAG {lag_id} combined member port output pps rate: {combined_output_pps}')
#     ideal_lb_variance_input_pps = combined_input_pps / lag_cnt
#     ideal_lb_variance_output_pps = combined_output_pps / lag_cnt
#     print("##########################################")
#     print("# IDEAL PER MEMBER PORT INPUT/OUTPUT PPS #")
#     print("##########################################")
#     print(f'LAG {lag_id} ideal input pps rate load balancing for member ports: {ideal_lb_variance_input_pps}')
#     print(f'LAG {lag_id} ideal output pps rate load balancing for member ports: {ideal_lb_variance_output_pps}')
#     i = 0
#     input_lb_pps_distribution_list = []
#     output_lb_pps_distribution_list = []
#     for intf in intf_list:
#         actual_input_pps_lb_distribution = int(input_intf_pps_list[i]) / combined_input_pps
#         input_lb_pps_distribution_list.append(actual_input_pps_lb_distribution)
#         actual_output_pps_lb_distribution = int(output_intf_pps_list[i]) / combined_output_pps
#         output_lb_pps_distribution_list.append(actual_output_pps_lb_distribution)
#         i += 1
#     i = 0
#     print("##############################################")
#     print("# PER MEMBER PORT INPUT TRAFFIC DISTRIBUTION #")
#     print("##############################################")
#     for intf in intf_list:
#         print(f'LAG {lag_id} member port {intf_list[i]} input pps distribution {input_lb_pps_distribution_list[i]}')
#         i += 1
#     i = 0
#     print("###############################################")
#     print("# PER MEMBER PORT OUTPUT TRAFFIC DISTRIBUTION #")
#     print("###############################################")
#     for intf in intf_list:
#         print(f'LAG {lag_id} member port {intf_list[i]} output pps distribution {output_lb_pps_distribution_list[i]}')
#         i += 1

def main():
    intf_list = intf_list_arg.split(" ")
    lag_cnt = len(intf_list)
    end_cnt = lag_cnt +1
    print(f'Processing for LAG {lag_id}. Member port count {lag_cnt}: {intf_list}')

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

    # DETERMINE LOAD BALANCING DISTRIBUTION
    '''Obtain combined input and output PPS rates for LAG member ports in order to:
        1. Determine ideal load balancing distribution among member ports
        2. Determine actual load balancing distribution among member ports
    '''
    combined_input_pps = 0
    i = 0
    for intf in intf_list:
        combined_input_pps = int(input_intf_pps_list[i]) + combined_input_pps
        i += 1
    combined_output_pps = 0
    i = 0
    for intf in intf_list:
        combined_output_pps = int(output_intf_pps_list[i]) + combined_output_pps
        i += 1
    print("###########################################")
    print("####### COMBINED INPUT/OUTPUT PPS #########")
    print("###########################################")
    print(f'LAG {lag_id} combined member port input pps rate: {combined_input_pps}')
    print(f'LAG {lag_id} combined member port output pps rate: {combined_output_pps}')
    ideal_lb_variance_input_pps = combined_input_pps / lag_cnt
    ideal_lb_variance_output_pps = combined_output_pps / lag_cnt
    print("##########################################")
    print("# IDEAL PER MEMBER PORT INPUT/OUTPUT PPS #")
    print("##########################################")
    print(f'LAG {lag_id} ideal input pps rate load balancing for member ports: {ideal_lb_variance_input_pps}')
    print(f'LAG {lag_id} ideal output pps rate load balancing for member ports: {ideal_lb_variance_output_pps}')
    i = 0
    input_lb_pps_distribution_list = []
    output_lb_pps_distribution_list = []
    for intf in intf_list:
        actual_input_pps_lb_distribution = int(input_intf_pps_list[i]) / combined_input_pps
        input_lb_pps_distribution_list.append(actual_input_pps_lb_distribution)
        actual_output_pps_lb_distribution = int(output_intf_pps_list[i]) / combined_output_pps
        output_lb_pps_distribution_list.append(actual_output_pps_lb_distribution)
        i += 1
    i = 0
    print("##############################################")
    print("# PER MEMBER PORT INPUT TRAFFIC DISTRIBUTION #")
    print("##############################################")
    for intf in intf_list:
        print(f'LAG {lag_id} member port {intf_list[i]} input pps distribution {input_lb_pps_distribution_list[i]}')
        i += 1
    i = 0
    print("###############################################")
    print("# PER MEMBER PORT OUTPUT TRAFFIC DISTRIBUTION #")
    print("###############################################")
    for intf in intf_list:
        print(f'LAG {lag_id} member port {intf_list[i]} output pps distribution {output_lb_pps_distribution_list[i]}')
        i += 1

if __name__ == '__main__':
    main()
