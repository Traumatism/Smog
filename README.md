# Smog Framework (beta)

## A semi-automatic osint/recon framework.

![](preview.png)

## How to use it:

`git clone https://github.com/traumatism/Smog/`

`cd Smog`

`py -m Smog`

Add a domain for example

`add domain domain.com`

Scan for subdomains with differents modules

`use crtsh`

`run`

`use hackertarget`

`run`

...

Now lets use the data we gathered to resolve the subdomains to IP addresses

`use resolve`

`run`

The process is quasi-infinite. You can add more modules to get more informations and add modules that uses these informations (that why its "semi-automatic", the actions order is decided by the human)

## TODO:

### Modules

* URL scanning
* Endpoints scanning
* Vulnerability scanning

### Features

* Export to json or plain text
* Add a workspace system
* Multiple queries executions with ";" or "&&"

## THIS IS IN BETA
