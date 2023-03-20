from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.db.models import F
from email_validator import validate_email, EmailNotValidError

from .models import Post, Entry, ForumUser
from .forms import SignUpForm, LoginForm, ForumUserPasswordChangeForm


class IndexView(generic.ListView):
	template_name = 'main/index.html'
	context_object_name = 'latest_post_list'

	def get_queryset(self):
		return Post.objects.all()[:10]


class AccountView(LoginRequiredMixin, generic.DetailView):
	template_name = 'account.html'
	model = ForumUser
	login_url = '/login/'

	def get_context_data(self, **kwargs):
		person = ForumUser.objects.get(pk=kwargs['object'].id)
		return {'person': person}

def my_logout(request):
	logout(request)
	return redirect('/')


class PostView(LoginRequiredMixin, generic.ListView):
	login_url = '/login/'
	template_name = 'main/post_detail.html'

	def __init__(self):
		super().__init__()
		self.post = None

	def get_queryset(self):
		self.post = get_object_or_404(Post, id=self.kwargs['pk'])
		return Post.objects.filter(id=self.post.id)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_id'] = self.post.id
		context['entries'] = self.post.entries.all()
		return context


class SignUpView(generic.FormView):
	template_name = 'signup.html'
	form_class = SignUpForm
	success_url = '/login/'

	def form_valid(self, form):
		user = form.save(commit=False)
		user.username = user.username.lower()
		user.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return render(self.request, 'signup.html', {'form': form})


class LoginView(generic.FormView):
	template_name = 'login.html'
	form_class = LoginForm
	success_url = '/'

	def form_valid(self, form):
		username = self.request.POST['username']
		password = self.request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(self.request, user)
			return super().form_valid(form)
		else:
			return super().form_invalid(form)

	def form_invalid(self, form):
		return redirect('/login/')


class PasswordChangeView(LoginRequiredMixin, generic.View):
	login_url = '/login/'
	template_name = "change-password.html"
	form_class = ForumUserPasswordChangeForm
	success_url = '/account/'

	def get(self, request):
		form = ForumUserPasswordChangeForm(user=self.request.user)
		return render(self.request, 'change-password.html', {'form': form})

	def post(self, request):
		user = self.request.user
		form = ForumUserPasswordChangeForm(self.request.POST)
		if form.check_old_password(self.request):
			if form.check_new_passwords():
				forum_user = ForumUser.objects.get(username=user.username)
				forum_user.set_password(form.user['new_password1'])
				forum_user.save()
				logout(request)
				return redirect('/login/')
		return render(request, 'change-password.html', {'form': form})


@login_required(login_url='/login/')
@require_http_methods(['POST'])
def post_create(request):
	author = ForumUser.objects.get(username=request.user.username)
	new_post_tag = request.POST['post_tag']
	post = Post(author=author, tag=new_post_tag)
	author.post_count = F('post_count') + 1
	author.save()
	post.save()
	return redirect(f'/{post.id}/')


@login_required(login_url='/login/')
@require_http_methods(['POST'])
def entry_create(request):
	author = ForumUser.objects.get(username=request.user.username)
	post = Post.objects.get(pk=request.POST['post_id'])
	content = request.POST['entry']
	entry = Entry(author=author, post=post, content=content)
	author.entry_count = F('entry_count') + 1
	author.save()
	entry.save()
	return redirect(f"/{post.id}/")

def email_update(request, pk):
	if request.method == 'POST':
		email = request.POST['email']
		try:
			validation = validate_email(email, check_deliverability=False)
			request.user.email = validation.email
			request.user.save()
		except EmailNotValidError as e:
			print(str(e))

		return redirect(f'/account/{request.user.id}')

	return render(request, 'email-update.html')
