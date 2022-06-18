# Base Notebook
# FROM jupyter/tensorflow-notebook:7a0c7325e470
FROM jupyter/tensorflow-notebook:latest

# Include some ML learning lessons and tutorials in the standard image
# RUN mkdir learn
# COPY ./learn ./learn
# USER root
# RUN sudo chown -R 1000:100 ./learn

# Install system libraries and tools
USER root
RUN apt-get -qq update && apt-get install -y alien libaio1 unixodbc unixodbc-dev graphviz

# Install Oarcle instant client (required for cx_Oracle python library)
RUN wget -q https://download.oracle.com/otn_software/linux/instantclient/195000/oracle-instantclient19.5-basic-19.5.0.0.0-1.x86_64.rpm && \
    alien -i oracle-instantclient19.5-basic-19.5.0.0.0-1.x86_64.rpm && \
    rm -f oracle-instantclient19.5-basic-19.5.0.0.0-1.x86_64.rpm
ENV PATH="/usr/lib/oracle/19.5/client64/lib/:${PATH}"

# Add python3 libraries
RUN python3 -m pip install --no-cache \
    jupyterhub==1.0.0 \
    keras==2.3.0 \
    pmdarima \
    cx_Oracle \
    mysql-connector \
    teradata \
    teradatasql \
    pydotplus \
    holidays \
    dash \  
    chart-studio \  
    jupyter-dash \
    pandas-profiling==2.9.0 \
    jupyter-notebookparams \
    jupyter_contrib_nbextensions && jupyter contrib nbextension install 

# Enable extensions    
RUN jupyter nbextension install --py jupyter_notebookparams --sys-prefix && jupyter nbextension enable --py jupyter_notebookparams --sys-prefix && jupyter nbextension enable codefolding/main

# Add xgboost
# RUN conda install --quiet --yes -c conda-forge xgboost fbprophet

# Add the R kernel and libraries
# RUN conda install --quiet --yes \
#    'r-base' \
#    'r-irkernel' \
#    'r-plyr' \
#    'r-devtools' \
#    'r-tidyverse' \
#    'r-shiny' \
#    'r-rmarkdown' \
#    'r-forecast' \
#    'r-rsqlite' \
#    'r-reshape2' \
#    'r-nycflights13' \
#    'r-caret' \
#    'r-rcurl' \
#    'r-crayon' \
#    'r-randomforest' \
#    'r-htmltools' \
#    'r-sparklyr' \
#    'r-htmlwidgets' \
#    'r-gridextra' \
#    'r-hexbin' && \
#    conda clean -tipsy && \
#    fix-permissions $CONDA_DIR
# ENV CPATH=$CONDA_DIR/include
# COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/
