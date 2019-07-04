# Packer

This directory contains the necessary configurations to build an AMI pre-baked with BountyDNS.

**Note: running the build will destroy any other AMIs that have the same name. You can increment the "version" variable to create duplicates.**

## Building the AMI

### Setting the Environment Variables

Copy `env.sh.example` to `env.sh` and set the appropriate variables. Make sure you have an AWS profile that can build EC2s.

### Running the Build

```
$ packer build -on-error=ask config.json
```
