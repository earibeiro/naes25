from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.abbreviation
    
class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        unique_together = ('name', 'state')

    def __str__(self):
        return f"{self.name}, {self.state.abbreviation}"
    
class Person(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pessoas_fisicas')

    def __str__(self):
        return f"{self.name} ({self.cpf})"
    
class Company(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pessoas_juridicas')

    def __str__(self):
        return f"{self.name} ({self.cnpj})"
    


