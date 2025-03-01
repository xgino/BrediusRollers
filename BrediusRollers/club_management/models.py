from django.db import models

class Profile(models.Model):
    firstname = models.CharField(max_length=50, verbose_name="First Name*")
    lastname = models.CharField(max_length=50, verbose_name="Last Name*")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def get_full_name(self):
        # Handle NoneType for firstname and lastname
        first_name = self.firstname if self.firstname else ""
        last_name = self.lastname if self.lastname else ""
        if not first_name and not last_name:
            return ""
        return f"{first_name} {last_name}"

    def get_short_name(self):
        # Return short name with handling for NoneType
        if self.firstname and self.lastname:
            return f"{self.firstname[0]}. {self.lastname}"
        elif self.firstname:
            return self.firstname[0] + "."
        elif self.lastname:
            return self.lastname
        return ""

class Address(models.Model):
    street = models.CharField(max_length=128, verbose_name="Street*")
    house_number = models.CharField(max_length=128, verbose_name="Housenumber*")
    zipcode = models.CharField(max_length=5, verbose_name="Zipcode Number*")
    zipcode_number = models.CharField(max_length=128, verbose_name="Zipcode Letter*")
    place = models.CharField(max_length=64, verbose_name="City*")

    def __str__(self):
        return self.street + " " + self.house_number

    def get_street(self):
        return self.street + ' ' + self.house_number
    
    def get_zip(self):
        return self.zipcode + ' ' + self.zipcode_number + ' ' + self.place

class Club(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name*")
    logo = models.ImageField(upload_to="clubs/", blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    members  = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Coach(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}"

class Role(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Title*")

    def __str__(self):
        return f"{self.title} - {self.profile}"

class Sponsor(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title*")
    logo = models.ImageField(upload_to="sponsors/")

    def __str__(self):
        return f"{self.title}"

class TrainingTime(models.Model):
    start_time = models.TimeField(verbose_name="Start Time*")
    end_time = models.TimeField(verbose_name="End Time*")

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class TrainingLocation(models.Model):
    location = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location}"