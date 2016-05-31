#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""ping.py
 
 ping.py uses the ICMP protocol's mandatory ECHO_REQUEST
 datagram to elicit an ICMP ECHO_RESPONSE from a
 host or gateway.
 Copyright (C) 2004 - Lars Strand <lars strand at gnist org>;
 
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 Must be running as root, or write a suid-wrapper. Since newer *nix
 variants, the kernel ignores the set[ug]id flags on #! scripts for
 security reasons
 RFC792, echo/reply message:
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |     Type      |     Code      |          Checksum             |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |           Identifier          |        Sequence Number        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |     Data ...
 +-+-+-+-+-

TODO:
 - do not create socket inside 'while' (but if not: ipv6 won't work)
 - add support for broadcast/multicast
 - add support for own payload string
CHANGELOG:
 DONE -->; bugfix from Filip Van Raemdonck mechanix debian org
 DONE -->; add more support for modules (raise instead of sys.exit)
 DONE -->; locale func names
 DONE -->; package def
 DONE -->; some code cleanup
 
"""
import sys
import os
import struct
import array
import time
import select
import binascii
import math
import getopt
import string
import socket
#import signal
import subprocess

import thread
import threading
import public

#from multiprocessing import Process,Queue
# total size of data (payload)
ICMP_DATA_STR = 56  
# initial values of header variables
ICMP_TYPE = 8
ICMP_TYPE_IP6 = 128
ICMP_CODE = 0
ICMP_CHECKSUM = 0
ICMP_ID = 0
ICMP_SEQ_NR = 0

RECEIVED_PACK = 0
TRANSMIT_PACK = 0 
#RUN_PING_FLAG = True
# Package definitions.
__program__   = 'ping'
__version__   = '0.5a'
__date__      = '2004/15/12'
__author__    = 'Lars Strand <lars at unik no>;'
__licence__   = 'GPL'
__copyright__ = 'Copyright (C) 2004 Lars Strand'

global ping_error_str 

ping_error_str = 'a'

def ping_error():
    global ping_error_str
    return ping_error_str 


def _error(err):
    """Exit if running standalone, else raise an exception
    """
    if __name__ == '__main__':
        print "%s: %s" % (os.path.basename(sys.argv[0]), str(err))
        print "Try `%s --help' for more information." % os.path.basename(sys.argv[0])
        sys.exit(1)
    else:
        raise Exception, str(err)
        return None
    
def _usage():
    """Print usage if run as a standalone program
    """
    print """usage: %s [OPTIONS] HOST
Send ICMP ECHO_REQUEST packets to network hosts.
Mandatory arguments to long options are mandatory for short options too.
  -c, --count=N    Stop after sending (and receiving) 'N' ECHO_RESPONSE
                   packets.
  -s, --size=S     Specify the number of data bytes to be sent. The default
                   is 56, which translates into 64 ICMP data bytes when
                   combined with the 8 bytes of ICMP header data.
  -f, --flood      Flood ping. Outputs packets as fast as they come back. Use
                   with caution!
  -6, --ipv6       Ping using IPv6.
  -t, --timeout=s  Specify a timeout, in seconds, before a ping packet is
                   considered 'lost'.
  -h, --help       Display this help and exit
Report bugs to lars [at] gnist org""" % os.path.basename(sys.argv[0])




class ping_thread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)  
        self.t_name = name
        self.RUN_PING_FLAG = True
        
    
    def setvalue(self,node,alive, timeout, ipv6, count, flood, size):
        self.alive = alive
        self.timeout = timeout
        self.ipv6 = ipv6
        self.number =count
        self.node = node
        self.flood = flood
        self.size = ICMP_DATA_STR
        
    def _construct(self,id, size, ipv6):
        """Constructs a ICMP echo packet of variable size
        """
        # size must be big enough to contain time sent
        if size < int(struct.calcsize("d")):
            _error("packetsize to small, must be at least %d" % int(struct.calcsize("d")))
    
        # construct header
        if ipv6:
            header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, ICMP_CHECKSUM, \
                                ICMP_ID, ICMP_SEQ_NR+id)
        else:
            header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, ICMP_CHECKSUM, \
                                ICMP_ID, ICMP_SEQ_NR+id)
        # if size big enough, embed this payload
        load = "-- IF YOU ARE READING THIS YOU ARE A NERD! --"
    
        # space for time
        size -= struct.calcsize("d")
        # construct payload based on size, may be omitted :)
        rest = ""
        if size >len(load):
            rest = load
            size -= len(load)
        # pad the rest of payload
        rest += size * "X"
        # pack
        data = struct.pack("d", time.time()) + rest
        packet = header + data          # ping packet without checksum
        checksum = self._in_cksum(packet)    # make checksum
        # construct header with correct checksum
        if ipv6:
            header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, checksum, \
                                ICMP_ID, ICMP_SEQ_NR+id)
        else:
            header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, checksum, ICMP_ID, \
                                ICMP_SEQ_NR+id)
        # ping packet *with* checksum
        packet = header + data 
        # a perfectly formatted ICMP echo packet
        return packet
    
    
    def _in_cksum(self,packet):
        """THE RFC792 states: 'The 16 bit one's complement of
        the one's complement sum of all 16 bit words in the header.'
        Generates a checksum of a (ICMP) packet. Based on in_chksum found
        in ping.c on FreeBSD.
        """
        # add byte if not dividable by 2
        if len(packet) & 1:              
            packet = packet + '\0'
        # split into 16-bit word and insert into a binary array
        words = array.array('h', packet) 
        sum = 0
        # perform ones complement arithmetic on 16-bit words
        for word in words:
            sum += (word & 0xffff) 
        hi = sum >> 16 
        lo = sum & 0xffff 
        sum = hi + lo
        sum = sum + (sum >> 16)
    
        return (~sum) & 0xffff # return ones complement
    
    def stop(self):
        self.RUN_PING_FLAG = False
        
    def run(self):
        """Pings a node based on input given to the function.
        """
        
        alive = self.alive
        timeout = self.timeout
        ipv6 = self.ipv6
        number = self.number
        node = self.node
        flood = self.flood
        size = self.size
        
        global RECEIVED_PACK
        global TRANSMIT_PACK
        #global RUN_PING_FLAG
        # if no node, exit
        if not node:
            _error("")
        # if not a valid host, exit
        if ipv6:
            if socket.has_ipv6:
                try:
                    info, port = socket.getaddrinfo(node, None)
                    host = info[4][0]
                    # do not print ipv6 twice if ipv6 address given as node
                    if host == node: 
                        noPrintIPv6adr = 1
                except:
                    _error("cannot resolve %s: Unknow host_666" % node)
            else:
                _error("No support for IPv6 on this plattform")
        else:    # IPv4
            try:
                host = socket.gethostbyname(node)
            except:
                _error("cannot resolve %s: Unknow host__11" % node)
        # trying to ping a network?
        if not ipv6:
            if int(string.split(host, ".")[-1]) == 0:
                _error("no support for network ping")
        # do some sanity check
        if number == 0:
            _error("invalid count of packets to transmit: '%s'" % str(a))
        if alive:
            number = 1
        # Send the ping(s)
        start = 1; mint = 999; maxt = 0.0; avg = 0.0
        lost = 0; tsum = 0.0; tsumsq = 0.0
        # tell the user what we do
        if not alive:
            if ipv6:
                # do not print the ipv6 twice if ip adress given as node
                # (it can be to long in term window)
                if noPrintIPv6adr == 1:
                    # add 40 (header) + 8 (icmp header) + payload
                    print "PING %s : %d data bytes (40+8+%d)" % (str(node), \
                                                             40+8+size, size)
                else:
                    # add 40 (header) + 8 (icmp header) + payload
                    print "PING %s (%s): %d data bytes (40+8+%d)" % (str(node), \
                                                                 str(host), 40+8+size, size)
            else:
                # add 20 (header) + 8 (icmp header) + payload
                print "PING %s (%s): %d data bytes (20+8+%d)" % (str(node), str(host), \
                                                             20+8+size, size)
        
        # trap ctrl-d and ctrl-c
        try:
        
            # send the number of ping packets as given
            while start <= number:
            
                if  self.RUN_PING_FLAG ==False:
                    print 'RUN_PING_FLAG',self.RUN_PING_FLAG
                    alive = 0
                    break
                lost += 1 # in case user hit ctrl-c
            
                # create the IPv6/IPv4 socket
                if ipv6:
                    # can not create a raw socket if not root or setuid to root
                    try:
                        pingSocket = socket.socket(socket.AF_INET6, socket.SOCK_RAW, \
                                               socket.getprotobyname("ipv6-icmp"))
                    except socket.error, e:
                        print "socket error: %s" % e
                        _error("You must be root (uses raw sockets)" % os.path.basename(sys.argv[0]))
                    
                # IPv4
                else:
                    # can not create a raw socket if not root or setuid to root
                    try:
                        pingSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, \
                                               socket.getprotobyname("icmp"))
                    except socket.error, e:
                        print "socket error: %s" % e
                        _error("You must be root (%s uses raw sockets)" % os.path.basename(sys.argv[0]))
                
                packet = self._construct(start, size, ipv6) # make a ping packet
                g_mutex = threading.Lock() 
                g_mutex.acquire() 
                RECEIVED_PACK = start-lost
                TRANSMIT_PACK = start-1
                g_mutex.release()
                # send the ping
                try:
                    pingSocket.sendto(packet,(node,1))
                except socket.error, e:
                    _error("socket error: %s" % e)
                # reset values
                pong = ""; iwtd = []
                # wait until there is data in the socket
                while 1:
                    # input, output, exceptional conditions
                    iwtd, owtd, ewtd = select.select([pingSocket], [], [], timeout)
                    break # no data and timout occurred 
                # data on socket - this means we have an answer
                if iwtd:  # ok, data on socket
                    endtime = time.time()  # time packet received
                    # read data (we only need the header)
                    pong, address = pingSocket.recvfrom(size+48)
                    lost -= 1 # in case user hit ctrl-c
                    # examine packet
                    # fetch TTL from IP header
                
                    if ipv6:
                        # since IPv6 header and any extension header are never passed
                        # to a raw socket, we can *not* get hoplimit field..
                        # I hoped that a socket option would help, but it's not
                        # supported:
                        #   pingSocket.setsockopt(IPPROTO_IPV6, IPV6_RECVHOPLIMIT, 1)
                        # so we can't fetch hoplimit..
                        # fetch hoplimit
                        #rawPongHop = struct.unpack("c", pong[7])[0]
                        # fetch pong header
                        pongHeader = pong[0:8]
                        pongType, pongCode, pongChksum, pongID, pongSeqnr = \
                                struct.unpack("bbHHh", pongHeader)
                        # fetch starttime from pong
                        starttime = struct.unpack("d", pong[8:16])[0]
                    # IPv4
                    else:
                        # time to live
                        rawPongHop = struct.unpack("s", pong[8])[0]
                        # convert TTL from 8 bit to 16 bit integer
                        pongHop = int(binascii.hexlify(str(rawPongHop)), 16)
                        # fetch pong header
                        pongHeader = pong[20:28]
                        pongType, pongCode, pongChksum, pongID, pongSeqnr = \
                                struct.unpack("bbHHh", pongHeader)
                        # fetch starttime from pong
                        starttime = struct.unpack("d", pong[28:36])[0]
                    # valid ping packet received?
                    if not pongSeqnr == start:
                        pong = None
                # NO data on socket - timeout waiting for answer
                if not pong:
                    if alive:
                        print "no reply from %s (%s)" % (str(node), str(host))
                    else:
                        print "ping timeout: %s (icmp_seq=%d) " % (host, start)
                    # do not wait if just sending one packet
                    if number != 1 and start < number:
                        time.sleep(flood ^ 1)
                    start += 1
                    continue  # lost a packet - try again
                triptime  = endtime - starttime # compute RRT
                tsum     += triptime            # triptime for all packets (stddev)
                tsumsq   += triptime * triptime # triptime^2  for all packets (stddev)
                # compute statistic
                maxt = max ((triptime, maxt))
                mint = min ((triptime, mint))
                if alive:
                    print str(node) + " (" + str(host) +") is alive"
                else:
                    if ipv6:
                        # size + 8 = payload + header
                        print "%d bytes from %s: icmp_seq=%d time=%.5f ms" % \
                            (size+8, host, pongSeqnr, triptime*1000)
                    else:
                        #print '**************\n',pong
                        print "%d bytes from %s: icmp_seq=%d ttl=%s time=%.5f ms" % \
                            (size+8, host, pongSeqnr, pongHop, triptime*1000)
                # do not wait if just sending one packet
                if number != 1 and start < number:
                    # if flood = 1; do not sleep - just ping                
                    time.sleep(flood ^ 1) # wait before send new packet
                # the last thing to do is update the counter - else the value
                # (can) get wrong when computing summary at the end (if user
                # hit ctrl-c when pinging)
                start += 1
                # end ping send/recv while
        # if user ctrl-d or ctrl-c
        except (EOFError, KeyboardInterrupt):
            # if user disrupts ping, it is most likly done before
            # the counter get updates - if do not update it here, the
            # summary get all wrong.
            start += 1
            pass
        # compute and print som stats
        # stddev computation based on ping.c from FreeBSD
        if start != 0 or lost > 0:  # do not print stats if 0 packet sent
            start -= 1              # since while is '<='
            avg = tsum / start      # avg round trip
            vari = tsumsq / start - avg * avg 
            # %-packet lost
            if start == lost:
                plost = 100
            else:
                plost = (lost/start)*100
            if not alive:
            
                print "\n--- %s ping statistics ---" % node
                print "%d packets transmitted, %d packets received, %d%% packet loss" % \
                    (start, start-lost, plost)
                # don't display summary if 100% packet-loss
                if plost != 100:
                    print "round-trip min/avg/max/stddev = %.3f/%.3f/%.3f/%.3f ms" % \
                        (mint*1000, (tsum/start)*1000, maxt*1000, math.sqrt(vari)*1000)
        pingSocket.close()
    

class get_ping_thread(threading.Thread):
    
    def __init__(self,name):
        threading.Thread.__init__(self)  
        self.t_name = name
        self.get_flag = False
        self.lost_packet = 10 
    
    def setvalue(self,lost_packet = 10):
        self.lost_packet = lost_packet
        
    def getvalue(self):
        global RECEIVED_PACK
        global TRANSMIT_PACK
        return (RECEIVED_PACK,TRANSMIT_PACK)
    
    def run(self):
        global RECEIVED_PACK
        global TRANSMIT_PACK
        global ping_error_str
        while True:
            if self.get_flag:
                break
            time.sleep(5)
            g_mutex = threading.Lock()
            g_mutex.acquire()
            #RECEIVED_PACK = 0 
            #TRANSMIT_PACK = 0
            print "%d packets transmitted, %d packets received, %d%% packet loss" % \
                    (TRANSMIT_PACK, RECEIVED_PACK, (TRANSMIT_PACK-RECEIVED_PACK)*100/(TRANSMIT_PACK))
            
            if (TRANSMIT_PACK-RECEIVED_PACK)> self.lost_packet:
                print 'ping lost: %d Is greater than the specified number :%d ' %((TRANSMIT_PACK+1)-(RECEIVED_PACK+1),self.lost_packet)
                 
                ping_error_str = 'ping lost: %d Is greater than the specified number :%d ' %((TRANSMIT_PACK+1)-(RECEIVED_PACK+1),self.lost_packet)
                
            g_mutex.release()
    
    def stop(self):
        self.get_flag =True
        

    
def ping_node(node='192.168.4.29',alive='0', timeout='1', ipv6='0', count=str(sys.maxint), flood='0', size=str(ICMP_DATA_STR),name='ping_start'):
    
    thread1 = ping_thread('ping_thread')
    thread1.setvalue(node,string.atoi(alive), string.atoi(timeout), string.atoi(ipv6), string.atoi(count), string.atoi(flood), string.atoi(size))
    thread1.start()
    time.sleep(2)
    #thread1.stop()
    return thread1
    

def get_ping_count(num='5',thread1=ping_thread('ping_thread')):
    #global RECEIVED_PACK
    #global TRANSMIT_PACK
    time.sleep(1)
    thread1.stop()
    thread2 = get_ping_thread('get_ping')
    tmp_num = string.atoi(num)
    thread2.setvalue(tmp_num)
    time.sleep(1)
    thread2.start()
    time.sleep(3)
    tmp_tuple = thread2.getvalue()
    thread2.stop()
    #print 'get_ping_count tmp_tuple:',tmp_tuple
    #print RECEIVED_PACK
    #print TRANSMIT_PACK
    
    if (tmp_tuple[1]- tmp_tuple[0]) < (string.atoi(num)):
        return True
    else:
        return False
    

if __name__ == "__main__":  
    
    alive = 0; timeout = 1.0; ipv6 = 0; count = sys.maxint;
    flood = 0; size = ICMP_DATA_STR
    
    node = '192.168.4.105'
    pthread = ping_node(node)
    time.sleep(15)
    get_ping_count('5',pthread)
    
    time.sleep(50)
    print '**********  main *****************'
    print ping_error()
    #print ''

    