# juniper_automation_fpc_util_avg
This tool obtains analyzes interface statistics to provide the following outputs:
1. Ideal per port load balancing pps rate for LAG member ports
2. Actual per port pps rate for each LAG member port
3. Traffic distribution pps rate percentage of each LAG member port


Requirements:
The Paramiko SSH library is required for connectivity to the target device.


Usage:
you@your_computer# python3 junos_fpc_utilization.py <ip-address> <username> <password> <interval-count>


Example Run:
me@my_computer# python3 junos_get_intf_pps_lb_distribution_ifd.py 10.0.0.21 user123 passwd123 ae1 'et-0/0/1 et-0/0/9 et-0/1/1 et-0/1/9'
Processing for LAG ae1. Member port count 4: ['et-0/0/1', 'et-0/0/9', 'et-0/1/1', 'et-0/1/9']
Sending command: show interfaces et-0/0/1 statistics | match "Input rate"

Sending command: show interfaces et-0/0/9 statistics | match "Input rate"

Sending command: show interfaces et-0/1/1 statistics | match "Input rate"

Sending command: show interfaces et-0/1/9 statistics | match "Input rate"

Sending command: show interfaces et-0/0/1 statistics| match "Output rate"

Sending command: show interfaces et-0/0/9 statistics| match "Output rate"

Sending command: show interfaces et-0/1/1 statistics| match "Output rate"

Sending command: show interfaces et-0/1/9 statistics| match "Output rate"

Interface et-0/0/1 - Input PPS: 68100
Interface et-0/0/1 - Output PPS: 27857
Interface et-0/0/9 - Input PPS: 63571
Interface et-0/0/9 - Output PPS: 21854
Interface et-0/0/9 - Input PPS: 63571
Interface et-0/0/9 - Output PPS: 21854
Interface et-0/0/9 - Input PPS: 63571
Interface et-0/0/9 - Output PPS: 21854
LAG ae1 combined member port input pps rate: 258813
LAG ae1 combined member port output pps rate: 93419
LAG ae1 ideal input pps rate load balancing for member ports: 64703.25
LAG ae1 ideal output pps rate load balancing for member ports: 23354.75
LAG ae1 member port et-0/0/1 input pps distribution 0.26312434074022556
LAG ae1 member port et-0/0/9 input pps distribution 0.24562521975325816
LAG ae1 member port et-0/0/9 input pps distribution 0.24562521975325816
LAG ae1 member port et-0/0/9 input pps distribution 0.24562521975325816
LAG ae1 member port et-0/0/9 output pps distribution 0.23393528083152249
LAG ae1 member port et-0/0/9 output pps distribution 0.23393528083152249
LAG ae1 member port et-0/0/9 output pps distribution 0.23393528083152249
LAG ae1 member port et-0/0/9 output pps distribution 0.23393528083152249
