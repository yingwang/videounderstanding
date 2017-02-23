import csv
from collections import namedtuple
from operator import attrgetter

videofile = open("/Users/yingwang/Downloads/predictions2.csv", "r")
audiofile = open("/Users/yingwang/Downloads/predictions00_logistic_model_audio_only.csv", "r")
outputfile = open("combined_predictions.csv", "w")

readVideo = csv.reader(videofile, delimiter=',')
firstVideoLine = next(readVideo)

writer = csv.writer(outputfile, delimiter=',')
#writer = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_NONE, quotechar='',escapechar='\\')
writer.writerow(firstVideoLine)
writer = csv.writer(outputfile, delimiter='|')

readAudio = csv.reader(audiofile, delimiter=',')
firstAudioLine = next(readAudio)

#print classPro
count = 0

# for each video
for videoRow in readVideo:
    # read in video prediction
    labelConfidentialParisVideo = videoRow[1].split()
    # confidence of first label is high, skip audio
    if float(labelConfidentialParisVideo[1]) > 0.5:
        skipAudioRow = next(readAudio)
        writer.writerow([videoRow[0] + ',' + videoRow[1]])

    # video confidence low, take audio into account
    else:
    	# init hashtable
    	ht1 = list()
    	for i in range(0, 4800):
   			ht1.append(0.0)
   		# read audio data into hashtable
        audioRow = next(readAudio)
        labelConfidentialParisAudio = audioRow[1].split()
        for i in range(0, 20):
            ht1[int(labelConfidentialParisAudio[i * 2])] = float(labelConfidentialParisAudio[i * 2 + 1]);
        max = 0
        index = 0
        
        # combine audio into video
        videoPairs = list()
        pair = namedtuple("Pair", ["label", "probablity"])
        for i in range(0, 20):
        	probablity = float(labelConfidentialParisVideo[i * 2 + 1]) * 0.615 + ht1[int(labelConfidentialParisVideo[i * 2])] * 0.385
        	videoPairs.append(pair(int(labelConfidentialParisVideo[i * 2]), probablity))
        # sort the list after recalculate probablity
        videoPairs = sorted(videoPairs, key=attrgetter('probablity'), reverse=True)

        # include remaining audio prediction
        # init hashtable
        ht2 = list()
    	for i in range(0, 4800):
            ht2.append(0.0)
   		# read video data into hashtable
        for i in range(0, 20):
   			ht2[int(labelConfidentialParisVideo[i * 2])] = float(labelConfidentialParisVideo[i * 2 + 1])
        # add Audio prediction into list
        for i in range(0, 20):
        	if ht2[int(labelConfidentialParisAudio[i * 2])] == 0:
        		videoPairs.append(pair(int(labelConfidentialParisAudio[i * 2]), float(labelConfidentialParisAudio[i * 2 + 1]) * 0.385))

        # calculation complete, write to file
        if videoPairs[0].label != labelConfidentialParisVideo[i * 2]:
        	count = count + 1
        	#print str(videoPairs[0].label) + " " + labelConfidentialParisVideo[i * 2]
        outputline = ""
        for i in range(0, 20):
        	outputline = outputline + str(videoPairs[i].label) + ' ' + str(videoPairs[i].probablity) + ' '
        writer.writerow([videoRow[0] + ',' + outputline])
# print how many entries changed 1st label
print count
