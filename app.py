from multiprocessing import Manager, Process
from multiprocessing.managers import DictProxy
import requests
import json

from flask import Flask

app = Flask(__name__)



@app.route("/")
def social_network_activity():

    result_dict = Manager().dict()
    process_list = [
                    Process(target=site_activity, args=("https://takehome.io/twitter","twitter", result_dict)),
                     Process(target=site_activity, args=("https://takehome.io/facebook", "facebook",result_dict)),
                     Process(target=site_activity, args=("https://takehome.io/instagram", "instagram",result_dict))
                ]
    
    [proc.start() for proc in process_list]
    [proc.join() for proc in process_list]

    return result_dict.copy()


def site_activity(url:str,result_key:str,result_dict:DictProxy):
    """Count the number of posts made on the site and return as activity level

    Args:
        url (str): site url
        result_key (str): key to identify results for this site
        result_dict (DictProxy): dict to store concurrent result

    Returns:
        DictProxy: Results for all the sites whose url were called concurrently to this function
    """
    try:
        resp =  requests.get(url=url)
        if resp.status_code == 200:
            result_dict[result_key] = len(json.loads(resp.content.decode("utf-8")))
        else:
            result_dict[result_key] = -1

    except Exception as ex:
        result_dict[result_key] = -1

    return result_dict


if __name__ == "__main__":
    app.run(debug=True)



