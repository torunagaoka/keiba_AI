def time_to_sec(time):
    """
    datetime型からfloat型への変換

    Parameters
    ----------
    time : datetime
        datetime型の時間

    Returns
    -------
    second : str
        秒
    """
    second = float(time.minute * 60 + time.second + time.microsecond * 10**(-6))
    return second


def time_avg(time_list):
    """
    timeのリストから平均値を算出をする

    Parameters
    ----------
    time_list : list
        timeが格納されているリスト

    Returns
    -------
    avg : float
        平均値
    """
    if (len(time_list) == 0):
        return 0
    else:
        avg = sum(time_list) / len(time_list)
        return avg


def normalization(text):
    """
    正規化処理
    半角文字と、改行を処理する

    Parameters
    ----------
    text : str
        テキスト

    Returns
    -------
    norm_text : str
        正規化したテキスト
    """
    norm_text = text.replace(' ', '').split('\n')
    return norm_text

