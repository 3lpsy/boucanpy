ZONE_TEMPLATE= '''
$TTL    120
@                IN      SOA     {domain_name}. root.{domain_name}. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
ns1              IN      A       {domain_ip}
ns2              IN      A       {domain_ip}
@                IN      A       {domain_ip}
*                IN      CNAME   {domain_name}
@                IN      NS       ns1.{domain_name}.
@                IN      NS       ns2.{domain_name}.
'''