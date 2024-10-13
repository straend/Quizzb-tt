from django.db import models

from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
import os


class ExamScore(models.Model):
    exam = models.ForeignKey("Exam", related_name="scores", on_delete=models.CASCADE)
    user = models.ForeignKey("DiscoUser", related_name="scores", on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    taken = models.DateTimeField(auto_created=True, blank=True, null=True)

class Exam(models.Model):
    name = models.CharField(max_length=300)
    pub_date = models.DateTimeField("date published")
    uuid = models.CharField(max_length=50)
    def score_count(self):
        return self.scores.count()
    
    def __str__(self):
        return f"{self.name}"

class DiscoUser(models.Model):
    name = models.CharField(max_length=200)
    discord_id = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}"
    
    def score_for_exam(self, exam: Exam):
        res = ExamScore.objects.filter(exam=exam, user=self).first()
        if res is None:
            return "-"
        return f"{res.score}"



class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    #exam = models.OneToOneField(Exam, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField()
    question_text = models.TextField()
    correct = models.OneToOneField("Choice", on_delete=models.CASCADE, related_name="correct", null=True)
    image = models.ImageField(null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    description_img = models.ImageField(blank=True, null=True)
    
    def load_image(self, image_id):
        #img_tmp = NamedTemporaryFile(delete=True)
        url = f"https://images.cdn.yle.fi/image/upload/fl_keep_iptc,f_auto,fl_progressive/q_80/w_600,c_fill,dpr_1.0/v1725524611/{image_id}.jpg"
        result = requests.get(url)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(result.content)
        img_temp.flush()

        self.image.save(os.path.basename(url), File(img_temp), save=True)
        #self.image.save(image_id, File(image_id, result.content))
    
    def load_image_desc(self, image_id):
        #img_tmp = NamedTemporaryFile(delete=True)
        url = f"https://images.cdn.yle.fi/image/upload/fl_keep_iptc,f_auto,fl_progressive/q_80/w_600,c_fill,dpr_1.0/v1725524611/{image_id}.jpg"
        result = requests.get(url)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(result.content)
        img_temp.flush()

        self.description_img.save(os.path.basename(url), File(img_temp), save=True)
        #self.description_img.save(img_tmp.name, img)
        
    def __str__(self):
        return f"{self.question_text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.choice_text}"
