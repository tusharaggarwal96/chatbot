from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^common/$', views.CommonUrl.as_view()),
    url(r'^chatboturl/?$', views.Chatbot.as_view()),
]
