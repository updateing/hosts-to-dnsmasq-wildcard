Hosts to DNSMasq Configuration Converter
===

##Introduction

This tool will convert hosts to DNSMasq's dnsmasq.conf.

`192.168.1.2 www.somedomain.com` -> `address=/www.somedomain.com/192.168.1.2`

##Special feature
If one *IP address* has more than one (sub-)domain names related, this program will combine them into one line, using DNSMasq's wildcard feature.
```
192.168.1.2 video.somedomain.com
192.168.1.2 img.somedomain.com
192.168.1.2 static.somedomain.com
192.168.1.2 user.somedomain.com
192.168.1.2 www.mydom.com
```
->
```
address=/somedomain.com/192.168.1.2
address=/www.mydom.com/192.168.1.2
```
During my tests, a 9500-line Google IPv6 hosts was converted to a 411-line dnsmasq.conf

##Usage
`hosts-to-dnsmasq.conf InputHostFile OutputDnsmasqConfFile`

If `OutputDnsmasqConfFile` does not exist, it will be created.

If it exists, it will be **overwritten**.

Example: `host-to-dnsmasq.py /etc/hosts dnsmasq-append.conf`