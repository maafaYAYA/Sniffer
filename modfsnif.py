#! /usr/local/bin/pytdon3.5
import socket
import struct
import textwrap
import json
import config
###global var 
#import variable

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '

config.F={
                'EtdFdest_mac':None,
                'EtdFsrc_mac':None,
                'EtdFdata':None,
                'EtdFetd_proto':None,
                'version':None,
                'header_lengtd':None,
                'ttl':None,
                'src':None,
                'target':None,
                'type':None,
                'ICMPtype':None,
                'ICMPcode':None,
                'ICMPchecksum':None,
                'TCPdestP':None,
                'TCPsrcP':None,
               }
config.Full= {}
def main():
        
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    #3  GGP  Gateway-to-Gateway
    #socket.socket([family[, type[, proto]]])
        count = 0
        maxi = 1
        while (count < maxi):
            raw_data, addr = conn.recvfrom(65536)
            dest_mac, src_mac, etd_proto, data = etdernet_frame(raw_data)
            print('\n Etdernet Frame: ')
            print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'.format(dest_mac, src_mac, etd_proto))
           
            print(config.F)
            #print('###############off')
             #1test sol 
             #adr=json.dumps(dest_mac)
             #print(adr)
            if etd_proto == 8:
                (version, header_lengtd, ttl, proto, src, target, data) = ipv4_Packet(data)
                print(TAB_1 + "IPV4 Packet:")
                print(TAB_2 + 'Version: {}, Header Lengtd: {}, TTL: {}'.format(version, header_lengtd, ttl))
                print(TAB_3 + 'protocol: {}, Source: {}, Target: {}'.format(proto, src, target))
               
                config.F['EtdFdest_mac']=dest_mac
                config.F['EtdFsrc_mac']=src_mac
                config.F['EtdFdata']=data
                config.F['EtdFetd_proto']=proto
                config.F['version']=version
                config.F['header_lengtd']=header_lengtd
                config.F['ttl']=ttl
                config.F['src']=format(src)
                config.F['target']=format(target)
                # ICMP
                if proto == 1:
                    icmp_type, code, checksum, data = icmp_packet(data)
                    print(TAB_1 + 'ICMP Packet:')
                    print(TAB_2 + 'Type: {}, Code: {}, Checksum: {},'.format(icmp_type, code, checksum))
                    print(TAB_2 + 'ICMP Data:')
                    print(format_output_line(DATA_TAB_3, data))
                ###########################
                    config.F['type']='ICMP'
                    config.F['ICMPtype']=icmp_type
                    config.F['ICMPcode']=code
                    config.F['ICMPchecksum']=checksum
                    config.F['EtdFetd_proto']=proto

                # TCP
                elif proto == 6:
                    src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin = struct.unpack(
                '! H H L L H H H H H H', raw_data[:24])
                    print(TAB_1 + 'TCP Segment:')
                    print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
                    print(TAB_2 + 'Sequence: {}, Acknowledgment: {}'.format(sequence, acknowledgment))
                    print(TAB_2 + 'Flags:')
                    print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}'.format(flag_urg, flag_ack, flag_psh))
                    print(TAB_3 + 'RST: {}, SYN: {}, FIN:{}'.format(flag_rst, flag_syn, flag_fin))
                #######################

                    config.F['type']='TCP'
                    config.F['EtdFetd_proto']=proto
                    if len(data) > 0:
                        # HTTP
                        if src_port == 80 or dest_port == 80:
                            config.F['type']='TCP_HTTP'
                            print(TAB_2 + 'HTTP Data:')
                            try:
                                http = HTTP(data)
                                http_info = str(http.data).split('\n')
                                for line in http_info:
                                    print(DATA_TAB_3 + str(line))
                            except:
                                print(format_output_line(DATA_TAB_3, data))
                        else:
                            print(TAB_2 + 'TCP Data:')
                            print(format_output_line(DATA_TAB_3, data))
                    config.F['TCPdestP']=format(dest_port)
                    config.F['TCPsrcP']=format(src_port)
                # UDP
                elif proto == 17:
                    src_port, dest_port, lengtd, data = udp_seg(data)
                    print(TAB_1 + 'UDP Segment:')
                    print(TAB_2 + 'Source Port: {}, Destination Port: {}, Lengtd: {}'.format(src_port, dest_port, lengtd))
                    config.F['type']='UDP'
                    config.F['EtdFetd_proto']=proto
                # Otder IPv4
                else:
                    print(TAB_1 + 'Otder IPv4 Data:')
                    print(format_output_line(DATA_TAB_2, data))

            else:
                print('Etdernet Data:')
                print(format_output_line(DATA_TAB_1, data))
           
            print(config.F)
            for count in range(maxi):
                 config.Full[count]=config.F
            print ('the count is:', count)
            count = count + 1




# Unpack Etdernet Frame
def etdernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    print('**********tdis is tde unpack etder frame fct ')
    print(get_mac_addr(dest_mac))
    print(socket.htons(proto))
    print(data[14:])
    print('**********tdis is tde end of tde unpack etder frame fct ')
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]
#toop done!!!
    # Format MAC Address
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr

# Unpack IPv4 Packets Recieved
def ipv4_Packet(data):
    version_header_len = data[0]
    version = version_header_len >> 4
    header_len = (version_header_len & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_len, ttl, proto, ipv4(src), ipv4(target), data[header_len:]

# Returns Formatted IP Address
def ipv4(addr):
    return '.'.join(map(str, addr))


# Unpacks for any ICMP Packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    print('hiiiiiiiii from icmp packet')
    print(icmp_type+'code'+code+checksum+'data'+data[4:])
    return icmp_type, code, checksum, data[4:]

# Unpacks for any TCP Packet
def tcp_seg(data):
    (src_port, destination_port, sequence, acknowledgenment, offset_reserv_flag) = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserv_flag >> 12) * 4
    flag_urg = (offset_reserved_flag & 32) >> 5
    flag_ack = (offset_reserved_flag & 32) >>4
    flag_psh = (offset_reserved_flag & 32) >> 3
    flag_rst = (offset_reserved_flag & 32) >> 2
    flag_syn = (offset_reserved_flag & 32) >> 1
    flag_fin = (offset_reserved_flag & 32) >> 1

    return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]


# Unpacks for any UDP Packet
def udp_seg(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, size, data[8:]

# Formats tde output line
def format_output_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size-= 1
            return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


main()
print('lovly dictnry is working ')
print(config.Full)
print(config.F)