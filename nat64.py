from __future__ import print_function

import binascii,socket,struct,ipaddress

from dnslib import DNSRecord,DNSError,QTYPE,RCODE,RR,DNSHeader,DNSQuestion,A,AAAA
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger

DNS_AAAA_RECORD = 28
DNS_A_RECORD = 1

class DNS64ProxyResolver(BaseResolver):
    def __init__(self,address,port,timeout=0):
        self.address = address
        self.port = port
        self.timeout = timeout

    def resolve(self,request,handler):
        try:
            if handler.protocol == 'udp':
                orig_proxy_r = request.send(self.address,self.port,
                            timeout=self.timeout)
                reply = DNSRecord.parse(orig_proxy_r)

                if request.q.qtype == DNS_AAAA_RECORD and (len(reply.rr) < 1 or reply.rr[0].rtype != DNS_AAAA_RECORD):
                    request.q.qtype = DNS_A_RECORD
                    orig_proxy_r = request.send(self.address,self.port,
                                timeout=self.timeout)
                    orig_reply = DNSRecord.parse(orig_proxy_r)
                    request.q.qtype = DNS_AAAA_RECORD

                    prefix6to4 = int(ipaddress.IPv6Address("fdcb:b3ab:4522:fa5a::"))
                    if len(orig_reply.rr) > 0:
                        reply = DNSRecord(DNSHeader(id=orig_reply.header.id,qr=1,ra=1), q=request.q)

                        for r in orig_reply.rr:
                            ip6 = ipaddress.IPv6Address(prefix6to4 | (int(ipaddress.IPv4Address(r.rdata))))
                            reply.add_answer(RR(request.q.qname, rtype=DNS_AAAA_RECORD, ttl=r.ttl, rdata=AAAA(str(ip6))))
            else:
                proxy_r = request.send(self.address,self.port,
                                tcp=True,timeout=self.timeout)
        except socket.timeout:
            reply = request.reply()
            reply.header.rcode = getattr(RCODE,'NXDOMAIN')

        return reply

if __name__ == '__main__':
    import argparse,sys,time
    resolver = DNS64ProxyResolver("8.8.8.8", 53, 5)
    handler = DNSHandler
    logger = DNSLogger([],False)
    udp_server = DNSServer(resolver,
                           port=5354,
                           address="0.0.0.0",
                           logger=None,
                           handler=handler)
    udp_server.start_thread()

    while udp_server.isAlive():
        time.sleep(1)
