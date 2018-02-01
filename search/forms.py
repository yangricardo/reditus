from django import forms

class SearchForm(forms.Form):
    search_field = forms.CharField(
        widget = forms.TextInput(attrs={
            "placeholder" : "2016.001.261711-1",
            "maxLength":"17",
            "pattern" : "[0-9]{4}\.[0-9]{3}\.[0-9]{6}-[0-9]",
        }),
        label = "",
        )

    class Meta:
        fields = ['search_field',]