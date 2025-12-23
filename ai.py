import requests
import time
import base64
from config import API_KEY, API_SECRET


class FusionBrain:
    def __init__(self):
        # ✅ BASE URL FINAL
        self.BASE_URL = "https://api.fusionbrain.ai"

        self.headers = {
            "X-Key": f"Key {API_KEY}",
            "X-Secret": f"Secret {API_SECRET}",
            "Content-Type": "application/json"
        }

        # model paling stabil
        self.model_id = 4

    def generate_image(self, prompt, width=512, height=512):
        # ==============================
        # 1️⃣ START GENERATE
        # ==============================
        payload = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        run_resp = requests.post(
            f"{self.BASE_URL}/api/v1/text2image/run",
            headers=self.headers,
            json={
                "model_id": self.model_id,
                "params": payload
            },
            timeout=30
        )

        print("RUN STATUS:", run_resp.status_code)
        print("RUN RESPONSE:", run_resp.text)

        if run_resp.status_code != 200 or not run_resp.text:
            raise Exception("Gagal start generate")

        request_id = run_resp.json().get("uuid")
        if not request_id:
            raise Exception("UUID tidak ditemukan")

        # ==============================
        # 2️⃣ POLLING STATUS
        # ==============================
        for i in range(30):  # ±60 detik
            time.sleep(2)

            status_resp = requests.get(
                f"{self.BASE_URL}/api/v1/text2image/status/{request_id}",
                headers=self.headers,
                timeout=30
            )

            print(f"STATUS CHECK {i+1}:", status_resp.text)

            if not status_resp.text:
                continue

            data = status_resp.json()

            if data.get("status") == "DONE":
                print("✅ DONE")
                return data["images"][0]

            if data.get("status") == "FAIL":
                raise Exception("Generate FAIL")

        raise TimeoutError("Generate TIMEOUT")

    @staticmethod
    def save_base64_image(base64_string, filename):
        image_bytes = base64.b64decode(base64_string)
        with open(filename, "wb") as f:
            f.write(image_bytes)
