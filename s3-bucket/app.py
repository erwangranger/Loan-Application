# from ast import Str
# from calendar import month
# from cmath import nan
# from distutils.archive_util import make_zipfile
# from faulthandler import disable
# from numpy import number
# from logging import getLogger
# from PIL import Image
import streamlit as st
# import time
# import pandas as pd
# import math
import os

st.set_page_config(
    page_title="S3 - Bucket Helper",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Bucket helper")
st.subheader("for the rest of us")

if 'bn' not in st.session_state:
    st.session_state.bn = 'my-bucket'



bucket_name = st.text_input(
    "In the following box, change the bucket name",
    placeholder='type your username here (without "installfest" and without @redhat.com)',
    disabled=False,
    # value= 'my-bucket',
    value=st.session_state.bn,
    key='mytext',
)

ro="s3_"+bucket_name+"_ro"
rw="s3_"+bucket_name+"_rw"

st.subheader("What these instructions will do")

st.write("""
* Create an S3 bucket called `"""+bucket_name+"""`
* Create an IAM role  called `"""+rw+"""`
* Create an IAM role  called `"""+ro+"""`
* Create an IAM user  called `"""+rw+"""`
* Create an IAM user  called `"""+ro+"""`
* Attach the policies to the users
* Generate the IAM credentials matching these users
"""
)

with st.expander("✨ Create an S3 bucket ("+bucket_name+")"):
    st.write(
        """
        ```bash
        aws s3api create-bucket \\
            --bucket """+bucket_name+""" \\
            --region us-east-1
        ```
        """
        )
    st.write(
        """
        Confirm that it has no content:

        ```bash
        aws s3 ls """+bucket_name+"""
        ```
        """
        )

with st.expander("✨ Create an IAM role  ("+rw+")"):
    st.write(
        """
        * create the policy file:
        ```bash
        cat << EOF > """+rw+""".json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
                    ],
                    "Resource": [
                        "arn:aws:s3:::"""+bucket_name+"""",
                        "arn:aws:s3:::"""+bucket_name+"""/*"
                    ]
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::"""+bucket_name+"""/*"
                }
            ]
        }
        EOF
        ```
        """
        )
    st.write(
        """
        * apply it to create the policy:
        ```bash
        aws iam create-policy \\
            --policy-name """+rw+""" \\
            --policy-document file://"""+rw+""".json

        ```
        """
        )


with st.expander("✨ Create an IAM role  ("+ro+")"):
    st.write(
        """
        * create the policy file:
        ```bash
        cat << EOF > """+ro+""".json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
                    ],
                    "Resource": [
                        "arn:aws:s3:::"""+bucket_name+"""",
                        "arn:aws:s3:::"""+bucket_name+"""/*"
                    ]
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": "s3:ListAllMyBuckets",
                    "Resource": "*"
                }
            ]
        }
        EOF
        ```
        """
        )
    st.write(
        """
        * apply it to create the policy:
        ```bash
        aws iam create-policy \\
            --policy-name """+ro+""" \\
            --policy-document file://"""+ro+""".json
        ```
        """
        )

with st.expander("✨ Create an IAM user  ("+rw+")"):
    st.write(
        """
        * create the user
        ```bash
        aws iam create-user \\
            --user-name """+rw+"""
        ```
        """
        )
    
with st.expander("✨ Create an IAM user  ("+ro+")"):
    st.write(
        """
        * create the user
        ```bash
        aws iam create-user \\
            --user-name """+ro+"""
        ```
        """
        )

with st.expander("✨ Attach the policies to the users"):
    st.write(
        """
        * rw:
            ```bash
            export RW_POL=$(aws iam list-policies \\
                --query 'Policies[?PolicyName==`"""+rw+"""`].Arn' \\
                --output text)
            echo ${RW_POL}
            
            aws iam attach-user-policy \\
                --policy-arn  ${RW_POL} \\
                --user-name """+rw+"""
            ```
        * ro:
            ```bash
            export RO_POL=$(aws iam list-policies \\
                --query 'Policies[?PolicyName==`"""+ro+"""`].Arn' \\
                --output text)
            echo ${RO_POL}
            
            aws iam attach-user-policy \\
                --policy-arn  ${RO_POL} \\
                --user-name """+ro+"""
            ```
        """
        )

with st.expander("✨ Generate the IAM credentials matching these users"):
    st.write(
        """
        * rw:
            ```bash
            aws iam create-access-key \\
                --user-name  """+rw+""" \\
                | tee ./"""+rw+""".keys.txt
            ```
        * ro:
            ```bash
            aws iam create-access-key \\
                --user-name  """+ro+""" \\
                | tee ./"""+ro+""".keys.txt
            ```
        """
        )

with st.expander("✨ Generate the IAM credentials matching these users"):
    st.write(
        """
        * rw:
            ```bash
            aws iam create-access-key \\
                --user-name  """+rw+""" \\
                | tee ./"""+rw+""".keys.txt
            ```
        * ro:
            ```bash
            aws iam create-access-key \\
                --user-name  """+ro+""" \\
                | tee ./"""+ro+""".keys.txt
            ```
        """
        )
