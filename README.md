# Docker Stack for AiiDAlab demonstration deployments

This repository contains the Dockerfile used to define the AiiDAlab demonstration deployment.

Docker images are available from Dockerhub via `docker pull aiidalab/aiidalab-docker-stack-demo:latest`.
See [aiidalab/aiidalab-docker-stack](https://hub.docker.com/repository/docker/aiidalab/aiidalab-docker-stack-demo) for a list of available tags.

# How to deploy AiiDAlab locally

We recommend to use [Docker](https://docs.docker.com/) in combination with [Docker Compose](https://docs.docker.com/compose/) for a local deployment of AiiDAlab.

## Prerequisites

Please follow the official instructions on how to [get Docker](https://docs.docker.com/get-docker/) and how to [install Docker Compose](https://docs.docker.com/compose/install/) on your system.
The deployment has been tested with Docker version 20.10.7 and Docker Compose version 1.29.2.

The repository comes with a wrapper script (`control.py`) that simplifies starting and stopping the AiiDAlab server.
If you want to use that script, you will have to install the [Click library](https://click.palletsprojects.com) (tested with version 7.1.2), e.g., with:
```
pip install click
```

## Launch AiiDAlab

### Using the control script

To start AiiDAlab with the wrapper script, simply execute:
```terminal
$ ./control.py up
Starting AiiDAlab...
```
This will up the service with docker-compose which may take a few minutes.
After successful, start you should see a message similar to this:
```terminal
Container started successfully.
Open this link in the browser to enter AiiDAlab:
http://localhost:8888/?token=56e70f7f4263314c5e33faa9691501...
```

#### Stopping AiiDAlab

To stop the server, simply run
```console
./control.py down
```

#### Notes

 - The script assumes that AiiDAlab is started on the local host and also accessed from there. Accessing the server from a different machine will require port forwarding.
 - You will need to use the link with token the first time that you open AiiDAlab in your browser. After this, a cookie will be set such that subsequent access does not require the token. This will only work if cookies are disabled and you access the server from the same browser.

#### Options

You can specify the port and the host directory that is mounted as the AiiDAlab home directory with the control script.
Execute
```terminal
$ ./control.py up --help
```
to see all available options.

### Manual approach

To start the AiiDAlab demo deployment, execute:
```
docker-compose up -d --build
```
To check that the server is up and ready you can execute the following command:
```
docker-compose exec aiidalab wait-for-services
```
This command will block until the AiiDAlab server has started.

You can find the address to access AiiDAlab via:
```
docker-compose logs --tail=5
```

#### Options

 - The AiiDAlab home directory will be automatically mounted at `$HOME/aiidalab` in the host system, but you can override that by setting the `$AIIDALAB_HOME` variable to a different path.
- To override the default port, specify the `$AIIDALAB_PORT` variable.

To specify default variables for docker-compose, modify the [`.env` file](https://docs.docker.com/compose/environment-variables/#the-env-file).

## Citation

Users of AiiDAlab are kindly asked to cite the following publication in their own work:

A. V. Yakutovich et al., Comp. Mat. Sci. 188, 110165 (2021).
[DOI:10.1016/j.commatsci.2020.110165](https://doi.org/10.1016/j.commatsci.2020.110165)

# Acknowledgements

This work is supported by the [MARVEL National Centre for Competency in Research](<http://nccr-marvel.ch>)
funded by the [Swiss National Science Foundation](<http://www.snf.ch/en>), as well as by the [MaX
European Centre of Excellence](<http://www.max-centre.eu/>) funded by the Horizon 2020 EINFRA-5 program,
Grant No. 676598.

![MARVEL](miscellaneous/logos/MARVEL.png)
![MaX](miscellaneous/logos/MaX.png)
