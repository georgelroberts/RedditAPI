## Testing Reddit's API: Search for number of times a country is mentioned
# G. Roberts 2-4-17 
# Please visit https://www.reddit.com/prefs/apps/ to create an app and find out
# your client_id and client_secret. user.
# Searches only for official capitalised country names (althought I added England and America myself)
# Geograpy is unfortunately incompatible with python 3.X, although if this were working it may be more versatile
# TODO: Put this feature into google maps to visually show how much each county appears

import praw
import matplotlib.pyplot as plt
from operator import itemgetter
import numpy as np
import seaborn 
seaborn.set() 

def main():
	reddit = praw.Reddit(client_id='yourID',
					client_secret='yourSecret',
					user_agent='testscript by /u/yourUserName')
	countryDict=importCountries()

	subName='worldnews'
	numberOfPosts=200

	posts = reddit.subreddit(subName).hot(limit=numberOfPosts)

	for post in posts:
		submission=reddit.submission(id=post.id)
		submission.comments.replace_more(limit=0)
		individualComment=submission.comments.list()
		for comment in individualComment:
			for country in countryDict:
				countryMentions=comment.body.count(country)
				countryDict[country]=countryDict[country]+countryMentions

	# Want to remove unmentioned countries for plotting
	for key in list(countryDict):
		if countryDict[key]==0:
			del countryDict[key]
	
	plotDict(countryDict,15, subName, numberOfPosts)
	
def importCountries():
	"""Imports a text file countaining all countries and their code"""
	rawCountries=open("countries.txt","r")
	rawCountriesList=rawCountries.readlines()
	countryDict={}
	for country in rawCountriesList:
		country=country.strip('\n')
		country=country[3:]
		countryDict[country]=0
	return countryDict

def plotDict(dictToPlot,numberOfCountries,subName, numberOfPosts):
	"""Converts a dictionary to a list and then creates a bar graph"""
	countryList=list(dictToPlot.items())
	countryList=sorted(countryList,key=itemgetter(1), reverse=True)
	if len(countryList)>numberOfCountries:
		countryList=countryList[0:numberOfCountries]
	x=list(zip(*countryList))[0]
	y=list(zip(*countryList))[1]
	x_pos=np.arange(len(x))

	plt.bar(x_pos, y,align='center')
	plt.xticks(x_pos, x, rotation=70, fontsize=14) 
	plt.ylabel('Number of Mentions', fontsize=16)
	plt.xlabel("Country ", fontsize=16)
	plt.title('Country mentions in /r/'+subName+' comments from '+str(numberOfPosts)+' posts')
	plt.margins(0.05, 0.01)
	#plt.axis('tight')
	plt.tight_layout()
	plt.show()

if __name__=="__main__":
	main()