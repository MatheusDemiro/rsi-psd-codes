# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 14:32:04 2018
@author: Glauco
"""

import subnetcalc as sb
import sys

"""
    Each entry in this table indicates the network address, 
    the network mask, and the forwarding interface.
"""
table = {
            ('41.0.1.0','24'): 3,
            ('41.0.1.192','26'): 2,
            ('20.100.0.0','19'): 1,
            ('0.0.0.0','0'): 4
        }

tableToBin = {}
"""
    Each entry in the list below is the destination address
    of a given packet.
""" 
packets = ['20.100.32.1', '41.0.1.200']

def forwarding(ip,tbl):
    """
        Receives the destination ip address and chooses the route
        based on the longest prefix match againt the routing table.
        Inputs:
            ip: ip address (string)
            tbl: routing table (dict whose the value is the forwarding interface and the key is a tuple with network address and netmask)
        
        Returns: the forwarding interface
    """

    """
        Please change here
    """
    ipToInt = sb.ip2int(ip)
    result = {}
    for i in tbl:
        net,broad = sb.getNetAndBroadAddr(i[0],i[1])
        firstToInt = sb.ip2int(sb.int2ip(net+1))
        lastToInt = sb.ip2int(sb.int2ip(broad-1))
        #Verificando se o ip se encontra na faixa de algum endereçamento de rede da tabela de roteamento
        if ipToInt >= firstToInt and ipToInt <= lastToInt:
            comparation = bin(firstToInt & ipToInt)[2:] #Comparar bit a bit do primeiro ip de rede com o ip do pacote
            result[comparation.count("1")] = (sb.int2ip(net), i[1])
    if result:
        return tbl[result[max(result)]]
    else:
        return -1 #Return -1 quando nao ha valor correspondente na tabela de enderecamento
           
           
if __name__ == "__main__":
    if len(sys.argv) == 3:
        tblfile = sys.argv[1]
        ip = sys.argv[2]
        try:
            tbl = dict()
            tblpointer = file(tblfile)
            for line in tblpointer:
                fields = line.split(",")
                tbl[(fields[0],fields[1])] = int(fields[2].strip("\n"))
        except:
            print("Problem")
        intf = forwarding(ip,table);
        print("The packet with dest addr",ip,"will be forwarded to interface", intf)
    else:
        for ip in packets:
            intf = forwarding(ip,table);
            print("The packet with dest addr",ip,"will be forwarded to interface", intf)
