from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from project.lib import mail

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


class Ticket(models.Model):
    ''' Model for storing lottery ticket data. '''
    
    class Meta:
        ordering = ['-date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6']
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=False, null=False,
        verbose_name="User", db_index=True)
    
    n1 = models.IntegerField('Feld-1', blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(49)])
    n2 = models.IntegerField('Feld-2', blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(49)])
    n3 = models.IntegerField('Feld-3', blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(49)])
    n4 = models.IntegerField('Feld-4', blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(49)])
    n5 = models.IntegerField('Feld-5', blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(49)])
    n6 = models.IntegerField('Feld-6', blank=False, null=False,
        validators=[MinValueValidator(1), MaxValueValidator(49)])
    win = models.IntegerField('Win', blank=True, default=0)
    checked = models.BooleanField('Checked', blank=True, default=False)
    date = models.DateField()
    
    
    def check_numbers(self, win_numbers):
        ''' Checks if this ticket has the same numbers as in the win_numbers
            list. If it does then it will send email to the user. It will also
            update itself for checked and win attributes.
            
            Note: all number should be integers, no strings allowed.
        '''
        self.checked = True
        self.win = 0
        win_count = 0
        for i in range(6):
            # getting n1, n2, etc. attribute of self
            n = getattr(self, 'n%d' % (i+1)) 
            if n in win_numbers:
                win_count += 1
        
        if win_count < 3:
            self.save()
            return False
        
        self.win = win_count
        self.save()
        
        if self.user.email:
            try:
                mail.send(self.user.email, 'Lottogewinn!',
                    'Ihr Lottoschein #%d (Ziehung: %s) hat gewonnen!' % \
                            (self.id, self.date))
            except:
                pass
        
        return True
    
    
    def is_outdated(self):
        return self.date < datetime.now().date()
    
    def is_today(self):
        return self.date == datetime.now().date()
    
    def __str__(self):
        return 'Lottoschein #%06d (date: %s)' % (self.id, str(self.date))
    
        
    
