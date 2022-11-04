from django.db import models



class Adress(models.Model):
    street = models.CharField(max_length=128, verbose_name="Straat")
    house_number = models.CharField(max_length=128, verbose_name="Huisnummer")
    zipcode = models.CharField(max_length=5, verbose_name="Postcodenummers")
    zipcode_number = models.CharField(max_length=128, verbose_name="Postcode letters")
    place = models.CharField(max_length=64, verbose_name="Woonplaats")

    def __str__(self):
        return self.street + " " + self.house_number

    class Meta:
        verbose_name_plural = "Adressen"

    def get_street(self):
        return self.street + ' ' + self.house_number
    
    def get_zip(self):
        return self.zipcode + ' ' + self.zipcode_number + ' ' + self.place