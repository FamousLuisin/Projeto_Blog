from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView

PER_PAGE = 3

class PostListView(ListView):
    # model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    # ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - ',
        })
        return context
    
class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = user_full_name + ' - Post - '

        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get(self, request, *args, **kwargs):
        
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404
        
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs
    

class CategoryListView(PostListView):  
    allow_empty = False
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(category__slug=self.kwargs.get('slug'))
        return qs
    
    def get_context_data(self, **kwargs):
        gtx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - '
        gtx.update({
            'page_title': page_title,
        })
        return gtx
    

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(tags__slug=self.kwargs.get('slug'))
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        name_tag = self.object_list[0].tags.filter(slug=self.kwargs.get('slug')).first().name
        page_title = name_tag + ' - tag -'
        ctx.update({
            'page_title': page_title,
        })
        return ctx
    
class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset().filter(
        Q (title__icontains=self._search_value) |
        Q (excerpt__icontains=self._search_value) |
        Q (content__icontains=self._search_value) 
    )[:PER_PAGE]
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'Search - {self._search_value[:20]} -  '
        
        ctx.update({
            'page_title': page_title,
            'search_value': self._search_value
        })
        return ctx
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

def page(request, slug):
    page_obj = Page.objects.filter(is_publishe=True).filter(slug=slug).first()
    
    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Page - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )

def post(request, slug):
    post_obj = Post.objects.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )

# =============================== Function =============================== #

# def index(request):
#     posts = Post.objects.get_published()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )


# def created_by(request, author_pk):
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     user = User.objects.filter(pk=author_pk).first()

#     if user is None:
#         raise Http404()
    
#     user_full_name = user.username

#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'

#     page_title = user_full_name + ' post - '
    

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


# def category(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].category.name} - Categoria - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()
    
#     tag_name = page_obj[0].tags.filter(slug=slug).first().name

#     page_title = f'{tag_name} - Tag - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


# def search(request):
#     search_value = request.GET.get('search', '').strip()
    
#     posts = Post.objects.get_published().filter(
#         Q (title__icontains=search_value) |
#         Q (excerpt__icontains=search_value) |
#         Q (content__icontains=search_value) 
#     )[:PER_PAGE]

#     page_title = f'Search - {search_value[:10]} -  '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#             'page_title': page_title,
#         }
#     )