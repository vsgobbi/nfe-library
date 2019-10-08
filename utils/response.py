from lxml import etree


class Response:

    @classmethod
    def responseDissector(cls, xmlResponse):
        xmlResponse = xmlResponse.replace("&lt;", "<")
        xmlResponse = xmlResponse.replace("&gt;", ">")
        print(xmlResponse)
        if "ConsultaNFeEmitidasResponse xmlns=" in xmlResponse and "<Sucesso>true</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("</Cabecalho>")
            strResult = splitResult[1].split("</Retorno")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._getTail(strResult)
        if "ConsultaNFeRecebidasResponse xmlns=" in xmlResponse and "<Sucesso>true</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("</Cabecalho>")
            strResult = splitResult[1].split("</Retorno")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._getTail(strResult)
        if "ConsultaCNPJResponse xmlns=" in xmlResponse and "<Sucesso>true</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("</Cabecalho>")
            strResult = splitResult[1].split("</Retorno")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._resultDict(strResult)
        if "EnvioRPSResponse xmlns=" in xmlResponse and "<Sucesso>true</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("""<Alerta xmlns="">""")
            strResult = splitResult[1].split("</Alerta>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._resultDict(strResult)
        if "EnvioRPSResponse xmlns=" in xmlResponse and "<Sucesso>false</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("</Cabecalho>")
            strResult = splitResult[1].split("</RetornoEnvioRPS>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._resultDict(strResult)
        if "CancelamentoNFeResponse xmlns=" in xmlResponse and "<Sucesso>true</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("</Cabecalho>")
            strResult = splitResult[1].split("</RetornoCancelamentoNFe>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._resultDict(strResult)
        if "ConsultaNFeResponse xmlns=" in xmlResponse and "<Sucesso>true</Sucesso>" in xmlResponse:
            splitResult = xmlResponse.split("<ChaveNFe>")
            splitResult = splitResult[1].replace("</ChaveNFe>", "")
            strResult = splitResult.split("</NFe>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._resultDict(strResult)
        if "Erro xmlns" in xmlResponse:
            splitResult = xmlResponse.split("""<Erro xmlns="">""")
            strResult = splitResult[1].split("</Erro>")
            strResult = str(strResult[0])
            strResult = "<root>" + strResult + "</root>"
            return cls._resultDict(strResult)
        else:
            try:
                xmlResponse = xmlResponse[38:]
                splitResult = xmlResponse.split("<soap:Body>")
                strResult = splitResult[1].split("</soap:Body>")
                strResult = str(strResult[0])
                strResult = "<root>" + strResult + "</root>"
                return cls._resultDict(strResult)
            except Exception as error:
                raise error

    @classmethod
    def _resultDict(cls, strResult):
        res = {}
        root = etree.fromstring(strResult)
        for i in root.iter():
            text = i.text
            text = text.encode("utf-8", "replace") if text else None
            if text:
                res.setdefault("{tag}".format(tag=i.tag), "{text}".format(text=text))
        return res

    @classmethod
    def _getTail(cls, strResult):
        tree = etree.fromstring(strResult)
        nfeData = []
        res = {}
        for i in tree:
            res.update({
                "SerieRPS": i.find('.//SerieRPS', namespaces={}).text,
                "NumeroRPS": i.find('.//NumeroRPS', namespaces={}).text,
                "DataEmissaoNFe": i.find('.//DataEmissaoNFe', namespaces={}).text,
                "CPFCNPJTomador": i.find('.//CPFCNPJTomador/CNPJ', namespaces={}).text,
                "CodigoVerificacao": i.find('.//CodigoVerificacao', namespaces={}).text,
                "NumeroNFe": i.find('.//NumeroNFe', namespaces={}).text
            })
            nfeData.append(res.copy())
        return nfeData
