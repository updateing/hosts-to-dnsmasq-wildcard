#!/usr/bin/python
'''
    Hosts to DNSMasq configuration converter

    Converts entries in a hosts file to dnsmasq conf,
    taking wildcard into consideration. All sub-domains
    are combined into one.
'''

import sys
import string

# TODO: use address to collect domains - that makes more sense
def findTopDomain(domain_name):
    countryName = ["cn", "sg", "jp", "hk", "uk", "ca", "ru", "kr", "gr", "bg", "cy", \
        "fi", "co", "au", "vi", "mn", "mm", "bn", "bz", "py", "ai", "ph", "pk", "pe", \
        "pg", "ar", "tj", "na", "ng", "nf", "fj", "np", "ni", "qa", "jm", "cu", "kw", \
        "kh", "sv", "af", "sl", "ag", "sa", "sb", "pr", "ly", "tr", "tw", "lb", "et", \
        "ec", "eg", "mx", "my", "mt", "uy", "br", "pa", "bd", "bo", "bh", "vn", "vc", \
        "ua", "gt", "om", "gh", "gi", "do", "th", "ma", "mz", "ug", "ke", "ls", "nz", \
        "zm", "za", "zw", "ve", "in", "il", "id", "ao", "uz", "ck", "cr", "bw", "tz"] # Common country codes used in Google hosts
    topDomains = ["com", "org", "net", "co"]
    domainElem = domain_name.split(".")
    if len(domainElem) < 4 and len(domainElem[0]) < 7: # enough to filter out "cdn-www.xda-developers.com" and "r12-xxxxxxx.googlevideo.com"
        return domain_name # TODO make it parameter (minimum parts to be truncated)

    realDomainAt = 0
    if domainElem[-1] not in countryName: # *.com
        return string.join(domainElem[-2:], ".")
    else:
        if domainElem[-2] not in topDomains: # *.cn
            return string.join(domainElem[-2:], ".")
        else: # *.com.cn, *.co.uk
            return string.join(domainElem[-3:], ".")

def processLine(line, address_map):
    line = line.strip();
    if line.startswith("#") or line == "":
        return # Skip comments and empty line
    else:
        lineElements = line.split()
        if len(lineElements) < 2:
            print "Malformed host line \"%s\", elements < 2" % line
            exit(1);
        topDomain = findTopDomain(lineElements[1])
        address_map[topDomain] = lineElements[0]

def writeDnsmasqConf(confFile, addressMap):
    lines = []
    for (key, value) in addressMap.items(): # TODO why?items()
        lines.append("address=/%s/%s" % (key, value) + "\n")
    confFile.writelines(lines)

# Main program
hostFile = open(sys.argv[1], "r")
masqFile = open(sys.argv[2], "w")
lines = hostFile.readlines()
addressMap = dict()
for line in lines:
    processLine(line, addressMap)
writeDnsmasqConf(masqFile, addressMap)

