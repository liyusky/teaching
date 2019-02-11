from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TypingStage(models.Model): #游戏关卡
    name = models.CharField(max_length=100, default="")
    #map = models.FileField(upload_to=map_directory_path, blank=True, null=True)#场景地图表
    #hint = models.TextField(default="")
    idx = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserStageStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(TypingStage, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "stage", )

    def __str__(self):
        return self.user.last_name + self.user.first_name + "," + self.stage.name