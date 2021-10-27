from django.shortcuts import render
from .ranking import *
from .models import Recent
from .relevance_feedback import *
# Create your views here.

# rank = Ranking()
rank = RelevanceFeedback()

def search(request):
    context = {}
    if request.method == 'POST':
        # print(request.body)
        feed = None
        try:
            feed = request.POST.get('feed')
        except:
            pass
        # print('feed',feed)
        query = request.POST.get('query')
        if query is not None:
            # print(query)
            rank.do_ranking(query)
            doc_vals = rank.print_retrieved_docs(print_doc=True)
            Recent.objects.all().delete()
            for x,y in doc_vals:
                temp = Recent(doc_id=x,cosine_score=y)
                temp.save()
            context = {"docs":doc_vals}
            return render(request,'search/results.html',context=context)
        else:
            # print(Recent.objects.all())
            if feed is None:
                doc_vals =[(x.doc_id,x.cosine_score) for x in Recent.objects.all()] 
                context = {"docs":doc_vals}
                return render(request,'search/results.html',context=context)
            else:
                doc_vals = rank.do_relevance_feedback(rel_docs=feed,print_docs=True)
                Recent.objects.all().delete()
                for x,y in doc_vals:
                    temp = Recent(doc_id=x,cosine_score=y)
                    temp.save()
                context = {"docs":doc_vals}
                return render(request,'search/results.html',context=context)
    else:
        context = {}
        return render(request,'search/search.html',context=context)

def feedback(request):
    pass
