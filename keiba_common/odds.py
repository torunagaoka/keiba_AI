def get_tansho_fukusho(soup, want_result):
    """
    単勝か複勝の払い戻しの情報を取得する

    Parameters
    ----------
    soup : soup
        soup
    want_result : boolen
        true⇨単勝
        false⇨複勝

    Returns
    -------
    header : list
        ヘッダー
    result : list
        結果（馬番）
    payout : list
         払い戻し
    """
    if (want_result):
        header_list = ['単勝']
        tr = soup.find(class_='Tansho')
    if not (want_result):
        header_list = ['複勝']
        tr = soup.find(class_='Fukusho')
    result_div = tr.find(class_='Result')
    # 結果（馬番）を取得する
    result = get_value_from_div_tag(result_div)
    len_result = len(result)
    # 払い戻しを取得する
    payout = tr.find(class_='Payout').text.split('円')
    payout = payout[:len_result]
    # ヘッダー
    header = header_list * len_result
    return header, result, payout


def get_ren_sanren(soup, want_result):
    """
    連系、三連系の結果を取得する

    Parameters
    ----------
    soup : soup
        soup
    want_result : str
        欲しい結果

    Returns
    -------
    header : list
        ヘッダー
    result : list
        結果（馬番）
    payout : list
         払い戻し
    """
    if(want_result == '枠連'):
        header = ['枠連']
        tr = soup.find(class_='Wakuren')
        result_div = tr.find(class_='Result')
        # 結果（馬番）を取得する
        result = get_value_from_ul_tag(result_div, True)
    elif(want_result == '馬連'):
        header = ['馬連']
        tr = soup.find(class_='Umaren')
        result_div = tr.find(class_='Result')
        # 結果（馬番）を取得する
        result = get_value_from_ul_tag(result_div, True)
    elif(want_result == 'ワイド'):
        header = ['ワイド']
        tr = soup.find(class_='Wide')
        result_div = tr.find(class_='Result')
        # 結果（馬番）を取得する
        result = get_value_from_ul_tag(result_div, True)
    elif(want_result == '馬単'):
        header = ['馬単']
        tr = soup.find(class_='Umatan')
        result_div = tr.find(class_='Result')
        # 結果（馬番）を取得する
        result = get_value_from_ul_tag(result_div, True)
    elif(want_result == '三連複'):
        header = ['三連複']
        tr = soup.find(class_='Fuku3')
        result_div = tr.find(class_='Result')
        # 結果（馬番）を取得する
        result = get_value_from_ul_tag(result_div, False)
    elif(want_result == '三連単'):
        header = ['三連単']
        tr = soup.find(class_='Tan3')
        result_div = tr.find(class_='Result')
        # 結果（馬番）を取得する
        result = get_value_from_ul_tag(result_div, False)
    len_result = len(result)
    # 払い戻しを取得する
    payout = tr.find(class_='Payout').text.split('円')
    payout = payout[:len_result]
    # ヘッダー
    header = header * len_result
    return header, result, payout


def get_value_from_div_tag(div):
    """
    値をdivタグから取得する

    Parameters
    ----------
    div : div
        div

    Returns
    -------
    value_list : list
        値を入れたリスト
    """
    search_div = div.find_all('div')
    value_list = []
    for i in range(len(search_div)):
        if(i % 3 == 0):
            value_list.append(search_div[i].text)
    return value_list


def get_value_from_ul_tag(div, interconnection):
    """
    値をulタグから取得する

    Parameters
    ----------
    div : div
        div

    Returns
    -------
    value_list : list
        値を入れたリスト
    """
    search_div = div.find_all('ul')
    value_list = []
    for i in range(0, len(search_div)):
        value_work = search_div[i].text.split('\n')
        if (interconnection):
            first = value_work[1]
            second = value_work[2]
            value_list.append(first + '-' + second)
        if not (interconnection):
            first = value_work[1]
            second = value_work[2]
            third = value_work[3]
            value_list.append(first + '-' + second + '-' + third)
    return value_list



