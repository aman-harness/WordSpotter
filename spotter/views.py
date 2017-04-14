from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from spotter.models import *
import Queue as Q
import decimal, json
import random
# Create your views here.

sampleSizeFraction = 4

words_remaing = 0
currentWord = 0

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

def init_m():
	q_max = Q.PriorityQueue()
	q_min = Q.PriorityQueue()

	print "Max, min running"

	sample = Sample.objects.filter()

	n_elements = sample.count()
	r = list(range(n_elements))
	random.shuffle(r)

	for x in r:
		q_max.put([abs(sample[x].succesRatio - decimal.Decimal(0)), sample[x].name])
		
	random.shuffle(r)
	for x in r:
		q_min.put([abs(sample[x].succesRatio - decimal.Decimal(1)), sample[x].name])

	PQ_min.objects.all().delete()
	PQ_max.objects.all().delete()

	rank = 0
	for x in range(sample.count()):
		element = q_max.get()
		new_element = PQ_max(names = element[1], rank = rank)
		new_element.save()

		element = q_min.get()
		new_element = PQ_min(names = element[1], rank = rank)
		new_element.save()
		rank = rank + 1


def receive(request):
	if request.method == "POST":
		for key, value in request.POST.items():

			sample = Sample.objects.get(name = key[8:-4])

			if value == "1":
				sample.timesCorrected = int(sample.timesCorrected) + 1

			sample.timesShown = int(sample.timesShown) + 1

			sample.save()


			print key, value

	images = PQ.objects.all().order_by("id")
	images_min = PQ_min.objects.all().order_by("id")
	images_max = PQ_max.objects.all().order_by("id")


	for x in range(4):
		print "deleted -- >", images[x].names
		images[x].delete()	

	images_min[0].delete()
	images_max[0].delete()

	name = "Aman"
	return HttpResponse(json.dumps({'name': name}), content_type="application/json")


def index(request):
	pq = PQ.objects.filter()
	cnt = pq.count()

	print cnt

	if cnt <= 5:
	# if words_remaing <= 8:
		init()
		init_m()

	context = {}
	images = PQ.objects.all().order_by("id")
	images_min = PQ_min.objects.all().order_by("id")
	images_max = PQ_max.objects.all().order_by("id")


	for x in range(4):
		context["str" + str(x)] = "/static/" + images[x].names + ".png"

	context["str" + str(4)] = "/static/" + images_min[0].names + ".png"
	context["str" + str(5)] = "/static/" + images_max[0].names + ".png"

	print context

	return render(request, 'users/index.html', context)


def redir(request):
	context = {}
	context['title'] = "spotter/"
	return render(request, 'users/basic.html', context)


