import csv
import io
import requests
import json
from elasticsearch import Elasticsearch
#from config.config_handling import get_config_value
from flask import Flask, jsonify, make_response, request, url_for, redirect, render_template
from markupsafe import Markup

app = Flask(__name__)
index = "blog"

def es_connection():
	#connection to elastic search
	es_obj = Elasticsearch(hosts = "http://localhost:9200")
	
	if es_obj.ping():
		print("Successfully connected to ES")
		return es_obj
	else:
		print("Connection to ES unsuccessful")
		return
	
	
def es_ingestion(data):
	#elasticsearch data ingestion
	client = es_connection()

	if client:
		ido = 1
		for obj in data:
			resp = client.index(index=index, id=ido, document=obj)
			ido += 1
			print (resp['result'])
			
		print("Successfully ingested to ES")
		return True
	else:
		print("Ingestion to ES unsuccessful")
		return False
	
	
    



@app.route("/")
def hello_world():
    return render_template('result.html')

    
@app.route('/url_get', methods=['POST'])
def url_get():
    # Base parameters and form input
    url = request.form['URL']
    
    # Make the API request and retrieve the JSON response
    response = requests.get(url)
    response_json = response.json()
    #submit data to elastic search for ingestion.
    status = es_ingestion(response_json)
    
    if status:
    	return render_template('result.html', disabled = 'false')
    
    else:
    	print("Ingestion into es unsuccessful")
    	return render_template('result.html', disabled = 'true') 
    
    
@app.route('/query_results', methods=['POST'])
def query_results():
	# Base parameters and form input
    	query = request.form['Query'].lower()
    	client = es_connection()
    	if not client:
    	    return ('', 204)
		
    	client.indices.refresh(index=index)
	
    	#Making search query to elastic search 
    	resp = client.search(index=index, query={"match_phrase": {"summary":query}}, highlight={"fields": {"*": {}}})
    	matched_results = resp['hits']['total']['value']
    	results = []
	
    	#arranging results
    	print("Got %d Hits:" % resp['hits']['total']['value'])
    	for hit in resp['hits']['hits']:
    		title = Markup(str(hit["_source"]["title"]).lower().replace(query, "<mark>"+query+"</mark>"))
    		tags = Markup(str(hit["_source"]["tags"]).lower().replace(query, "<mark>"+query+"</mark>"))
    		summary = Markup(str(hit["_source"]["summary"]).lower().replace(query, "<mark>"+query+"</mark>"))
    		
    		results.append([title,hit["_source"]["href"],tags,summary])
    		
    	return render_template('result.html',results=results,disabled = 'false')

    

if __name__ == '_main_':
    app.run(debug=True)
