# Smog Framework (beta)

### A semi-automatic osint/recon framework.

### How to use it:

`git clone https://github.com/traumatism/Smog/`
`cd Smog`
`py -m Smog`

### THIS IS IN BETA

```
.
├── clean.sh
├── LICENSE
├── README.md
└── smog
   ├── __init__.py
   ├── __main__.py
   ├── abstract
   │  ├── command.py
   │  ├── module.py
   │  └── type.py
   ├── banner
   │  ├── __init__.py
   │  └── banner.py
   ├── commands
   │  ├── add.py
   │  ├── clear.py
   │  ├── credits.py
   │  ├── help.py
   │  ├── python.py
   │  ├── run.py
   │  ├── select.py
   │  ├── show.py
   │  └── use.py
   ├── database
   │  ├── __init__.py
   │  ├── database.py
   │  └── types
   │     ├── __init__.py
   │     ├── domain.py
   │     ├── ip_address.py
   │     ├── subdomain.py
   │     └── url.py
   ├── logger
   │  ├── __init__.py
   │  └── logger.py
   ├── modules
   │  ├── crtsh.py
   │  ├── resolve.py
   │  └── test.py
   └── shell
      ├── __init__.py
      ├── arguments.py
      └── shell.py
```
