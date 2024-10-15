from django.shortcuts import render
from web_tool.request_data import *

def transcript(request, gene_sequence_name):
   
    data = [
        {"name": "A", "value": 30},
        {"name": "B", "value": 80},
        {"name": "C", "value": 45},
        {"name": "D", "value": 60},
        {"name": "E", "value": 20},
        {"name": "F", "value": 90},
        {"name": "G", "value": 50}
    ]
    context = {'data': data,
               "gene_sequence_name" : gene_sequence_name}
    
    return render(request, 'transcript.html', context)