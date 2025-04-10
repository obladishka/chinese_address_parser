from django.db import models


class Province(models.Model):
    """Provinces sourcebook."""
    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")
    popularity = models.PositiveIntegerField(
        verbose_name="province popularity",
        help_text="Fills in automatically",
        default=0
    )


class City(models.Model):
    """Cities sourcebook."""
    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name="1st parent item",
        help_text="Select the 1st parent item according to address hierarchy",
        related_name="cities"
    )
    popularity = models.PositiveIntegerField(
        verbose_name="province popularity",
        help_text="Fills in automatically",
        default=0
    )


class SpecialWord(models.Model):
    """Special words' sourcebook."""
    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")
    popularity = models.PositiveIntegerField(
        verbose_name="province popularity",
        help_text="Fills in automatically",
        default=0
    )


class AddressObject(models.Model):
    """Address objects' sourcebook."""
    cn_name = models.CharField(max_length=200, verbose_name="name in Chinese", unique=True)
    eng_name = models.CharField(max_length=200, verbose_name="name in English")
    is_parent_item = models.BooleanField(verbose_name="parent items or not")
    hierarchy = models.DecimalField(
        verbose_name="object hierarchy",
        help_text="Select object's hierarchy in address",
        decimal_places=1,
        max_digits=2
    )
