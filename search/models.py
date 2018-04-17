from django.db import models

class Process(models.Model):
    objects = models.Manager()

    cod = models.CharField(max_length=17,primary_key=True)
    serventia = models.CharField(max_length=40)
    comarca = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'process'
        verbose_name_plural = 'processes'


    def __str__(self):
        return self.cod




class ProcessFile(models.Model):
    objects = models.Manager()  
    
    id = models.CharField(max_length=50,primary_key=True)
    cod = models.ForeignKey(Process,on_delete=models.CASCADE)    

    class Meta:
        verbose_name = 'processfile'
        verbose_name_plural = 'processfiles'

    def __str__(self):
        return self.id



class Character(models.Model):
    objects = models.Manager()

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name = 'character'
        verbose_name_plural = 'characters'


    def __str__(self):
        return self.name



class ProcessCharacter(models.Model):
    objects = models.Manager()  
    
    process_cod = models.ForeignKey(Process,on_delete=models.CASCADE)    
    character_cod = models.ForeignKey(Character,on_delete=models.CASCADE)    
    typerel = models.CharField(max_length=1)

    class Meta:
        verbose_name = 'processcharacter'
        verbose_name_plural = 'processcharacters'

    def __str__(self):
        return self.typerel