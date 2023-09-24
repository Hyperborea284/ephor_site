from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.http import JsonResponse

from .forms import BlogPostModelForm
from .models import BlogPost
from nlp import *


@login_required
def blog_post_list_view(request):
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        # qs = BlogPost.objects.filter(user=request.user.id)
        # qs = BlogPost.objects.published()
        qs = (qs | my_qs).distinct()

    template_name = 'blog/list.html'
    context = {'object_list' : qs}
    return render(request, template_name, context)

@login_required
def blog_post_create_view(request):

    if not request.user.is_authenticated:
        return render(request,'not-a-user.html', {})

    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        name = form.cleaned_data['slug']
        Func.idiom(form, name)
        resumo = Func.bert_sumarizar(form)

        ent_list, lang_code, lang_code_short, lang_code_full = Func.entities(form.cleaned_data['content'].replace('\n', ' '))

        output_tri, output_bi, filtered_word_1 = Func.cleaner(form.cleaned_data['content'], lang_code_short)
        
        # Use calcula_ome and analise_prototipica instead of proto
        palavras_ordenadas, ome = Func.calcula_ome(form.cleaned_data['content'])
        alt_freq_bai_ord, bai_freq_alt_ord, alt_freq_alt_ord, bai_freq_bai_ord = Func.analise_prototipica(palavras_ordenadas, ome)

        obj = form.save(commit=False)
        obj.user = request.user  
        obj.summ_bert = resumo
        obj.ent_list = ent_list
        obj.alt_freq_bai_ord = alt_freq_bai_ord
        obj.bai_freq_alt_ord = bai_freq_alt_ord
        obj.alt_freq_alt_ord = alt_freq_alt_ord
        obj.bai_freq_bai_ord = bai_freq_bai_ord
        obj.output_tri = output_tri
        obj.output_bi = output_bi
        obj.wordcloud = f'image/plots/wordclouds/{name}_word_cloud.jpeg'
        obj.barplot = f'image/plots/barplots/{name}_word_freq.jpeg'
        obj.sents_1 = f'image/plots/sents_1/{name}_sents_1.jpeg'
        obj.reinert = f'image/plots/reinerts/{name}_reinert.png'
        obj.save()
        form = BlogPostModelForm()

    template_name = 'form.html'
    context = {'form' : form}
    return render(request, template_name, context)



@login_required
def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'

    context = {'object' : obj}
    return render(request, template_name, context)


@login_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()

    template_name = 'form.html'
    context = {'form' : form, 'title' : f"Update {obj.title}" }
    return render(request, template_name, context)


@login_required
def blog_post_delete_view(request, slug):
    template_name = 'blog/delete.html'
    obj = get_object_or_404(BlogPost, slug=slug)

    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/")
 
    return render(request, template_name)


@login_required
def blog_post_create_view_scheduler(request):

    if not request.user.is_authenticated:
        return render(request,'not-a-user.html', {})
 
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        name = form.cleaned_data['slug']
        Func.idiom(form, name)
        resumo = Func.bert_sumarizar(form)
        ent_list, lang_code, lang_code_short, lang_code_full = Func.entities(form.cleaned_data['content'].replace('\n', ' '))
        output_tri, output_bi, filtered_word_1 = Func.cleaner(form.cleaned_data['content'], lang_code_short)
        alt_freq_bai_ord, bai_freq_alt_ord, alt_freq_alt_ord, bai_freq_bai_ord = Func.proto(filtered_word_1)        

        obj = form.save(commit=False)
        obj.user = request.user  
        obj.summ_bert = resumo
        obj.ent_list = ent_list
        obj.alt_freq_bai_ord = alt_freq_bai_ord
        obj.bai_freq_alt_ord = bai_freq_alt_ord
        obj.alt_freq_alt_ord = alt_freq_alt_ord
        obj.bai_freq_bai_ord = bai_freq_bai_ord
        obj.output_tri = output_tri
        obj.output_bi = output_bi
        obj.wordcloud = f'image/plots/wordclouds/{name}_word_cloud.jpeg'
        obj.barplot = f'image/plots/barplots/{name}_word_freq.jpeg'
        obj.sents_1 = f'image/plots/sents_1/{name}_sents_1.jpeg'
        obj.reinert = f'image/plots/reinerts/{name}_reinert.png'
        obj.save()
        form = BlogPostModelForm()

    template_name = 'form.html'
    context = {'form' : form}
    return render(request, template_name, context)


def salvar_geolocalizacao(request):
    if request.method == 'POST':
        data = request.POST
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Salvando a geolocalização no banco de dados
        user_access_log = UserAccessLog.objects.latest('id')  # Supondo que você quer associar à última entrada do log
        user_access_log.latitude = latitude
        user_access_log.longitude = longitude
        user_access_log.save()

        return JsonResponse({'message': 'Geolocalização salva com sucesso!'})

    return JsonResponse({'message': 'Método inválido.'}, status=400)


