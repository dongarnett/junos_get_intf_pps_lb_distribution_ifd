import argparse, paramiko, os, re, sys, time
from lib_ssh_connectivity import Device
from lib_ssh_connectivity import create_handle_quiet
from pprint import pprint



'''Get total packet values from device'''
def get_intf_packet_cnt_input_ifd(dut_host, intf_name):
    '''Command sets for device configuration'''
    command_set_1 = [f'show interfaces statistics {intf_name} | match "Input packets"']
    '''Create handle'''
    dut_host_session = create_handle_quiet(dut_host)
    dut_host_terminal = dut_host_session.invoke_shell()
    '''Start execution'''
    for command in command_set_1:
        print(f'Sending command: {command}\n')
        try:
            dut_host_terminal.send(f'{command}\n')
            time.sleep(1)
        except:
            print(f"An error occurred.")
        output = dut_host_terminal.recv(1000).decode('utf-8')
    #output_recv = output.split('\r\n')
    dut_host_terminal.send('exit\n')
    return output
    time.sleep(10)


'''Call function to get packet count values from intf list, then parse values'''
def call_and_parse_packet_cnt_input_ifd(dut_host, intf_list):
    input_pps_list = []
    for intf in intf_list:
        output_to_parse = get_intf_packet_cnt_input_ifd(dut_host, intf)
        split_data = output_to_parse.split('\r\n')
        for line in split_data:
            if "packets" in line:
                parsed_items = line.split()
                print(parsed_items)
                input_pps = parsed_items[-1]
                input_pps_list.append(input_pps)
    return input_pps_list


'''Get packet count values from device'''
def get_intf_packet_cnt_output_ifd(dut_host, intf_name):
    '''Command sets for device configuration'''
    command_set_1 = [f'show interfaces statistics {intf_name} | match "Output packets"']
    '''Create handle'''
    dut_host_session = create_handle_quiet(dut_host)
    dut_host_terminal = dut_host_session.invoke_shell()
    '''Start execution'''
    for command in command_set_1:
        print(f'Sending command: {command}\n')
        try:
            dut_host_terminal.send(f'{command}\n')
            time.sleep(1)
        except:
            print(f"An error occurred.")
        output = dut_host_terminal.recv(1000).decode('utf-8')
    #output_recv = output.split('\r\n')
    dut_host_terminal.send('exit\n')
    return output
    time.sleep(10)


'''Call function to get packet count values from intf list, then parse values'''
def call_and_parse_packet_cnt_output_ifd(dut_host, intf_list):
    output_pps_list = []
    for intf in intf_list:
        output_to_parse = get_intf_packet_cnt_output_ifd(dut_host, intf)
        split_data = output_to_parse.split('\r\n')
        for line in split_data:
            if "packets" in line:
                parsed_items = line.split()
                print(parsed_items)
                output_pps = parsed_items[-1]
                output_pps_list.append(output_pps)
    return output_pps_list


'''Get pps values from device'''
def get_intf_pps_input_ifd(dut_host, intf_name):
    '''Command sets for device configuration'''
    command_set_1 = [f'show interfaces {intf_name} statistics | match "Input rate"']
    '''Create handle'''
    dut_host_session = create_handle_quiet(dut_host)
    dut_host_terminal = dut_host_session.invoke_shell()
    '''Start execution'''
    for command in command_set_1:
        print(f'Sending command: {command}\n')
        try:
            dut_host_terminal.send(f'{command}\n')
            time.sleep(1)
        except:
            print(f"An error occurred.")
        output = dut_host_terminal.recv(1000).decode('utf-8')
    dut_host_terminal.send('exit\n')
    return output
    time.sleep(10)


'''Call function to get pps values from intf list, then parse pps values'''
def call_and_parse_pps_input_ifd(dut_host, intf_list):
    input_pps_list = []
    for intf in intf_list:
        output_to_parse = get_intf_pps_input_ifd(dut_host, intf)
        split_data = output_to_parse.split('\r\n')
        for line in split_data:
            if "pps" in line:
                parsed_items = line.split()
                input_pps = int(parsed_items[-2].replace('(', ''))
                #print(input_pps)
                input_pps_list.append(input_pps)
    return input_pps_list


'''Get pps values from device'''
def get_intf_pps_output_ifd(dut_host, intf_name):
    '''Command sets for device configuration'''
    command_set_1 = [f'show interfaces {intf_name} statistics| match "Output rate"']
    '''Create handle'''
    dut_host_session = create_handle_quiet(dut_host)
    dut_host_terminal = dut_host_session.invoke_shell()
    '''Start execution'''
    for command in command_set_1:
        print(f'Sending command: {command}\n')
        try:
            dut_host_terminal.send(f'{command}\n')
            time.sleep(1)
        except:
            print(f"An error occurred.")
        output = dut_host_terminal.recv(1000).decode('utf-8')
    dut_host_terminal.send('exit\n')
    return output
    time.sleep(10)


'''Call function to get pps values from intf list, then parse pps values'''
def call_and_parse_pps_output_ifd(dut_host, intf_list):
    output_pps_list = []
    for intf in intf_list:
        output_to_parse = get_intf_pps_output_ifd(dut_host, intf)
        split_data = output_to_parse.split('\r\n')
        for line in split_data:
            if "pps" in line:
                parsed_items = line.split()
                output_pps = int(parsed_items[-2].replace('(', ''))
                #print(output_pps)
                output_pps_list.append(output_pps)
    return output_pps_list


def validate_lag_load_balancing(lag_id, intf_list, link_cnt, input_intf_pps_list, output_intf_pps_list):
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
    ideal_lb_variance_input_pps = combined_input_pps / link_cnt
    ideal_lb_variance_output_pps = combined_output_pps / link_cnt
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
    dict_intf_stats = {
                "combined_input_pps" : combined_input_pps,
                "combined_output_pps" : combined_output_pps,
                "ideal_lb_variance_input_pps" : ideal_lb_variance_input_pps,
                "ideal_lb_variance_output_pps" : ideal_lb_variance_output_pps,
                "input_lb_pps_distribution_list" : input_lb_pps_distribution_list,
                "output_lb_pps_distribution_list" : output_lb_pps_distribution_list
                }
    return dict_intf_stats
