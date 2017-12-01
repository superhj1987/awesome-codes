#!/usr/bin/env python
#coding:utf-8
# 使用神经网络根据历史比赛数据预测未来比赛结果

import redis
import common
import sys
import pandas as pd
import ast
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense
from keras.models import load_model

cli = redis.Redis()

GAME_URL = "002{year}{gameNo:0>5d}_gamedetail.json";
DATA_URL = "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/20{year}/scores/gamedetail/";


years = range(15,18)
gameCount = 1230

global models
global gameDetailDf

def getAndSaveData():
	for year in years:
	    for no in range(1,gameCount + 1):
	    	gameUrl = GAME_URL.format(year=year,gameNo=no)
	        url = DATA_URL.format(year=year) + gameUrl
	        
	        try:
	        	text = common.get_url_content(url)
	        except:
	        	continue

	        data = common.parse_json_str(text)

	        stt = data["g"]["stt"]
	        # 比赛是否结束
	        if not stt.endswith("Final"):
	        	print '%s game is not finished' % key
	        	continue
	        vls = data["g"]["vls"]
	        hls = data["g"]["hls"]

	        vs = int(vls['s'])
	        hs = int(hls['s'])
	        # 主队是赢还是输
	        w = 1.0 if hs > vs else 0.0

	        di = {}
	        di.update({"win":w})

	        # 比赛数据diff
	        vsts = vls['tstsg']
	        hsts = hls['tstsg']
	        for k in hsts:
	        	di.update({k : int(hsts[k]) - int(vsts[k])})

	        # 队伍名称
	        vn = vls["ta"]
	        hn = hls["ta"]
	        di.update({"home":hn,"away":vn})
	        # 比赛日期
	        date = data["g"]["gdtutc"]
	        di.update({"date":date})

	        key = gameUrl
	        cli.hset("gamedetaildiff", key, str(di))
	        print "%s save successfully." % key
	        cli.hset("gamedetail", key, text)

def preAndTrainData():
	data = cli.hgetall("gamedetaildiff")
	df = pd.DataFrame([ast.literal_eval(data[k]) for k in data])
	df = df.fillna(value=0.0)

	dataX = df.drop(["win","date","home","away"],axis=1)
	dataY = df["win"]

	trainX = np.array(dataX)[::2] # training set
	trainY = np.array(dataY)[::2]

	# testX = np.array(dataX)[1::2] # test set
	# testY = np.array(dataY)[1::2]

	models = Sequential()
	models.add(Dense(60, input_dim=trainX.shape[1], activation='relu'))
	models.add(Dense(30, activation='relu'))
	models.add(Dense(1, activation='sigmoid'))
	models.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	models.fit(trainX,trainY,batch_size=6,epochs=10)

	return models
	# model.evaluate(testX,testY,batch_size=2)

def predict(home=None, away=None):

	homeData = gameDetailDf[(gameDetailDf['name']==home) & (gameDetailDf['home']==1)].sort_values(by='date', ascending=False)[:5].mean()
	awayData = gameDetailDf[(gameDetailDf['name']==away) & (gameDetailDf['home']==0)].sort_values(by='date', ascending=False)[:5].mean()
	homeData = homeData.drop(['home'])
	awayData = awayData.drop(['home'])
	newX= np.array(homeData - awayData)
	return models.predict_classes(newX[np.newaxis,:], verbose=0)[0][0]


if __name__ == '__main__': 

	gameDetailData = cli.hgetall("gamedetail")
	gameDetailJson = []
	for k in gameDetailData:
		diV = {}
		diH = {}
		j = common.parse_json_str(gameDetailData[k])
		vls = j['g']['vls']
		hls = j['g']['hls']

		diV.update(vls["tstsg"])
		diV.update({"date": j["g"]["gdtutc"], "name": vls["ta"], "home": 0})
		gameDetailJson.append(diV)

		diH.update(hls["tstsg"])
		diH.update({"date": j["g"]["gdtutc"], "name": hls["ta"], "home": 1})
		gameDetailJson.append(diH)

	gameDetailDf = pd.DataFrame(gameDetailJson)
	gameDetailDf = gameDetailDf.fillna(value=0.0)

	teams = [
		['ATL','CLE'],
		['BOS','PHI'],
		['DEN','CHI']
	]

	models = load_model('nba-model.hdf5')

	for t in teams:
		p = predict(t[0],t[1])
		if p == 1:
			print "%s(win) vs %s(loss)" % (t[0],t[1])
		else:
			print "%s(loss) vs %s(win)" % (t[0],t[1])

