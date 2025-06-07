from django.views.generic import DetailView, ListView, DeleteView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


    def get_queryset(self):
        return Post.objects.filter(is_active=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview_image']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'preview_image']
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('blog:post_list')

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs.get('pk')])


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
