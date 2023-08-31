from abc import abstractmethod

class WhatsAppClientInterface:
    @abstractmethod
    def fetch_products(self):
        pass

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def send_image_base64(self):
        pass