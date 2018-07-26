from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView
)

from .forms import MessageReplyForm, NewMessageForm, NewMessageFormMultiple
from .models import Thread, UserThread

try:
    from account.decorators import login_required
except:  # noqa
    from django.contrib.auth.decorators import login_required


class InboxView(TemplateView):
    """
    View inbox thread list.
    """
    template_name = "pinax/messages/inbox.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InboxView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)
    
        threads = Thread.ordered(Thread.inbox(self.request.user))
        
        # threads_unread = Thread.ordered(Thread.unread(self.request.user))
        
        completed_threads = Thread.ordered(Thread.deleted(self.request.user))
        
        allthreads = threads
       

        context.update({
            "threads": allthreads,
            "completed_threads": completed_threads,
        })
        return context


class ThreadView(UpdateView):
    """
    View a single Thread or POST a reply.
    """
    model = Thread
    form_class = MessageReplyForm
    context_object_name = "thread"
    template_name = "pinax/messages/thread_detail.html"
    #success_url = reverse_lazy("pinax_messages:inbox")

    @method_decorator(login_required)
    def dispatch(self, request,*args, **kwargs):
        context = super(ThreadView, self).dispatch(request, *args, **kwargs)
        return context
    
    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)

        context.update({
            "user_thread": UserThread.objects.get(thread=self.object.pk, user=self.request.user).deleted,
        })
        return context

    def get_queryset(self):
        qs = super(ThreadView, self).get_queryset()
        qs = qs.filter(userthread__user=self.request.user).distinct()
        return qs

    def get_form_kwargs(self):
        kwargs = super(ThreadView, self).get_form_kwargs()
        kwargs.update({ 
            "user": self.request.user,
            "thread": self.object,
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        self.object.userthread_set.filter(user=request.user).update(unread=False)
        return response


class MessageCreateView(CreateView):
    """
    Create a new thread message.
    """
    template_name = "pinax/messages/message_create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageCreateView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        if self.form_class is None:
            if self.kwargs.get("multiple", False):
                return NewMessageFormMultiple
        return NewMessageForm

    def get_initial(self):
        user_id = self.kwargs.get("user_id", None)
        if user_id is not None:
            user_id = [int(user_id)]
        elif "to_user" in self.request.GET and self.request.GET["to_user"].isdigit():
            user_id = map(int, self.request.GET.getlist("to_user"))
        if not self.kwargs.get("multiple", False) and user_id:
            user_id = user_id[0]
        return {"to_user": user_id}

    def get_form_kwargs(self):
        kwargs = super(MessageCreateView, self).get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
        })
        return kwargs


class ThreadDeleteView(DeleteView):
    """
    Delete a thread.
    """
    model = Thread
    success_url = reverse_lazy("pinax_messages:inbox")
    template_name = "pinax/messages/thread_confirm_delete.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        # atualizo a hora da tarefa na hora da conclusão
        self.object.data_finalizada = datetime.datetime.now()
        self.object.save()
        # marco como "deletada" a mensagem nos n end-points possíveis da thread
        self.object.userthread_set.update(deleted=True)
        return HttpResponseRedirect(success_url)
