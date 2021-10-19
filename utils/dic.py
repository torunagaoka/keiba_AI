KAISAI = {1: '札幌', 2: '函館', 3: '福島', 4: '新潟', 5: '東京',
          6: '中山', 7: '中京', 8: '京都', 9: '阪神', 10: '小倉'}


def get_kaisai(where):
    """
    開催場所を取得する

    Parameters
    ----------
    where : int
        開催番号

    Returns
    -------
    kaisai_str : str
        開催場所のstr
    """
    kaisai_str = KAISAI.get(where)
    return kaisai_str

