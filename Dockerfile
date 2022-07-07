#FROM jupyter/scipy-notebook:python-3.10.5

FROM jupyter/scipy-notebook:python-3.8.8



# Install from requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/

RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


#COPY --chown=${NB_UID}:${NB_GID} docker-setup.sh /tmp/

RUN papermill setup.ipynb /tmp/setup__out.ipynb  && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"