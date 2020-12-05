from django import forms
from .models import Job, Employer,Location
from django.core.files.uploadedfile import InMemoryUploadedFile
from .humanize import naturalsize


# Create the form class.
class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    # picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    # upload_field_name = 'picture'

    # Hint: this will need to be changed for use in the jobs application :)
    class Meta:
        model = Job
        fields = ['title', 'employer', 'location', 'salary_l', 'salary_h','description']  # Picture is manual

    # # Validate the size of the picture
    # def clean(self):
    #     cleaned_data = super().clean()
    #     pic = cleaned_data.get('picture')
    #     if pic is None:
    #         return
    #     if len(pic) > self.max_uplojob_limit:
    #         self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # # Convert uploaded File object to a picture
    # def save(self, commit=True):
    #     instance = super(CreateForm, self).save(commit=False)

    #     # We only need to adjust picture if it is a freshly uploaded file
    #     f = instance.picture   # Make a copy
    #     if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
    #         bytearr = f.read()
    #         instance.content_type = f.content_type
    #         instance.picture = bytearr  # Overwrite with the actual image data

    #     if commit:
    #         instance.save()

        # return instance


class EmployerForm(forms.ModelForm):
    class Meta:
        model=Employer
        fields=['name','description']
class LocationForm(forms.ModelForm):
    class Meta:
        model=Location
        fields=['name']
# class TitleForm(forms.ModelForm):
#     class Meta:
#         model=Title
#         fields=['name','description']
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
