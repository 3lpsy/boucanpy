
output "bountydns_server_public_ip" {
  value = "${aws_instance.main.public_ip}"
}

output "bountydns_server_url" {
  value = "http://${var.dns_dashboard_sub}.${var.dns_root}:8080"
}


