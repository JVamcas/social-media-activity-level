from multiprocessing import Manager, Process
from flask import request

from flask import Flask, request

app = Flask(__name__)



@app.route("/")
def social_network_activity():
    # TODO: your code here

    result_dict = {}
    process_list = [
                    Process(target=site_activity, args=("https://takehome.io/twitter","twitter", result_dict)),
                     Process(target=site_activity, args=("https://takehome.io/facebook", "facebook",result_dict)),
                     Process(target=site_activity, args=("https://takehome.io/instagram", "instagram",result_dict))
                ]
    
    [proc.start() for proc in process_list]
    [proc.join() for proc in process_list]

    json_response = {}
    return json_response


def site_activity(url:str,result_key):

    try:
        result = request

    except Exception as ex:
        result["result"] = -1

    return result
