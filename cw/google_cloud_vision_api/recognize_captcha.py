import ast
# from mother import passwords
import base64
import json
from requests import post
from passpacker import passwords


def recognize_captcha(image_path_list):
    images = []
    for path in image_path_list:
        if path.startswith("http"):
            image = {"source": {'imageUri': path}}
        else:
            image = {'content': base64.b64encode(
                open(path, 'rb').read()).decode("UTF-8")}
        images.append(image)
    request_list = [
        {'image': image, 'features': [
            {'type': "TEXT_DETECTION", 'maxResults': 100}]}
        for image in images]
    # request_list = [
    #     {'image': {'content': ef}, 'features': [
    #         {'type': "TEXT_DETECTION", 'maxResults': 100}]}
    # for ef in encode_files]
    json_data = json.dumps({'requests': request_list})
    url = "https://vision.googleapis.com/v1/images:annotate?key="
    api_key = passwords['google_cloud_vision_api']
    headers = {'Content-Type': 'application/json'}

    print("Google Cloud Vision Api...", end='')
    obj_response = post(url + api_key, data=json_data, json=headers)
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
    text = recognize_captcha(
        ["test.jpg", "test2.png", "http://www.tokai-com.co.jp/company/images/soshikizu_img01.gif", "large.jpg"])
    print(text)
    # recognize_captcha("sosiki_tate.png")
    # load_data()
