from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from spotter.models import *
import Queue as Q
import decimal, json
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
	q = Q.PriorityQueue()
	total_words = Sample.objects.filter().count()
	words_remaing = total_words / sampleSizeFraction

	print "Init running", words_remaing

	sample = Sample.objects.filter()
	flag = False

	for x in range(sample.count()):
		if sample[x].succesRatio != 0.5:
			flag = True
			break

	# print "Flag = " + str(flag)
	if flag is True:
		for x in range(sample.count()):
			if sample[x].timesShown != 0:
				sample[x].succesRatio = sample[x].timesCorrected / float(sample[x].timesShown)
				sample.save()
				q.put([abs(sample[x].succesRatio - decimal.Decimal(0.5)), sample[x].name])

	for x in range(sample.count()):
		q.put([abs(sample[x].succesRatio - decimal.Decimal(0.5)), sample[x].name])


	PQ.objects.all().delete()

	rank = 1
	for x in range(sample.count()):
		element = q.get()
		new_element = PQ(names = element[1], rank = rank)
		new_element.save()
		rank = rank + 1


def receive(request):
	if request.method == "POST":
		# print request.POST.items()
		for key, value in request.POST.items():

			# import pdb; pdb.set_trace()
			# print key[8:-4]
			sample = Sample.objects.get(name = key[8:-4])

			# print "Correct ->" + key[8:-4]
			if value == "1":
				sample.timesCorrected = int(sample.timesCorrected) + 1

			# print sample.timesShown, "--------------!!!!!"
			sample.timesShown = int(sample.timesShown) + 1

			sample.save()

			# print sample.timesShown, "--------------!!!!!"

			print key, value

	images = PQ.objects.all().order_by("id")
	for x in range(9):
		print "deleted -- >", images[x].names
		images[x].delete()	

	name = "Aman"
	return HttpResponse(json.dumps({'name': name}), content_type="application/json")


def index(request):
	pq = PQ.objects.filter()
	cnt = pq.count()

	print cnt

	if cnt <= 8:
	# if words_remaing <= 8:
		init()

	context = {}
	images = PQ.objects.all().order_by("id")

	# import pdb; pdb.set_trace()

	for x in range(9):
		# context["str" + str(x)] = "/static/" + str(q.queue[x][1]) + ".png"
		context["str" + str(x)] = "/static/" + images[x].names + ".png"
		# print q.queue[x][1], q.queue[x][0]

	# print context
	return render(request, 'users/index.html', context)


