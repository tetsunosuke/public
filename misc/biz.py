# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
#df = pd.read_csv("bizcampus.csv", encoding="shift_jis")
df = pd.read_csv("2018.csv", encoding="cp932")

#sample = df.loc[:,[u"受講日（実施日）",u"ログインID", u"研修名",u"形態",u"受講状況", u"受講者名", u"部署", u"研修ID"]]
sample = df.loc[:,[u"ログインID", u"研修名",u"形態",u"受講状況", u"受講者名", u"部署", u"研修ID"]]

# 形態＝集合研修かつ受講状況＝出席 または 動画のものにしぼる
# 出席以外はキャンセルか予約中なので
d = sample.query("(受講状況 != 'キャンセル' and 形態 == '動画') or (形態 == '集合研修' and 受講状況 == '出席')")
c = d.groupby(["ログインID", "受講者名"]).count()
# 整形のため一度読んで書く
c.to_csv("count.csv")
df = pd.read_csv("count.csv")
# df の参照エラーを防ぐためにコピー
r = df[["ログインID", "受講者名", "研修ID"]].copy()
r["分類"] = "BizCAMPUS"
r.columns = ["ログインID", "受講者名", "件数", "分類"]
# スペース削除とログインIDから会社名の割り出し
r.loc[:,"受講者名"] = r["受講者名"].map(lambda x:x.replace("　", ""))
r.loc[:,"ログインID"] = r["ログインID"].map(lambda x: "PC" if x.find("photocreate") >= 0 else "PLL" if x.find("ccc") >= 0 else "SPS")

result = r[["分類", "ログインID", "受講者名", "件数"]]
result.columns = ["分類", "所属", "受講者名", "件数"]
result.to_csv("2018result.csv", encoding="cp932", index=False)

