from django.db import models

# Create your models here.


class Location(models.Model):
    lat = models.DecimalField(max_digits=8, decimal_places=4)
    lon = models.DecimalField(max_digits=8, decimal_places=4)
    loc_description_text = models.CharField(max_length=200)

    def __str__(self):
        return f'Location: {self.loc_description_text}\n \
                            --> lat: {self.lat}, lon: {self.lon}'


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
