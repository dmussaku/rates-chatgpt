import json
from typing import Dict

import openai
from django.conf import settings

from .models import ContainerTypes


class OpenAIClient(object):
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def create_context(self):
        container_types = ContainerTypes.choices
        default_container_type = ContainerTypes.TWENTY_FOOTER
        return f"""
        Context:
        We are a global logistics company that transports containers over sea.
        Return me only a json with the following format:
            - is_dangerous: boolean field, false by default. Indicate whether any of the goods are dangerous to be transported.
            - is_hazardous: boolean field, false by default. Indicate whether any of the goods are hazardous.
            - is_customs_needed: boolean field, false by default. Indicate whether any of the goods require customs clearance.
            - pol: Find the closest sea port of leave and return an object of the following format:
                - name: name of the port
                - code: UN/LOCODE of the port
                - country_code: ISO 3166-1 alpha-2 country code
            - pod:  Find the closest sea port of destination and return an object of the following format:
                - name: name of the port
                - code: UN/LOCODE of the port
                - country_code: ISO 3166-1 alpha-2 country code
            - containers: list of objects of the following format:
                - amount: integer Amount of containers, 1 by default
                - type: string enumerated from the following values: {container_types}. {default_container_type} by default
                - goods_names: Array of strings. names of the goods. [] by default

            Don't add any other fields at the end.
        """

    def get_answer(self, question) -> Dict:
        context = self.create_context()
        prompt = f"Question: {question}\nContext: {context}"
        print(prompt)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print("-" * 80)
        print(response)
        print("-" * 80)
        text = response.choices[0]["text"].replace("\n", "")
        if text.startswith("Answer:"):
            text = text.strip("Answer:")

        return json.loads(text.strip())
