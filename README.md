# dataset-yt8m
----
##Processing dataset of yt8m

#### Step1
Run `./download.sh` to download yt8m video level data.

The data is a set of tfrecord files.

#### Step2
Run `python dataset.py --category {{category}}` to map yt8m id to youtube id.

{{category}} is used for spliting data into multiple part and run parallely.

**NOTE**: not all of id can map to youtube id.

#### Step3

Run `python get_transcription.py --category {{category}}` to retrive english captions.

{{category}} is used for spliting data into multiple part and run parallely.

**NOTE**: not all of video has reachable english captions.

