#!/usr/bin/env bash
current="$(pwd)"
mkdir -p $current/video
cd $current/video

curl data.yt8m.org/download.py | partition=2/video/train mirror=us python
curl data.yt8m.org/download.py | partition=2/video/validate mirror=us python
curl data.yt8m.org/download.py | partition=2/video/test mirror=us python

cd -
