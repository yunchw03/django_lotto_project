from django.db import models
from django.contrib.auth.models import User

class LottoRound(models.Model):
    """로또 회차 정보 (예: 1120회차)"""
    round_number = models.PositiveIntegerField(unique=True) 
    draw_date = models.DateTimeField()                      
    is_drawn = models.BooleanField(default=False)           
    winning_numbers = models.CharField(max_length=50, blank=True)  
    bonus_number = models.PositiveIntegerField(null=True, blank=True) 

    def __str__(self):
        return f"{self.round_number}회차"

    def save(self, *args, **kwargs):
        if self.is_drawn and self.winning_numbers:
            super().save(*args, **kwargs)             
            
            win_set = set(map(int, [n.strip() for n in self.winning_numbers.split(',') if n.strip()]))
            bonus = self.bonus_number

            
            tickets = Ticket.objects.filter(round=self)
            for ticket in tickets:
                
                user_set = set(map(int, [n.strip() for n in ticket.numbers.split(',') if n.strip()]))
                
                match_count = len(win_set & user_set)
                
                if match_count == 6:
                    ticket.rank = 1
                elif match_count == 5 and (bonus in user_set):
                    ticket.rank = 2
                elif match_count == 5:
                    ticket.rank = 3
                elif match_count == 4:
                    ticket.rank = 4
                elif match_count == 3:
                    ticket.rank = 5
                else:
                    ticket.rank = -1 
                ticket.save()
        else:
            super().save(*args, **kwargs)
            
class Ticket(models.Model):
    """사용자가 구매한 로또 티켓 한 줄"""
    SELECTION_CHOICES = [('AUTO', '자동'), ('MANUAL', '수동')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(LottoRound, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=50)
    is_auto = models.CharField(max_length=10, choices=SELECTION_CHOICES)
    purchase_date = models.DateTimeField(auto_now_add=True)
    rank = models.IntegerField(default=0) # 0:미정, 1~5:등수, -1:낙첨

    def __str__(self):
        status = "미정" if self.rank == 0 else ("낙첨" if self.rank == -1 else f"{self.rank}등")
        return f"{self.user.username}의 {self.round.round_number}회 티켓 ({self.is_auto}) - 결과: {status}"

