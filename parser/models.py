from django.db import models


class Province(models.Model):
    """Provinces sourcebook."""

    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")


class SpecialWord(models.Model):
    """Special words' sourcebook."""

    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")


class AddressObject(models.Model):
    """Address objects' sourcebook."""

    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")
    is_parent_item = models.BooleanField(verbose_name="parent items or not")
    hierarchy = models.DecimalField(
        verbose_name="object hierarchy",
        help_text="Select object's hierarchy in address",
        decimal_places=1,
        max_digits=2,
    )
