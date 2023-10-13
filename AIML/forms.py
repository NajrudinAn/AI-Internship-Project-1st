from django import forms

class MyForm(forms.Form):
    def __init__(self, input_names, maped_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in input_names:
            if field_name not in maped_data:
                self.fields[field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )
            else:
                choices = [(str(k), v) for k, v in maped_data[field_name].items()]
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.Select(attrs={'class': 'form-control'})
            )
