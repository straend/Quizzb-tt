from django.core.management.base import BaseCommand, CommandError
from ylequizz.models import Exam, Question, Choice
import requests
import regex

class Command(BaseCommand):
    help = "Load polls from yle"
    re = regex.compile(r"(.+)\s*\[IMS id=(.*?)\|.*\]")

    def handle(self, *args, **options):
        r = requests.get("https://tehtava.api.yle.fi/v1/public/series?series_uuids=422b3639-c6fc-41a8-93c0-b731a1fee682").json()
        citem = 0
        for exam in r['data'][0]['exams'][0:5]:
            print(f"Exam {citem}/{len(r['data'][0]['exams'])}")
            if Exam.objects.filter(uuid=exam['uuid']).first():
                print("Exam exists")
                citem+=1
                continue
  
            exam_url = "https://tehtava.api.yle.fi/v1/public/exams.json?uuid={}".format(exam['uuid'])
            exam_data = requests.get(exam_url).json()
            e = Exam(name=exam['name'], pub_date=exam['published_at'], uuid=exam['uuid'])
            e.save()
            for qu in exam_data['data'][0]['questions']:
                q = Question(
                    exam=e,
                    order = qu["order_number"],
                    question_text = qu["main_text"],
                )
                m = self.re.match(qu["main_text"])
                if (m):
                    q.question_text = m.group(1)
                    q.load_image(m.group(2))
                m2 = self.re.match(qu["feedback"])
                if m2:
                    q.description = m2.group(1)
                    q.load_image_desc(m2.group(2))
                else:
                    q.description = qu["feedback"]
                
                q.save()
                for opt in qu["options"]:
                    c = Choice(question=q, choice_text=opt["text"])
                    c.save()
                    if "correct" in opt and opt["correct"]==True:
                        q.correct = c
                        q.save()
            citem += 1
