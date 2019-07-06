# Environment Variables & Secrets

This holds the example/dev environment variables. To boot in "prod" (via packer/terraform), the compose.sh will assume the environment variables are stored in `/etc/bountydns/env`. This folder is created automatically via packer and is seed by terraform. To build manually, simply copy x.dev.env or x.env.example to /etc/bountydns/env/x.prod.env (if using docker-compose).
