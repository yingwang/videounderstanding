import csv

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
        
        for i in range(0, 20):
            labelConfidentialParisVideo[i * 2 + 1] = float(labelConfidentialParisVideo[i * 2 + 1]) * 0.5 + classPro[int(labelConfidentialParisVideo[i * 2])] * 0.5
            if labelConfidentialParisVideo[i * 2 + 1] > max:
            	max = labelConfidentialParisVideo[i * 2 + 1]
            	index = labelConfidentialParisVideo[i * 2]
        if index != labelConfidentialParisVideo[0]:
        	print videoRow[0]
        	count = count + 1
        writer.writerow([videoRow[0] + ',' + index + ' ' + str(max)])
print count
