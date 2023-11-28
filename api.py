from flask import Flask, request, jsonify
import requests
# from flask_marshmallow import Marshmallow
# from marshmallow import fields, exceptions
# from marshmallow.validate import Length, Range, Regexp, OneOf
from enum import Enum

from os import listdir
import json

app = Flask(__name__)
endpoints = [x.split('.')[0] for x in listdir("./endpoints")]



@app.route('/api/<endpoint>', methods=['POST'])
def api_gateway(endpoint):
	# request.get_data()
	# check if endpoint exists
	if endpoint not in endpoints:
		return jsonify({"error": "endpoint not found"}), 404
	requestJson = request.get_json(force=True)
	endpointDetails = json.load(open("./endpoints/"+endpoint+".json", "r", encoding="utf-8-sig"))

	headers = endpointDetails["headers"]
	body = endpointDetails["body"]
	params = endpointDetails["params"]
	codes = endpointDetails["response"]

	headers["Authorization"] = request.headers.get('Authorization')

	# add params to body if possible
	for key in params:
		if params[key] in requestJson:
			value = body
			steps = key.split(".")
			for step in steps[0:-1]:
				value = value[step]
			print(requestJson[params[key]])
			print(value[steps[-1]])
			value[steps[-1]] = requestJson[params[key]]
	response = requests.post(endpointDetails["url"], headers=headers, json=endpointDetails["body"])

	# check if response code is valid
	return handleResponse(response, codes)

def handleResponse(response, codes):
	if str(response.status_code) not in codes:
		if "default" in codes:
			return jsonify(without_keys(codes["default"],['HTTP_Code'])), codes["default"]["HTTP_Code"]
		return jsonify({"description": "error not described or unexpected"}), 500
	if "conditional" in codes[str(response.status_code)]:
		if response.json()["Rows"]["HTTP_Code"] in codes[codes["conditional"]]:
			return handleResponse(response, codes[codes["conditional"]])
	if codes[str(response.status_code)]["success"]:
		return jsonify(response.json()), codes[str(response.status_code)]["HTTP_Code"]
	return without_keys(codes[str(response.status_code)],['HTTP_Code']), codes[str(response.status_code)]["HTTP_Code"]
def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8485, threaded=True)
