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


def str_format(text, digit):
    """
    正規化処理
    半角文字と、改行を処理する

    Parameters
    ----------
    text : str
        テキスト
    digit : str
        フォーマットの形（'01'など）

    Returns
    -------
    form_text : str
        0埋めしたテキストを作成する
    """
    form_text = str(format(text, digit))
    return form_text
