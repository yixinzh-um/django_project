import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from jobs.models import Job,Employer,Comment, Location


import re

def run():
    fhand = open('jobs/all_jobs.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    
    Job.objects.all().delete()
    Employer.objects.all().delete()
    Comment.objects.all().delete()

    for row in reader:
        s = re.findall('[0-9]+',row[2])

        des=row[3].replace('\n', ' <br />')

        sl=s[0]
        sh=s[1]
        try:
            sl= int(sl)
        except:
            sl = None
        try:
            sh=int(sh)
        except:
            lo = None
  
        # print(y,lo,la,a)
        

        employer, created = Employer.objects.get_or_create(name=row[5])
        location, created = Location.objects.get_or_create(name=row[6])
        job, created = Job.objects.get_or_create(title=row[1], employer=employer, location=location, salary_l=sl, salary_h=sh,description=des)

        employer.save()
        location.save()
        job.save()

