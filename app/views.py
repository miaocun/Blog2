from django.shortcuts import render,redirect
from django.views.generic import View
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
from operator import and_,or_
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings


# Create your views here.
class IndexView(View):
    def get(self,request, *args,**kwargs):
        post_data = Post.objects.order_by('-id')
        paginator = Paginator(post_data,3)

        page=request.GET.get('page',1)
        post_data = paginator.page(page)



        return render(request, 'app/index.html',{
            'post_data': post_data
        })

class PostDetailView(View):
    def get(self,request, *args,**kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html',{
            'post_data': post_data
        })

class CreatePostView(LoginRequiredMixin, View):
    def get(self,request, *args,**kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {
            'form' : form
        })

    def post(self,request, *args,**kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            category = form.cleaned_data['category']
            category_data=Category.objects.get(name=category)
            post_data.category=category_data
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', post_data.id)
        
        return render(request, 'app/post_form.html',{
            'form' : form})

class PostEditView(LoginRequiredMixin, View):
    def get(self,request, *args,**kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial = {

                'category':post_data.category,
                'title':post_data.title,
                'content':post_data.content,
            }
        )

        return render(request, 'app/post_form.html',{
            'form': form
        })

    def post(self,request, *args,**kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            category = form.cleaned_data['category']
            category_data=Category.objects.get(name=category)
            post_data.category=category_data
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])
        
        return render(request, 'app/post_form.html',{
            'form' : form})

class PostDeleteView(LoginRequiredMixin, View):
    def get(self,request, *args,**kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html',{
            'post_data': post_data})

    def post(self,request, *args,**kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')

class CategoryView(View):
    def get(self,request, *args,**kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        paginator = Paginator(post_data,3)

        page=request.GET.get('page',1)
        post_data = paginator.page(page)



        return render(request, 'app/index.html', {
            'post_data':post_data
        })

class SearchView(View):
    def get(self,request, *args,**kwargs):
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')

 

        if keyword:
            exclusion_list = set([' ','　'])
            query_list = ['']
            for word in keyword.split(' '):
                if not word in exclusion_list:
                    query_list.append(word)
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            post_data = post_data.filter(query)
        
        else:
            keyword=""

        paginator = Paginator(post_data,3)
        page = request.GET.get('page',1)

        try:
            post_data = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            post_data = paginator.page(1)

        return render(request,'app/index.html',{
            'keyword' : keyword,
            'post_data' : post_data
        })

 
class UploadView(View):
    def post(self,request, *args,**kwargs):
        file = request.FILES['image']

        cloudinary.config( 
            cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'], 
            api_key = settings.CLOUDINARY_STORAGE['API_KEY'], 
            api_secret = settings.CLOUDINARY_STORAGE['API_SECRET']
        )
        res = cloudinary.uploader.upload(
            file = file,
            folder = settings.MARKDOWNX_MEDIA_PATH,)
        return JsonResponse({"image_code": f"![]({res['url']})"})