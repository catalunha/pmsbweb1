from django.shortcuts import render

from django.views.generic import (
    DeleteView,
)

from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)

class FakeDeleteView(DeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        fk_metodo = getattr(self.object, "fake_delete", None)

        if callable(fk_metodo):
            self.object.fake_delete()
        else:
            raise Exception("model não tem metodo fake_delete")
        
        return HttpResponseRedirect(self.get_success_url())

class AjaxableFormResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableFormResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableFormResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class FakeDeleteQuerysetViewMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(fake_deletado = False)