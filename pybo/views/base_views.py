from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from ..models import Question
from django.db.models import Q

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    answer_page = request.GET.get('answerPage', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    print(page_obj)
    context = {'question_list': page_obj, 'page': page, 'answer_page': answer_page, 'kw': kw}

    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer_page = 1
    
    paginator = Paginator(question.answer_set.all(), 5)
    answer_page_obj = paginator.get_page(answer_page)
    
    context = {'question': question, 'answer_page': answer_page_obj}
    return render(request, 'pybo/question_detail.html', context)
