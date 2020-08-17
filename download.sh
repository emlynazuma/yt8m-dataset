#!/usr/bin/env bash
current="$(pwd)"
mkdir -p $current/data/yt8m_raw
cd $current/data/yt8m_raw

curl data.yt8m.org/download.py | partition=2/video/train mirror=us python
curl data.yt8m.org/download.py | partition=2/video/validate mirror=us python
curl data.yt8m.org/download.py | partition=2/video/test mirror=us python

cd -
