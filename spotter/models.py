from __future__ import unicode_literals
from decimal import Decimal
 
from django.db import models

class General(models.Model):
	# count of words shiwn uptill now
	count_w = models.IntegerField(default=0)

	# counts of words shown uptill now
	count_s = models.IntegerField(default=0)
 
class Word(models.Model):

	# Number of samples this word has.
    idd = models.IntegerField(null=False, primary_key = True)
    count_n = models.IntegerField(null=False)
    # isShown = models.BooleanField(default=False)
 
class Sample(models.Model):
    root = models.ForeignKey(Word)
    
    name = models.CharField(default = "", max_length = 13)
    # The number of times any image is shown.
    timesShown = models.IntegerField(default = 0)

    # The number of times marked as corrected
    timesCorrected = models.IntegerField(default = 0)

    # The success ratio matrix
    succesRatio = models.DecimalField(max_digits=20,decimal_places=4, default=Decimal('0.5'))

