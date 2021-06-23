# Docker Stack for AiiDAlab demonstration deployments

This repo contains the Docker file used for AiiDAlab demonstration deployments.

Docker images are available from Dockerhub via `docker pull aiidalab/aiidalab-docker-stack-demo:latest`.
See [aiidalab/aiidalab-docker-stack](https://hub.docker.com/repository/docker/aiidalab/aiidalab-docker-stack-demo) for a list of available tags.

# Deploy locally

Make sure that Docker is installed on your machine, otherwise go to [Docker installation page](http://www.docker.com/install)
and follow the instructions for your operating system.

Then, start the AiiDAlab demo server with:
```
./run.sh PORT PATH_TO_AIIDALAB_HOME_DIR
```

Where `PORT` is any free port on your machine (typically it is 8888) and `PATH_TO_AIIDALAB_HOME_DIR` is an absolute path to the folder where user's data will be stored
(typically it is something like `${HOME}/aiidalab`).
The last line of the output of the command above will contain the link to access AiiDAlab in your browser.

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
