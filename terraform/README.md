# Terraform Configurations

We use [Terraform](https://www.terraform.io/) to deploy the picoCTF platform to
a cloud provider, such as Amazon AWS, Google Cloud, or DigitalOcean. This folder
is used to manage different deployment types and document the cases in which
each might be used.

If you are not familiar with Terraform, it is recommended that you read through
through the [introduction](https://www.terraform.io/intro/index.html) and
[getting started](https://www.terraform.io/intro/getting-started/install.html)
prior to deploying picoCTF. For details on setting up resources on a specific
provider, see the provider-specific documentation found on the Terraform
website.

## Warnings

**Running Terraform on its own does not start the CTF.** Terraform simply sets
up the resources you need, such as domain names and servers, on a cloud
provider. You will need to run a few steps (including an Ansible playbook) to
finish configuring your CTF for launch.

Also, be advised that in most cases, using Terraform to set up resources will
incur costs on whatever cloud provider you choose to use. On some providers, you
can get some trial credits or, if you are an educator, educational credits. The
cost of any resources you create is your responsibility. Be sure to destroy (not
just shut down) any resources that you are not using.

When updating this folder, **do not include access tokens in any files that are
committed**. You can store such tokens in a file called `private.auto.tfvars` -
the value of any variable in that file will be added automatically when running
Terraform. The file `private.auto.tfvars` is ignored by Git, helping you avoid
accidentally adding and committing it. In each folder, a file called
`private-template.tfvars` shows variables that you *must* set to successfully
run Terraform.

## Configurations

* `digitalocean_single_tier`: A single-tier setup on DigitalOcean. This will
  require you to set up the database on the Web server, and is generally not
  recommended for large CTFs.

