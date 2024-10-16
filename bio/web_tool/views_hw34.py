from django.shortcuts import render
from web_tool.request_data import *
from web_tool.hw_34_transcript import get_exon_and_other,get_filtered_data,expand_position_value

def transcript(request, gene_sequence_name):

    print(gene_sequence_name)
    bedgraph = './web_tool/data/SRR20334757_m0_bedgraph.csv'
    result = get_filtered_data(bedgraph,gene_sequence_name)
    barData = expand_position_value(result)

    #print(barData)
   
    #barData = [
    #     {'position': 1666, 'value': 1.0}, {'position': 1667, 'value': 1.0}
    #]
    data = [
        
        {'start': 200, 'end': 308, 'read_count': 108, 'values': 16.0},
        {'start': 400, 'end': 450, 'read_count': 50, 'values': 8.0},
        {'start': 1630, 'end': 1638, 'read_count': 32,  'values': 1.0},
        # 可以加入更多數據對
    ]

    barHorizontal = [
        {"type": "UTR", "start": 0, "end": 300, "color": "gray"},
        {"type": "CDS", "start": 300, "end": 1000, "color": "green"},
        {"type": "EXON", "start": 100, "end": 400, "color": "orange"},
        {"type": "EXON", "start": 500, "end": 800, "color": "yellow"}
    ]
    context = {'barData': barData, 'barHorizontal':barHorizontal ,
               "gene_sequence_name" : gene_sequence_name,'data':data}
    
    return render(request, 'transcript.html', context)


