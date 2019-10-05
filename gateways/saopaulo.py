from utils.rps import Rps
from utils.schemaCreateRps import schemaCreateRps


class SaopauloGateway:

    @classmethod
    def sendRps(cls, privateKeyContent, certificateContent, **kwargs):
        xml = Rps.xmlCreateRps(
            xml=schemaCreateRps,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **kwargs
        )

        print(xml)

        #TODO Send request
