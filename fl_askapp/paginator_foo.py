from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(data, count, page):
    paginator = Paginator(data, count)
    try:	
        paginated_data_list = paginator.page(page)
        pagenum = int(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
        pagenum = 1	
    except EmptyPage:
        paginated_data_list = paginator.page(paginator.num_pages)
        pagenum = paginator.num_pages
    if paginator.num_pages == 1:
        paginator.show_paginator = False
    else:
        paginator.show_paginator = True
    if pagenum >= 3:
        paginator.show_prev_prev = True
        paginator.prev_prev = pagenum - 2
    else:
        paginator.show_prev_prev = False
    if pagenum >= 4:
        paginator.show_gap_prev = True
    else: 	
        paginator.show_gap_prev = False

    if (pagenum + 2) <= paginator.num_pages :
        paginator.show_next_next = True
        paginator.next_next = pagenum + 2
    else:
        paginator.show_next_next = False
    if (pagenum + 3) <= paginator.num_pages :
        paginator.show_gap_next = True
    else: 	
        paginator.show_gap_next = False
    return paginated_data_list
