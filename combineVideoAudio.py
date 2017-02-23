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


classPro = list();
for i in range(0, 4800):
   classPro.append(0.0)
#print classPro
count = 0
for videoRow in readVideo:
    #print(videoRow[0],videoRow[1])
    labelConfidentialParisVideo = videoRow[1].split()
    # confidence of first label is high, skip audio
    if float(labelConfidentialParisVideo[1]) > 0.1:
    	#print labelConfidentialParisVideo[1]
        skipAudioRow = next(readAudio)
        writer.writerow([videoRow[0] + ',' + videoRow[1]])
    	#writer.writerow([videoRow[0], ',', videoRow[1]])
    #TODO: Write video line to CSV
    # take audio into account
    else:
        audioRow = next(readAudio)
        labelConfidentialParisAudio = audioRow[1].split()
        for i in range(0, 20):
            classPro[int(labelConfidentialParisAudio[i * 2])] = float(labelConfidentialParisAudio[i * 2 + 1]);
        max = 0
        index = 0
        
        #video confidence low, combine video and audio
        videoPairs = list()
        pair = namedtuple("Pair", ["label", "probablity"])
        for i in range(0, 20):
        	probablity = float(labelConfidentialParisVideo[i * 2 + 1]) * 0.615 + classPro[int(labelConfidentialParisVideo[i * 2])] * 0.385
        	videoPairs.append(pair(int(labelConfidentialParisVideo[i * 2]), probablity))
        #print videoPairs
        #print "----"
        videoPairs = sorted(videoPairs, key=attrgetter('probablity'), reverse=True)
        #print videoPairs
        #print "----------"
        #print "----------"
        if videoPairs[0].label != labelConfidentialParisVideo[i * 2]:
        	count = count + 1
        	#print str(videoPairs[0].label) + " " + labelConfidentialParisVideo[i * 2]
        outputline = ""
        for i in range(0, 20):
        	outputline = outputline + str(videoPairs[i].label) + ' ' + str(videoPairs[i].probablity) + ' '
        #writer = csv.writer(outputfile, delimiter ='|',quotechar =' ',quoting=csv.QUOTE_MINIMAL)
        # writer = csv.writer(outputfile, delimiter='|')
        writer.writerow([videoRow[0] + ',' + outputline])
print count
