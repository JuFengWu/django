from django.shortcuts import render
from web_tool.request_data import *

def transcript(request, gene_sequence_name):

    context = {
        'gene_sequence_name': gene_sequence_name,
       }
    
    return render(request, 'transcript.html', context)