
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Post,Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView)





class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    paginate_by = 2
    model = Post
    context_object_name = 'posts'
    # template_name = 'post_list.html'
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())
   

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'posts'


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_form.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_delete.html'

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/draft_list.html'
    template_name = 'blog/draft_list.html'
    context_object_name = 'posts'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')


#################### Comments Operations #################

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # below code connect the comments to the current post
            comment.post = post
            comment.save()
            return redirect('blog:detail', pk =post.pk)
    else:
        form =CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comments_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk =pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:detail', pk = post_pk)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect('blog:detail', pk=pk)