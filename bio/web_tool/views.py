from django.shortcuts import render
from django.http import HttpResponse #匯入http模組
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web_tool.request_data import *
import io
from web_tool.search import search
from web_tool.browse import browse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import urllib, base64

def hello_world(request):
    time = datetime.now()
    return render(request, 'hello_world.html', locals())

def search_show(request):
    return render(request, 'search.html')
def get_data(gene_name):
    # 這裡是假設的數據，可以根據實際情況從資料庫查詢

    """
    data = {
        'wormbase_id': 'WBGene00016885',
        'status': 'Live',
        'gene_sequence_name': 'C52E2.6',
        'gene_name': 'fxbx-97',
        'other_name': 'C52E2.b',
        'wormbase_link': 'https://wormbase.org/species/c_elegans/gene/WBGene00016885'
    }
    """
    data=search(gene_name)
    return data

def search_show(request):
    if request.method == "POST":
        gene_name = request.POST.get('gene')
        data = get_data(gene_name)
        return render(request, 'search.html', {'data': data})
    return render(request, 'search.html')


# 範例資料
EXAMPLE_TABLE_DATA = [
    {"gene_id": "WBGene00045159", "gene_name": "smy-3", "target_rna_name": "D1086.14", "target_rna_type": "snoRNA"},
    {"gene_id": "WBGene00045109", "gene_name": "smy-2", "target_rna_name": "C33A12.21", "target_rna_type": "snoRNA"},
    {"gene_id": "WBGene00007539", "gene_name": "smy-2", "target_rna_name": "B0334.12", "target_rna_type": "snoRNA"},
    {"gene_id": "WBGene00220001", "gene_name": "gene-X", "target_rna_name": "K02F3.15", "target_rna_type": "snoRNA"},
]

@csrf_exempt
def browse_result(request):
    
    if request.method == "POST":
        selected_target_type = request.POST.get("target_type")
        selected_non_coding_rna = request.POST.getlist("non_coding_rna[]")

        # 根據選擇篩選資料（你可以自行實現具體的篩選邏輯）
        #filtered_data = EXAMPLE_TABLE_DATA  # 這裡可根據實際邏輯進行資料過濾
        filtered_data = []
        data = browse(False,selected_non_coding_rna)

        for i in data:
            x = {"gene_id": i['Gene Name'], "gene_name": i['Gen class'], "target_rna_name": i['Sequence Name'], "target_rna_type": i['biotype']}
            filtered_data.append(x)
        context = {
            "table_data": filtered_data,
        }
    
        return render(request, "brows.html", context)
    return render(request, "brows.html")

# HW2 start 

def modify_verticle(color_ranges):
    result = [{'start': item[0], 'end': item[1], 'color': item[2]} for item in color_ranges]
    return result

def draw_colored_ranges(buf,ranges, total_length=10000):
    fig, ax = plt.subplots(figsize=(10, 1))

    last_position = 0  # 用於跟踪繪製的區間起始位置
    # 遍歷範圍列表，繪製不同顏色的區間
    for start, end, color in ranges:
        # 添加之前未填充部分（灰色）
        if last_position < start - 1:
            ax.add_patch(
                patches.Rectangle(
                    (last_position, 0), start - 1 - last_position, 1, 
                    color="lightgrey", edgecolor='blue'
                )
            )
        
        # 添加指定顏色的區域
        ax.add_patch(
            patches.Rectangle(
                (start - 1, 0), end - start + 1, 1, 
                color=color, edgecolor='blue'
            )
        )
        
        last_position = end  # 更新已繪製的區間位置

    # 繪製剩餘部分為灰色
    if last_position < total_length:
        ax.add_patch(
            patches.Rectangle(
                (last_position, 0), total_length - last_position, 1, 
                color="lightgrey", edgecolor='blue'
            )
        )

    # 加入數字標記（顯示範圍的起點、終點）
    ax.text(0, 1.2, f"{1}", ha='center')
    for start, end, color in ranges:
        ax.text(start, 1.2, f"{start}", ha='center')
        ax.text(end, 1.2, f"{end}", ha='center')
    ax.text(total_length, 1.2, f"{total_length}", ha='center')

    # 設置圖像邊界和隱藏軸
    ax.set_xlim(0, total_length)
    ax.set_ylim(0, 1)
    ax.axis('off')

    
    plt.savefig(buf, format='png')
    buf.seek(0)

def gene_sequence_detail(request, gene_sequence_name):
    #get_data_from_web(gene_sequence_name)
    spliced_squence,spliced_features,unspliced_squence,unspliced_features  = get_split_data()
    spliced_table = get_positive_table_data(spliced_features)
    
    spliced_color_ranges = get_positive_sequence_range(spliced_features)
    sequences = split_string_into_tuples(spliced_squence)
    
    unspliced_table = get_positive_table_data(unspliced_features)
    unspliced_color_ranges = get_positive_sequence_range(unspliced_features)
    unsequences = split_string_into_tuples(unspliced_squence)

    
    """
    # Sample data, replace with your method of fetching sequence data
    sequences = (
        "ATGTGAAAAATCTGTTGGTGTAAAACTCTTTAAAATAATGGATATAGACTCTGAAG",
        "CATTTGAGCTAGCTTCAAAGAAATAACCAAAATCAACAGTTCTCGTCGACTATTGGAA",
        # Add all your lines here
    )
    # Define the ranges for coloring with specific colors (1-based index)
    color_ranges = [
        (1, 10, 'orange'),  # Orange for this range
        (50, 58, 'green')   # Green for this range
    ]
    """
    
    # Prepare data with color flags
    highlighted_sequences = []
    
    # Flatten the sequences into one string for easier index handling
    full_sequence = ''.join(sequences)

    # Create a new string where parts within the range are wrapped in HTML <span> tags
    colored_sequence = "1 &#9"
    for i, char in enumerate(full_sequence, 1):  # 1-based index
        # Check which color to apply based on the index
        color = None
        for start, end, color_name in spliced_color_ranges:
            if start <= i <= end:
                color = color_name
                break
        
        # Apply the color if within range
        if color:
            
            colored_sequence += f'<span class="{color}">{char}</span>'
        else:
            colored_sequence += char

        # Add line breaks for every 50 characters (adjust if necessary)
        if i % 50 == 0:
            value = i//50
            colored_sequence += "<br/>" + str(value*50+1) +"&#9"

    # Append the entire colored sequence as a single entry
    highlighted_sequences.append(colored_sequence)


    # Prepare data with color flags
    unsplice_highlighted_sequences = []
        
    # Flatten the sequences into one string for easier index handlin
    unfull_sequence = ''.join(unsequences)
    # Create a new string where parts within the range are wrapped i
    uncolored_sequence = "1 &#9"
    for i, char in enumerate(unfull_sequence, 1):  # 1-based index
        # Check which color to apply based on the index
        color = None
        for start, end, color_name in unspliced_color_ranges:
            if start <= i <= end:
                color = color_name
                break
        
        # Apply the color if within range
        if color:
            uncolored_sequence += f'<span class="{color}">{char}</span>'
        else:
            uncolored_sequence += char
        # Add line breaks for every 50 characters (adjust if necessa
        if i % 50 == 0:
            value = i//50
            uncolored_sequence += "<br/>" + str(value*50+1) +"&#9"
    # Append the entire colored sequence as a single entry
    unsplice_highlighted_sequences.append(uncolored_sequence)

    spliced_buf = io.BytesIO()

    draw_colored_ranges(spliced_buf,spliced_color_ranges, total_length=len(spliced_color_ranges))

    new_spliced_color_ranges = modify_verticle(spliced_color_ranges)
    
    spliced_string = base64.b64encode(spliced_buf.read())
    spliced_matplotlib_image_url = urllib.parse.quote(spliced_string)
    #print(new_spliced_color_ranges)

    #fake_test = [{'start': 1, 'end': 174, 'color': 'orange'}, {'start': 175, 'end': 434, 'color': 'yellow'}, {'start': 435, 'end': 700, 'color': 'orange'}, {'start': 701, 'end': 1132, 'color': 'yellow'}, {'start': 1133, 'end': 1806, 'color': 'orange'}]
    #new_spliced_color_ranges = fake_test

    unspliced_buf = io.BytesIO()
    draw_colored_ranges(unspliced_buf,unspliced_color_ranges, total_length=len(unspliced_color_ranges))
    
    new_unspliced_color_ranges = modify_verticle(unspliced_color_ranges)


    spliced_string = base64.b64encode(unspliced_buf.read())
    unspliced_matplotlib_image_url = urllib.parse.quote(spliced_string)

    #positiveData = [{"Exon" : "b","Start":"d","End":'f',"Length":'h'},
    #                {"Exon" : "a","Start":"d","End":'f',"Length":'g'}]
    splicedData = spliced_table
    unsplicedData = unspliced_table

    context = {
        'gene_sequence_name': gene_sequence_name,
        'spliced_sequences': highlighted_sequences,
        'spliced_matplotlib_image_url': 
        'data:image/png;base64,' + spliced_matplotlib_image_url,
        "splicedData" : splicedData,
        'unspliced_sequences': unsplice_highlighted_sequences,
        'unspliced_matplotlib_image_url': 
        'data:image/png;base64,' + unspliced_matplotlib_image_url,
        "unsplicedData" : unsplicedData,
        "new_spliced_color_ranges" : new_spliced_color_ranges,
        "new_unspliced_color_ranges" : new_unspliced_color_ranges}
    
    return render(request, 'gene_sequence_detail.html', context)