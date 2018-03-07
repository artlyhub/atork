from django.db import models


def scramble_uploaded_image(instance, filename):
    extension = filename.split(".")[-1]
    return "item/{}.{}".format(uuid.uuid4(), extension)


class FundItem(models.Model):
    artist = models.CharField(max_length=50)
    image = models.ImageField(upload_to=scramble_uploaded_image, blank=True)
    name = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    estimate_min_price = models.IntegerField()
    estimate_max_price = models.IntegerField()
    hammer_price = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.artist, self.image)


class Funder(models.Model):
    funditem = models.ForeignKey(FundItem, related_name='funditems')
    funder_name = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    amount = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.funder_name, self.funditem.name)
