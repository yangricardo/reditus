from django import forms

class SearchForm(forms.Form):
    search_field = forms.CharField(
        widget = forms.TextInput(attrs={
            "placeholder" : "2016.001.261711-1",
            "maxLength":"17",
            "pattern" : "[0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4}",
        }),
        label = "Código do Processo",
        )

    class Meta:
        fields = ['search_field',]