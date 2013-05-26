from django.db import models


class Agency(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    agency = models.ForeignKey(Agency)

    def __unicode__(self):
        return '{0}, {1}'.format(self.name, self.title)


class AnnualSalary(models.Model):
    employee = models.ForeignKey(Employee)
    salary = models.IntegerField()
    year = models.IntegerField()

    def __unicode__(self):
        return '${0} in {1}'.format(self.salary, self.year)
