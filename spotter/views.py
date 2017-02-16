from django.shortcuts import render
from spotter.models import *
import Queue as Q
# Create your views here.

sampleSizeFraction = 4

words_remaing = 0
currentWord = 0

q = Q.PriorityQueue()

def generate_matrix(word, start_from, sample_n):
	for x in range(start_from, start_from + word):
		print x
		word = Word(count_n = sample_n, idd = x)
		word.save()
		for y in range(1, 1 + sample_n):
			name = "word" + str(x) + "sample" + str(y) + ".png"
			sample = Sample(name = name, root = word)
			sample.save()


def init():
	total_words = Sample.objects.filter().count()
	words_remaing = total_words / sampleSizeFraction

	sample = Sample.objects.filter()
	flag = False

	for x in range(sample.count()):
		if sample[x].succesRatio != 0.5:
			flag = True
			break

	print "Flag = " + str(flag)
	if flag is True:
		for x in range(sample.count()):
			if sample[x].timesShown != 0:
				sample[x].succesRatio = sample[x].timesCorrected / float(sample[x].timesShown)
				sample.save()
				q.put([abs(0.5 - sample[x].succesRatio), sample[x].name])

	for x in range(sample.count()):
		q.put([sample[x].succesRatio, sample[x].name])


def index(request):
	if words_remaing <= 8:
		init()

	context = {}
	for x in range(9):
		context["str" + str(x)] = "/static/" + str(q.queue[x][1]) + ".png"
		print q.queue[x][1], q.queue[x][0]

	# context["str1"] = "/static/aman.jpg"

	print context
	return render(request, 'users/index2.html', context)


