# Super Simple Python Webserver
This is a simple python webserver. It's meant to be expanded upon with program logic, security features and whatever else your project will need.

When I have need a simple website, I always start with this as my template.

Just update the `build.sh` and `run.sh` scripts with your docker container registry and you're ready to start testing.

# server.py

The program lives at `app/server.py` and right now there's not too much program logic in it. Just the basics where text is returned properly as UTF-8 text and non-text (eg images) is returned properly as bytes.

The functions for parsing and using parameters are here, but they don't do anything right now beyond just list the parameters received.

The goal here is to be expandable, you start with what's here and by adding a few functions you can have a super basic website that words reliably well.

Additionally, the `html` content is stored in `.html` files so that syntax highlighting and other nice IDE features will work.