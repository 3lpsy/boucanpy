
provider "aws" {
  version = "~> 2.0"
  region  = "${var.aws_default_region}"
}


### NETWORKING
resource "aws_vpc" "main" {
  cidr_block           = "${var.vpc_cidr}"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "bountydns-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.main.id}"

  tags = {
    Name = "bountydns-ig"
  }
}


resource "aws_subnet" "main" {
  vpc_id     = "${aws_vpc.main.id}"
  cidr_block = "${cidrsubnet(aws_vpc.main.cidr_block, 8, 0)}"

  tags = {
    Name = "bountydns-subnet"
  }
}

resource "aws_network_acl" "main" {
  vpc_id     = "${aws_vpc.main.id}"
  subnet_ids = ["${aws_subnet.main.id}"]

  tags = {
    Name = "bountydns-acl"
  }
}

resource "aws_network_acl_rule" "dashboard_ingress" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 100
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "${var.trusted_external_cidr_block}"
  from_port      = 8080
  to_port        = 8080
}

resource "aws_network_acl_rule" "ssh_ingress" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 200
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "${var.trusted_external_cidr_block}"
  from_port      = 22
  to_port        = 22
}

resource "aws_network_acl_rule" "http_ingress" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 300
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "${var.internet_cidr_block}"
  from_port      = 80
  to_port        = 80
}

resource "aws_network_acl_rule" "https_ingress" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 400
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "${var.internet_cidr_block}"
  from_port      = 443
  to_port        = 443
}


resource "aws_network_acl_rule" "dns_tcp_ingress" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 500
  egress         = false
  protocol       = "tcp"
  rule_action    = "allow"
  cidr_block     = "${var.internet_cidr_block}"
  from_port      = 53
  to_port        = 53
}

resource "aws_network_acl_rule" "dns_udp_ingress" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 600
  egress         = false
  protocol       = "udp"
  rule_action    = "allow"
  cidr_block     = "${var.internet_cidr_block}"
  from_port      = 53
  to_port        = 53
}

resource "aws_network_acl_rule" "all_outbound" {
  network_acl_id = "${aws_network_acl.main.id}"
  rule_number    = 700
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "${var.internet_cidr_block}"
  from_port      = 0
  to_port        = 65535
}

resource "aws_route_table" "main" {
  vpc_id = "${aws_vpc.main.id}"

  tags = {
    Name = "bountydns-rt"
  }
}

resource "aws_route" "egress" {
  route_table_id         = "${aws_route_table.main.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.main.id}"
}

resource "aws_route_table_association" "main" {
  subnet_id      = "${aws_subnet.main.id}"
  route_table_id = "${aws_route_table.main.id}"
}


### Security Groups 

resource "aws_security_group" "main" {
  name        = "bountydns-sg"
  description = "A Generica Security Group for a BountyDNS Server"
  vpc_id      = "${aws_vpc.main.id}"
}

# TODO: make restrictive
resource "aws_security_group_rule" "allow_all_in" {
  type              = "ingress"
  from_port         = 0
  to_port           = 65535
  protocol          = -1
  cidr_blocks       = ["${var.internet_cidr_block}"]
  security_group_id = "${aws_security_group.main.id}"
}

resource "aws_security_group_rule" "allow_all_out" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = -1
  cidr_blocks       = ["${var.internet_cidr_block}"]
  security_group_id = "${aws_security_group.main.id}"
}


### EC2(s)

#### Pull latest ami

resource "aws_key_pair" "main" {
  key_name   = "bountydns-key"
  public_key = "${file("${path.root}/data/key.pem.pub")}"
}

resource "aws_instance" "main" {
  ami                    = "ami-0f951f1a641b201ef"
  instance_type          = "t2.micro"
  subnet_id              = "${aws_subnet.main.id}"
  vpc_security_group_ids = ["${aws_security_group.main.id}"]
  key_name               = "${aws_key_pair.main.key_name}"

  associate_public_ip_address = true
  tags = {
    Name = "bountydns-server"
  }
}


### Environment + Secrets 

#### Database 

resource "random_pet" "db_database" {
  length    = 2
  separator = "_"
}
resource "random_pet" "db_username" {
  length    = 2
  separator = "_"
}
resource "random_string" "db_password" {
  length  = 32
  special = false
}

#### do not use single quotes
data "template_file" "db_env" {
  template = <<-EOT
POSTGRES_DB="${random_pet.db_database.id}"
POSTGRES_USER="${random_pet.db_username.id}"
POSTGRES_PASSWORD="${random_string.db_password.result}"
EOT
}


#### Proxy 

#### do not use single quotes
data "template_file" "proxy_env" {
  template = <<-EOT
SSL_ENABLED="0"
INSECURE_LISTEN_PORT="8080"
API_BACKEND_PROTO="http"
API_BACKEND_HOST="bountydns"
API_BACKEND_PORT="8080"
DEBUG_CONF="1"
EOT
}

#### Broadcast 

resource "random_string" "broadcast_password" {
  length  = 24
  special = false
}

#### do not use single quotes
data "template_file" "broadcast_env" {
  template = <<-EOT
REDIS_PASSWORD="${random_string.broadcast_password.result}"
REDIS_MASTER_HOST="redis"
EOT
}


### Configuration
resource "null_resource" "server_configure" {
  triggers = {
    server_id = "${aws_instance.main.id}"
    db_env = "${data.template_file.db_env.rendered}"
    proxy_env = "${data.template_file.proxy_env.rendered}"
    broadcast_env = "${data.template_file.broadcast_env.rendered}"
  }

  connection {
    host = "${aws_instance.main.public_ip}"
    type = "ssh"
    user = "ubuntu"
    private_key = "${file("${path.root}/data/key.pem")}"
    agent = false # change to true if agent is required
  }

  provisioner "remote-exec" {
    inline = [
      "echo '${data.template_file.db_env.rendered}' | sudo tee /etc/bountydns/env/db.prod.env",
      "echo '${data.template_file.proxy_env.rendered}' | sudo tee /etc/bountydns/env/proxy.prod.env",
      "echo '${data.template_file.broadcast_env.rendered}' | sudo tee /etc/bountydns/env/broadcast.prod.env",
    ]
  }
}

### Route53

resource "aws_route53_zone" "main" {
  name = "${var.dns_root}"
}

resource "aws_route53_record" "a" {
  zone_id = "${aws_route53_zone.main.zone_id}"
  name = "${var.dns_sub}.${var.dns_root}"
  type = "A"
  ttl = "5"
  records = ["${aws_instance.main.public_ip}"]
}

resource "aws_route53_record" "ns" {
  zone_id = "${aws_route53_zone.main.zone_id}"
  name = "${var.dns_sub}.${var.dns_root}"
  type = "NS"
  ttl = "5"
  records = ["${var.dns_sub}.${var.dns_root}."]
}
