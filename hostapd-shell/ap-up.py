from socket import AF_INET
from pyroute2 import IPRoute

# get access to the netlink socket
ip = IPRoute()

# print interfaces
print(ip.get_links())
print([x.get_attr('IFLA_IFNAME') for x in ip.get_links()])

#ip.link('set',
#        index=idx,
#        state = 'down')
