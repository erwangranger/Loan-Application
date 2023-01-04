#!/bin/bash

python3 -m venv myvenv

source myvenv/bin/activate

# install the required packages
python3.10 -m pip install streamlit

# start the Streamlit application
python3.10 -m streamlit run app.py

deactivate
