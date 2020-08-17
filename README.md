# dataset-yt8m
----
## Processing dataset of yt8m.
yt8m is a open dataset which contain large amount of human labeled youtube videos. This repo provide scripts to process these data into training-ready format for different purpose.

#### Step1
Run `./download.sh` to download yt8m video level data.

The data is a set of tfrecord files.

#### Step2
Run `python tfrecord_to_csv.py --category {{category}}` to convert tfrecord extension to csv extension.

#### Step3

Run `python get_ytid_and_cap.py --category {{category}}` to retrive english captions and map yt8m id to youtube id.

{{category}} is used for spliting data into multiple part and run parallely.

**NOTE**: not all of video has reachable english captions.

#### Step4

Run `python preprocessing.py` to 

1. select videos which has caption.

2. combine yt label.

3. clean text.
