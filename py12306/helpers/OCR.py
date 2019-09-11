import math
import random

from py12306.config import Config
from py12306.helpers.request import Request
from py12306.log.common_log import CommonLog
from py12306.vender.ruokuai.main import RKClient


class OCR:
    """
    图片识别
    """
    session = None

    def __init__(self):
        self.session = Request()

    @classmethod
    def get_img_position(cls, img):
        """
        获取图像坐标
        :param img_path:
        :return:
        """
        self = cls()
        if Config().AUTO_CODE_PLATFORM == 'free':
            return self.get_image_by_free_site(img)
        return self.get_img_position_by_ruokuai(img)

    def get_img_position_by_ruokuai(self, img):
        ruokuai_account = Config().AUTO_CODE_ACCOUNT
        soft_id = '119671'
        soft_key = '6839cbaca1f942f58d2760baba5ed987'
        rc = RKClient(ruokuai_account.get('user'), ruokuai_account.get('pwd'), soft_id, soft_key)
        result = rc.rk_create(img, 6113)
        if "Result" in result:
            return self.get_image_position_by_offset(list(result['Result']))
        CommonLog.print_auto_code_fail(result.get("Error", CommonLog.MESSAGE_RESPONSE_EMPTY_ERROR))
        return None

    def get_image_position_by_offset(self, offsets):
        positions = []
        width = 75
        height = 75
        for offset in offsets:
            random_x = random.randint(-5, 5)
            random_y = random.randint(-5, 5)
            offset = int(offset)
            x = width * ((offset - 1) % 4 + 1) - width / 2 + random_x
            y = height * math.ceil(offset / 4) - height / 2 + random_y
            positions.append(int(x))
            positions.append(int(y))
        return positions

    def get_image_by_free_site(self, img):
        from py12306.helpers.ocr.ml_predict import get_coordinate
        import base64

        result = get_coordinate(base64.b64decode(img))
        result = self.get_image_position_by_offset(result)
        # CommonLog.print_auth_code_info("验证码识别的结果为：" + result)

        if result:
            return result

        return None


if __name__ == '__main__':
    pass
    # code_result = AuthCode.get_auth_code()
