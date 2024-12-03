from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    picture = models.CharField(max_length=512)

    def __str__(self):
        return self.username


class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    is_active = models.BooleanField()
    is_public = models.BooleanField()
    created_on = models.DateField()
    expires_on = models.DateTimeField()

    def __str__(self):
        return self.title


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=128)

    def __str__(self):
        return self.option_text


class Vote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote {self.vote_id} on {self.option}"


class Friend(models.Model):
    user_id1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends1')
    user_id2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends2')
    status = models.IntegerField()

    class Meta:
        unique_together = ('user_id1', 'user_id2')

    def __str__(self):
        return f"Friendship between {self.user_id1} and {self.user_id2} - Status: {self.status}"
