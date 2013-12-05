import sys
from socket import inet_aton

def get_net_size(netmask):
    binary_str = ''
    for octet in netmask:
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))

def cidr_notation(ip_address, netmask):
    """
    Retrieve the cidr notation given an ip address and netmask.
    
    For example:
    
        cidr_notation('12.34.56.78', '255.255.255.248')
    
    Would return: 12.34.56.72/29 
    
    @see http://terminalmage.net/2012/06/10/how-to-find-out-the-cidr-notation-for-a-subne-given-an-ip-and-netmask/
    @see http://www.aelius.com/njh/subnet_sheet.html
    """
    try:
        inet_aton(ip_address)
    except:
        raise Exception("Invalid ip address '%s'" % ip_address)
    try:
        inet_aton(netmask)
    except:
        raise Exception("Invalid netmask '%s'" % netmask)

    ip_address_split = ip_address.split('.')
    netmask_split = netmask.split('.')
    
    # calculate network start
    net_start = [str(int(ip_address_split[x]) & int(netmask_split[x]))
                    for x in range(0,4)]
    
    return '.'.join(net_start) + '/' + get_net_size(netmask_split)
