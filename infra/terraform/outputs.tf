
output "bountydns_server_public_ip" {
  value = "${aws_instance.main.public_ip}"
}

output "route53_zone_name_servers" {
  value = "${join(",", aws_route53_zone.main.name_servers)}"
}
