from django.shortcuts import render
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect

class FakeDeleteView(DeleteView):
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        fk_metodo = getattr(obj, "fake_delete", None)

        if callable(fk_metodo):
            obj.fake_delete()
        else:
            raise Exception("model não tem metodo fake_delete")
        
        return HttpResponseRedirect(self.get_success_url())
