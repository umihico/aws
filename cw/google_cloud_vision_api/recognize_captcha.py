import ast
# from mother import passwords
import base64
import json
from requests import Request, Session
from GitHub.passpacker import passwords


def recognize_captcha(str_image_path):
    bin_captcha = open(str_image_path, 'rb').read()
    str_encode_file = base64.b64encode(bin_captcha).decode("UTF-8")

    str_url = "https://vision.googleapis.com/v1/images:annotate?key="
    # str_api_key = passwords['google_cloud_vision_api']
    str_api_key = passwords['google_cloud_vision_api']
    str_headers = {'Content-Type': 'application/json'}
    str_json_data = {
        'requests': [
            {
                'image': {
                    'content': str_encode_file
                },
                'features': [
                    {
                        'type': "TEXT_DETECTION",
                        'maxResults': 10
                    }
                ]
            }
        ]
    }

    print("Google Cloud Vision Api...", end='')
    obj_session = Session()
    obj_request = Request("POST",
                          str_url + str_api_key,
                          data=json.dumps(str_json_data),
                          headers=str_headers
                          )
    obj_prepped = obj_session.prepare_request(obj_request)
    obj_response = obj_session.send(obj_prepped,
                                    verify=True,
                                    timeout=60
                                    )
    print("end request")

    if obj_response.status_code == 200:
        # print(obj_response.text)
        # with open('data.json', 'w') as outfile:
        #     json.dump(obj_response.text, outfile)
        try:
            text = ast.literal_eval(obj_response.text)[
                "responses"][0]["textAnnotations"][0]['description']
        except (Exception, ) as e:
            print(obj_response.text)
            return 'error'
        return text
        # return obj_response.text
    else:
        print(obj_response.status_code)
        print(obj_response)
        print(obj_response.text)
        return "error"


if __name__ == '__main__':
    textb = recognize_captcha("test.jpg")
    print(text)
    # recognize_captcha("sosiki_tate.png")
    # load_data()
