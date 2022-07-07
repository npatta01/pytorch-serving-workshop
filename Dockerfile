#FROM jupyter/scipy-notebook:python-3.10.5

FROM jupyter/scipy-notebook:python-3.8.8



# USER root
# # apt-utils is missing and needed to avoid warning about skipping debconf
# RUN apt-get update && apt-get --yes install apt-utils
# # install whatever else you want on this line
# RUN apt-get --yes install htop tmux -y
# # set the user back to original setting
# USER $NB_UID



# Install from requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/

RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


#COPY --chown=${NB_UID}:${NB_GID} docker-setup.sh /tmp/

COPY --chown=${NB_UID}:${NB_GID} setup.ipynb /tmp/

RUN papermill /tmp/setup.ipynb /tmp/setup__out.ipynb -k python3 --log-output --log-level DEBUG --progress-bar && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"