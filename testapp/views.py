from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from testapp.forms import *
from django.contrib import messages
app_name = 'test'
import random

#def showCard(request):
def startTest(request):
    count = Question.objects.all().count()
    l = []
    for i in range(1,count):
        quesid = Question.objects.all()[i].id
        l.append(quesid)
    random.shuffle(l)
    global d
    d = {}
    d['qnos'] = l.copy()
    d['count'] = len(l)
    row1 = []
    for i in range(1,6):
        row1.append(l.pop(0))
    row2 = []
    for i in range(1, 6):
        row2.append(l.pop(0))
    row3 = []
    for i in range(1, 6):
        row3.append(l.pop(0))
    row4 = []
    for i in range(1, 6):
        row4.append(l.pop(0))
    row5 = []
    for i in range(1, 6):
        row5.append(l.pop(0))
    random.shuffle(row1)
    random.shuffle(row2)
    random.shuffle(row3)
    random.shuffle(row4)
    random.shuffle(row5)
    d['tabledata'] = [row1,row2,row3,row4,row5]
    global ques
    ques = []
    return redirect('test:testPaper')


@csrf_exempt
def Bingo(request):
    if request.method == 'POST':
        line = request.POST['line']
        rows = d['tabledata']
        no = request.POST['no']
        q = []
        if line == 'row':
            q = rows[int(no) - 1]
        elif line == 'col':
            for row in rows:
                q.append(row[int(no) - 1])
        else :
            if no == '1':
                i = 0
                for row in rows:
                    q.append(row[i])
                    i = i + 1
            else:
                i = 4
                for row in rows:
                    q.append(row[i])
                    i = i - 1
        for x in q :
            if x not in d['marked']:
                messages.info(request,'Sorry, You did not win')
                return redirect('test:testPaper')
        return render(request,'bingocard/win.html')


def testPaper(request):
    if(d['count']>0):
        random.shuffle(d['qnos'])
        qid = d['qnos'].pop()
        d['count'] = d['count']-1
        question = Question.objects.get(id=qid)
        data = {'ques':question}
        return render(request,'testapp/test-paper.html',data)
    else:
        messages.info(request,'Test Ended')
        return render(request,'testapp/ended.html')


@csrf_exempt
def result(request,pk):
    #data={}
    if request.method=="POST":
        v=request.POST['option']
        q=Question.objects.get(id=pk)
        if v==q.answer:
            ques.append(q.id)
            #d['msg']="Congratulations, Your answer is correct"
            messages.info(request,"Congratulations, Your answer is correct")
        else:
            messages.info(request,"Sorry, Your answer is not correct")
            #d['msg']="Sorry, your answer is not correct"
        d['marked'] = ques
    return render(request,'bingocard/show-card.html',d)
    #return redirect('test:testPaper')





@csrf_exempt
def deleteQuestion(request,pk):
    obj = get_object_or_404(Question, id=pk)
    if request.method == 'POST':
        obj.delete()
        #return redirect('test:viewQuestion')
    else:
        messages.info(request,'Failed to delete')
        #Question.objects.filter(id=pk).delete()
    return redirect('test:viewQuestion')

@csrf_exempt
def updateQuestion(request,pk):
    context = {}
    obj = get_object_or_404(Question,id=pk)
    form = addQuestionform(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Question updated successfully')
        return redirect('test:viewQuestion')
    context['form'] = form
    return render(request,'testapp/update-question.html',context)


def addQuestion(request):
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                messages.success(request,'Question added successfully')
                return redirect('test:addQuestion')
        context={'form':form}
        return render(request,'testapp/add-question.html',context)
    else:
        return redirect('home:home')

def viewQuestion(request):
    #if request.method == 'POST':
    if request.user.is_staff:
        questions = Question.objects.all()
        count = questions.count()
        data={'questions' : questions,'total':count}
        return render(request,'testapp/view-question.html',data)
    else:
        return redirect('home:home')

"""
def testpage(request):
    if request.method == 'POST':
        print(request.POST)
        questions=Question.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'testapp/result.html',context)
    else:
        questions=Question.objects.all()
        context = {
            'questions':questions
        }
        return render(request,'testapp/test-paper.html',context)

    if 'user' not in request.session:
        return redirect('home:index')
        
        """


