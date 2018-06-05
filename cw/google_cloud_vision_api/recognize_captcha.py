import ast
# from mother import passwords
import base64
import json
from requests import Request, Session
from passpacker import passwords


def recognize_captcha(image_path_list):
    encode_files = [base64.b64encode(
        open(path, 'rb').read()).decode("UTF-8") for path in image_path_list]
    request_list = [
        {'image': {'content': ef}, 'features': [
            {'type': "TEXT_DETECTION", 'maxResults': 100}]}
        for ef in encode_files]
    json_data = json.dumps({'requests': request_list})
    url = "https://vision.googleapis.com/v1/images:annotate?key="
    api_key = passwords['google_cloud_vision_api']
    headers = {'Content-Type': 'application/json'}

    print("Google Cloud Vision Api...", end='')
    obj_session = Session()
    obj_request = Request("POST", url + api_key,
                          data=json_data, headers=headers)
    obj_prepped = obj_session.prepare_request(obj_request)
    obj_response = obj_session.send(obj_prepped, verify=True, timeout=60)
    print("end request")
    try:
        obj_response.raise_for_status()
        dumped = ast.literal_eval(obj_response.text)
        texts = []
        for response in dumped["responses"]:
            try:
                text = response["textAnnotations"][0]['description']
            except (IndexError, ) as e:
                texts.append("IndexError")
            else:
                texts.append(text)
        return texts
    except (Exception, ) as e:
        return obj_response.text
        # return obj_response.text


if __name__ == '__main__':
    text = recognize_captcha(["test.jpg", "test2.png"])
    print(text)
    # recognize_captcha("sosiki_tate.png")
    # load_data()
