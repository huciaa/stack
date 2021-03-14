#!/bin/sh
aws s3 mv /home/ec2-user/unpack s3://stackdev2 --recursive
