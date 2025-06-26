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
    

class RetentionPolicy(models.Model):
    policy_name = models.CharField(max_length=100)    
    retention_period = models.PositiveIntegerField(help_text="Retention period in days")
    expiry_date = models.DateField(blank=True, null=True)    

class DataOwner(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='data_owners', blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='data_owners', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    retention_policy = models.ForeignKey(RetentionPolicy, on_delete=models.CASCADE, related_name='data_owners', blank=True, null=True)
   
    def __str__(self):
        if self.person:
            return f"Data Owner: {self.person.name}"
        elif self.company:
            return f"Data Owner: {self.company.name}"
        return "Data Owner"
    
    def _get_policy_name(self):
        if self.retention_policy:
            return self.retention_policy.policy_name
        return "No Retention Policy"

class RegisterLog(models.Model):
    data_owner = models.ForeignKey(DataOwner, on_delete=models.CASCADE, related_name='register_logs')
    action = models.CharField(max_length=50)  # e.g., 'create', 'update', 'delete'
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} by {self.data_owner} at {self.timestamp}"
    
class DataAccessLog(models.Model):
    data_owner = models.ForeignKey(DataOwner, on_delete=models.CASCADE, related_name='data_access_logs')
    accessed_by = models.CharField(max_length=100)  # Could be a user or system name
    access_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)  # e.g., 'view', 'edit', 'delete'
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.accessed_by} accessed {self.data_owner} at {self.access_time}"
    
class DataType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class AuditLog(models.Model):
    information = models.TextField()
    request = models.ForeignKey(DataAccessLog, on_delete=models.CASCADE, related_name='audit_logs')

    def __str__(self):
        return f"Audit Log for {self.request} - {self.information[:50]}..." if self.information else "Audit Log"