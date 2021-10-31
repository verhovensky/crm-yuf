def check_out_of_stock(ql, pl, res=None, plindex=0):
    if res is None:
        res = {}
    for i in ql:
        if i <= pl[plindex].stock:
            res.update({pl[plindex].name: 'ok'})
            plindex += 1
        else:
            res.update({pl[plindex].name: 'out'})
            plindex += 1
    return res
