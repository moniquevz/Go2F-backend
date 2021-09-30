from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Template
from base.templates import templates
from base.serializers import TemplateSerializer

from rest_framework import status

@api_view(['GET'])
def getTemplates(request):
    templates = Template.objects.all()
    serializer = TemplateSerializer(templates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTemplate(request, pk):
    template = Template.objects.get(_id=pk)
    serializer = TemplateSerializer(template, many = False)
    return Response(serializer.data)