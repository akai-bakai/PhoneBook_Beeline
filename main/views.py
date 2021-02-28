from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from . import forms, models
from django.urls import reverse_lazy

from .models import Person


class HomePageView(ListView):
    model = Person
    template_name = 'main/home.html'
    context_object_name = 'persons'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_by = self.request.GET.get('search_by')   #For search
        query = self.request.GET.get('query')
        search_message = 'All phones'
        if search_by in ['phone', 'name'] and query:
            if search_by == 'name':
                search_message = f"Searching for 'name' by {query}"
                persons = models.Person.objects.filter(name__icontains=query)
            else:
                search_message = f"Searching for 'phones' by {query}"
                persons = models.Person.objects.filter(phones__phone__startswith=query)
            context['persons'] = persons
            return context
        context['search_message'] = search_message
        context['persons'] = models.Person.objects.all()
        return context

class AddPhoneFormView(CreateView):
    model = Person
    template_name = 'main/add_person.html'
    form_class = forms.CreatePersonForm
    success_url = reverse_lazy('home')

    def get_success_url(self) -> str:
        phone_numbers = self.request.POST.get('phones')
        for phone_number in phone_numbers.split('\n'):
            models.Phone.objects.create(phone=phone_number, contact=self.object)
        return super().get_success_url()


class UpdatePhoneFormView(UpdateView):
    model = models.Person
    template_name = 'main/update_person.html'
    form_class = forms.UpdatePersonForm
    success_url = reverse_lazy('home')


class DeletePhoneView(DeleteView):
    model = models.Person
    template_name = 'main/delete_person.html'
    success_url = reverse_lazy('home')


