from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        db_table='user'

    def __str__(self):
        return self.name

class Log(models.Model):
    classification = models.CharField(max_length=255)
    input = models.CharField(max_length=255,unique=True)
    output = models.CharField(max_length=255)
    class Meta:
        db_table='log'

class Corpus(models.Model):
    classification = models.CharField(max_length=255)
    word = models.CharField(max_length=255)
    class Meta:
        db_table='corpus'

class Base_Classification(models.Model):
    classification = models.CharField(max_length=255)
    phrase = models.CharField(max_length=255)
    class Meta:
        db_table='base_classification'

class Base_Previous(models.Model):
    classification = models.CharField(max_length=255)
    phrase = models.CharField(max_length=255,null=True)
    class Meta:
        db_table='base_previous'

class Base_Response(models.Model):
    classification = models.CharField(max_length=255)
    phrase = models.CharField(max_length=255)
    class Meta:
        db_table='base_response'

class Base_Next(models.Model):
    classification = models.CharField(max_length=255)
    phrase = models.CharField(max_length=255,null=True)
    class Meta:
        db_table='base_next'
