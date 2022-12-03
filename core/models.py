from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=60)
    path = models.CharField(max_length=200)

    class Meta:
        ordering = ("name",)
        db_table = 'image'

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=500)

    class Meta:
        ordering = ("title",)
        db_table = 'news'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=70, db_index=True, unique=True)
    cnpj = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='images/')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=False)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

    def get_available(self):
        return "Yes" if self.available else "No"


class History(models.Model):
    battle_name = models.CharField(max_length=60)
    image = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=500)
    curiosity = models.CharField(max_length=500)

    class Meta:
        ordering = ("battle_name",)
        db_table = 'history'

    def __str__(self):
        return self.battle_name


class Chapter(models.Model):
    name = models.CharField(max_length=60)
    image = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    catchphrase = models.CharField(max_length=300)

    class Meta:
        ordering = ("name",)
        db_table = 'chapter'

    def __str__(self):
        return self.name
