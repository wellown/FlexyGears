#coding: utf-8
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from userena.forms import (SignupForm, AuthenticationForm, identification_field_factory)

class SignupFormExtra(SignupForm):
    """ 
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.   

    """
    first_name = forms.CharField(label=_(u'First name'),
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=30,
                                required=False)

    def __init__(self, *args, **kw):
        """
        
        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.
        
        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-2]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        self.fields.keyOrder = new_order

    def save(self):
        """ 
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user

class SigninFormExtra(AuthenticationForm):
    # 自定义userena的登录页面Form。实现登录界面的全中文化
    identification = forms.CharField(label = "邮件地址或用户名",
                                    widget=forms.TextInput(attrs={'class': 'required','placeholder':'请输入用户名或邮件地址'}),
                                    max_length=75)
    password = forms.CharField(label="密码",
                                widget=forms.PasswordInput(attrs={'class': 'required','placeholder':'请输入密码'}, 
                                render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),
                                     required=False,
                                     label=_(u'保存登录信息'))

    #def __init__(self, *args, **kwargs):
    #    """ A custom init because we need to change the label if no usernames is used """
        # super(AuthenticationForm, self).__init__(*args, **kwargs)
        # if userena_settings.USERENA_WITHOUT_USERNAMES:
        #    self.fields['identification'] = identification_field_factory(_(u"Email"),
    #                                                                     _(u"Please supply your email."))

    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            user = authenticate(identification=identification, password=password)
            if user is None:
                raise forms.ValidationError(_(u"请输入正确的用户名（或邮件地址）和密码"))
        return self.cleaned_data
