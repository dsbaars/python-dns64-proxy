Python DNS64 proxy
==================

This is a very dirty and quick, experimental implementation of an DNS64 proxy in Python 3.

__Use at your own risk__! I don't know anything about programming DNS servers, I just used the first library I thought was suitable (dnslib), and hacked away using trail and error until I got the basics working. Feel free to fork and improve.

Why?
----
I was experimenting with creating IPv6-only networks, which requires NAT64 and DNS64 if you want to keep visiting the outside world.

NAT64 can be done using tayga.
DNS64 can be done with TOTD or BIND. TOTD seems to be dead (can't find any code) and I don't want to run BIND just to do DNS64.
This allows me to keep using DNSMasq.

License
-------
MIT
