from django.shortcuts import render
from web_tool.request_data import *
from web_tool.hw_34_transcript import get_exon_and_other,get_filtered_data

def transcript(request, gene_sequence_name):

    print(gene_sequence_name)
   
    data = [
        {"position": 100, "value": 5},
        {"position": 200, "value": 10},
        {"position": 300, "value": 35},
        {"position": 400, "value": 15},
        {"position": 500, "value": 10},
        {"position": 600, "value": 30},
        {"position": 700, "value": 20},
        {"position": 800, "value": 25},
        {"position": 900, "value": 18},
        {"position": 1000, "value": 40},
        {"position": 1100, "value": 12},
        {"position": 1200, "value": 8},
        {"position": 1300, "value": 15},
        {"position": 1400, "value": 20},
        {"position": 1500, "value": 35},
        {"position": 1600, "value": 40},
        {"position": 1700, "value": 10},
        {"position": 1800, "value": 30},
        {"position": 1900, "value": 25},
        {"position": 2000, "value": 18}
    ]
    data2 = [
        {"type": "UTR", "start": 0, "end": 300, "color": "gray"},
        {"type": "CDS", "start": 300, "end": 1000, "color": "green"},
        {"type": "EXON", "start": 100, "end": 400, "color": "orange"},
        {"type": "EXON", "start": 500, "end": 800, "color": "yellow"}
    ]
    context = {'data': data, 'data2':data2,
               "gene_sequence_name" : gene_sequence_name}
    
    return render(request, 'transcript.html', context)


