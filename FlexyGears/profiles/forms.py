#coding: utf-8
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from userena.forms import (SignupForm, AuthenticationForm, identification_field_factory)
