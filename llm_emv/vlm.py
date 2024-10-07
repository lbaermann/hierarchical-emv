import base64
from abc import ABC
from io import BytesIO
from typing import Union, List

from PIL.Image import Image
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


class VLM(ABC):

    @property
    def model(self) -> BaseChatModel:
        raise NotImplementedError

    def prepare_multimodal_message_content(self, *args: Union[str, Image]) -> List[dict]:
        raise NotImplementedError


class OpenAiVision(VLM):

    def __init__(self,
                 model: ChatOpenAI = None):
        super().__init__()
        self._model = model or ChatOpenAI(model='gpt-4o', max_tokens=256)

    @property
    def model(self):
        return self._model

    def prepare_multimodal_message_content(self, *args: Union[str, Image]):
        content = []
        for a in args:
            if isinstance(a, str):
                content.append({"type": "text", "text": a})
            else:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{_encode_image_png_base64(a)}",
                        "detail": "low",
                    },
                })
        return content


def _encode_image_png_base64(image: Image):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')
