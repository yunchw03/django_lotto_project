import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import LottoRound, Ticket

def buy_page(request):
    """로또 구매 메인 페이지 + 내 구매 내역 조회"""
    current_round = LottoRound.objects.filter(is_drawn=False).first()
    
    user = User.objects.first()
    tickets = Ticket.objects.filter(user=user).order_by('-purchase_date')
    
    return render(request, 'lotto/buy.html', {
        'round': current_round,
        'tickets': tickets # HTML 파일로 티켓 목록을 넘겨줍니다.
    })

def buy_auto(request, round_id):
    """자동 번호 구매 로직"""
    if request.method == 'POST':
        lotto_round = get_object_or_404(LottoRound, id=round_id)
        
        numbers_list = sorted(random.sample(range(1, 46), 6))
        numbers_str = ",".join(map(str, numbers_list))
        
        user = User.objects.first()
        
        Ticket.objects.create(
            user=user,
            round=lotto_round,
            numbers=numbers_str,
            is_auto='AUTO'
        )
        return redirect('buy_page')

def buy_manual(request, round_id):
    """수동 번호 구매 로직"""
    if request.method == 'POST':
        lotto_round = get_object_or_404(LottoRound, id=round_id)
        raw_numbers = request.POST.get('manual_numbers', '')
        
        try:
            parsed_numbers = sorted([int(n.strip()) for n in raw_numbers.split(',') if n.strip()])
            
            if len(parsed_numbers) != 6 or len(set(parsed_numbers)) != 6 or any(n < 1 or n > 45 for n in parsed_numbers):
                raise ValueError("올바르지 않은 번호 구성입니다.")
            
            numbers_str = ",".join(map(str, parsed_numbers))
            user = User.objects.first()
            
            Ticket.objects.create(
                user=user,
                round=lotto_round,
                numbers=numbers_str,
                is_auto='MANUAL'
            )
        except ValueError:
            pass
            
        return redirect('buy_page')