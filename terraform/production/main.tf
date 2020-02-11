# Terraform configuration to deploy picoCTF to Digital Ocean (production)
# Author: Steve Matsumoto <stephanos.matsumoto@sporic.me>

variable do_token {}

variable "region" {
  default = "nyc3"
}

provider "digitalocean" {
  token = var.do_token
}

###
# Environmental Configuration
# All variables are currently commented out because the defaults for the
# single_tier_aws module match a production deployment configuration.
# See the testing environment for an example of variables being overloaded.
###

resource "digitalocean_ssh_key" "default" {
  name = "CTFLab Production Key"
  public_key = file("~/.ssh/ctflab_production_ecdsa.pub")
}

resource "digitalocean_droplet" "web" {
  image = "ubuntu-18-04-x64"
  ipv6 = true
  name = "ctflab-web"
  private_networking = true
  region = var.region
  size = "s-1vcpu-1gb"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
}

resource "digitalocean_domain" "web" {
  name = "ctf.practicalsecurity.cc"
}

resource "digitalocean_record" "web_a" {
  domain = digitalocean_domain.web.name
  name = "@"
  type = "A"
  value = digitalocean_droplet.web.ipv4_address
}

resource "digitalocean_record" "web_aaaa" {
  domain = digitalocean_domain.web.name
  name = "@"
  type = "AAAA"
  value = digitalocean_droplet.web.ipv6_address
}

resource "digitalocean_record" "web_caa_letsencrypt" {
  domain = digitalocean_domain.web.name
  flags = "0"
  name = "@"
  tag = "issue"
  type = "CAA"
  value = "letsencrypt.org."
}

resource "digitalocean_droplet" "shell" {
  image = "ubuntu-18-04-x64"
  ipv6 = true
  name = "ctflab-shell"
  private_networking = true
  region = var.region
  size = "s-1vcpu-1gb"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
}

resource "digitalocean_domain" "shell" {
  name = "shell.ctf.practicalsecurity.cc"
  ip_address = digitalocean_droplet.shell.ipv4_address
}

resource "digitalocean_record" "shell_a" {
  domain = digitalocean_domain.shell.name
  name = "@"
  type = "A"
  value = digitalocean_droplet.shell.ipv4_address
}

resource "digitalocean_record" "shell_aaaa" {
  domain = digitalocean_domain.shell.name
  name = "@"
  type = "AAAA"
  value = digitalocean_droplet.shell.ipv6_address
}

resource "digitalocean_record" "shell_caa_letsencrypt" {
  domain = digitalocean_domain.shell.name
  flags = "0"
  name = "@"
  tag = "issue"
  type = "CAA"
  value = "letsencrypt.org."
}

###
# Output:
# Return the following to the user for configuring the ansible inventory
###

output "web_ipv4" {
  value = digitalocean_droplet.web.ipv4_address
}

output "web_ipv4_private" {
  value = digitalocean_droplet.web.ipv4_address_private
}

output "shell_ipv4" {
  value = digitalocean_droplet.shell.ipv4_address
}

output "shell_ipv4_private" {
  value = digitalocean_droplet.shell.ipv4_address_private
}

