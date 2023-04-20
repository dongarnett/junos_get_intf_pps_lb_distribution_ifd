import argparse, paramiko, os, re, sys, time
from lib_ssh_connectivity import Device
from lib_ssh_connectivity import create_handle_quiet
from pprint import pprint
#from collections import defaultdict



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
        #print(output_to_parse)
        split_data = output_to_parse.split('\r\n')
        #print(split_data)
        for line in split_data:
            #print(line)
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
        #print(output_to_parse)
        split_data = output_to_parse.split('\r\n')
        #print(split_data)
        for line in split_data:
            #print(line)
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
