from utils.connection import NewAdapter
from utils.rps import Rps
from utils.response import Response
from utils.schemas import schemaCreateRps, schemaCancelRps, schemaConsultNfes
from ssl import wrap_socket, CERT_REQUIRED, PROTOCOL_TLSv1
from requests import Session
from socket import AF_INET, SOCK_STREAM, socket


class SaopauloGateway:

    @classmethod
    def sendRps(cls, privateKeyPath, certificatePath, **kwargs):
        xml = Rps.xmlCreateRps(
            xml=schemaCreateRps,
            privateKeyContent=open(privateKeyPath, "rb").read(),
            certificateContent=open(certificatePath, "rb").read(),
            **kwargs
        )

        return cls.postRequest(
            xml=xml,
            method="rps",
            privateKeyPath=privateKeyPath,
            certificatePath=certificatePath,
        )

    @classmethod
    def cancelRps(cls, privateKeyPath, certificatePath, **kwargs):
        xml = Rps.cancelRps(
            xml=schemaCancelRps,
            privateKeyContent=open(privateKeyPath).read(),
            certificateContent=open(certificatePath).read(),
            **kwargs
        )
        return cls.postRequest(
            xml=xml,
            method="rps",
            privateKeyPath=privateKeyPath,
            certificatePath=certificatePath,
           )

    @classmethod
    def consultNfes(cls, privateKeyPath, certificatePath, **kwargs):
        xml = Rps.consultNfes(
            xml=schemaConsultNfes,
            privateKeyContent=open(privateKeyPath).read(),
            certificateContent=open(certificatePath).read(),
            **kwargs
        )
        return cls.postRequest(
            xml=xml,
            method="consult",
            privateKeyPath=privateKeyPath,
            certificatePath=certificatePath,
        )

    @classmethod
    def postRequest(cls, xml, method, privateKeyPath, certificatePath):

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(20)
        socks = wrap_socket(
            sock=clientSocket,
            keyfile=privateKeyPath,
            certfile=certificatePath,
            cert_reqs=CERT_REQUIRED,
            ssl_version=PROTOCOL_TLSv1,
            ca_certs="../static/cacert.pem",
        )

        session = Session()

        session.mount('http://', NewAdapter(soqt=socks))
        session.mount('https://', NewAdapter(soqt=socks))

        headers = {
            'content-type': 'application/soap+xml; charset=utf-8;',
            'Accept': 'application/soap+xml; charset=utf-8;',
            'Cache-Control': "no-cache",
            'Host': "nfe.prefeitura.sp.gov.br",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
        }

        response = session.post(
            "https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx",
            xml,
            headers=headers,
            verify=True
        )

        status = response.status_code
        if status != 200:
            return "Error"

        if method == "consult":
            return Response.getTail(cls.clearedResponse(response))

        if method == "rps":
            return Response.resultDict(cls.clearedResponse(response))

    @classmethod
    def clearedResponse(cls, response):
        response.encoding = "utf-8"
        xmlResponse = str(response.content)
        xmlResponse = xmlResponse.replace("&lt;", "<")
        xmlResponse = xmlResponse.replace("&gt;", ">")
        return xmlResponse