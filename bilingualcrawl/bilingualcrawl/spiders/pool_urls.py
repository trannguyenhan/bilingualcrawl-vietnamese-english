def create_pool_urls(configs, prefix_next_page):
    urls = []
    for base_url in configs: 
        url = base_url['url']
        number_pages = base_url['number_pages']
        for page in range(0, number_pages): 
            tmp_url = url + prefix_next_page + "/" + str(page + 1)
            if page + 1 == 1: 
                tmp_url = url
            urls.append(tmp_url)

    return urls
