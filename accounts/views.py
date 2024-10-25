from .models import User
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    
    def form_valid(self, form):
        user = form.save()
        send_welcome_email(user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('login')
    
    
class LoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    

class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
    
class ProfileEditView(UpdateView):
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_object(self):
        return self.request.user
    

class ProfileDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('home')
    
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return super().delete(request, *args, **kwargs)


def send_welcome_email(user: User):
    subject = 'Добро пожаловать в MahiruStore!'
    message = '''
    Спасибо, что присоединились к MahiruStore! Мы рады приветствовать вас в нашем сообществе.

    Вы теперь можете наслаждаться всеми преимуществами нашего магазина, включая:
    - Просмотр и покупку самых популярных товаров в различных категориях.
    - Легкость поиска нужных товаров благодаря удобной навигации по каталогу.
    - Получение эксклюзивных предложений и акций только для зарегистрированных пользователей.

    Чтобы начать, вы можете посетить наш каталог товаров по следующей ссылке:
    https://localhost:8000/catalogs

    Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться к нашей службе поддержки:
    - Email: support@mahirustore.com
    - Телефон: +7(123)456-78-90

    С уважением,
    Команда MahiruStore
    '''
    
    # Email settings from settings.py should be configured
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # from email
        [user.email],                 # recipient list
    )
    
