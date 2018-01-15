# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RegistrationCode

class SignupForm(UserCreationForm):
	registration_code = forms.CharField(max_length=20, label=u'가입코드')

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = u'아이디'
		self.fields['password1'].label = u'비밀번호'
		self.fields['password2'].label = u'비밀번호 재확인'
	
	def clean_registration_code(self):
		data = self.cleaned_data['registration_code']
		try:
			code = RegistrationCode.objects.filter(code=data)[0]
			if code.is_used:
				raise forms.ValidationError(u'가입 코드가 이미 사용되었습니다.')
		except IndexError as e:
			raise forms.ValidationError(u'가입 코드가 올바르지 않습니다.')
		return data
