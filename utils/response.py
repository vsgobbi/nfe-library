from lxml import etree
from re import search


class Response:

    @classmethod
    def resultDict(cls, strResult):
        responseGroup = search("\<RetornoXML>(.*)\</Retorno", strResult).group(1)
        res = {}
        root = etree.fromstring(responseGroup)
        for i in root.iter():
            text = i.text
            text = text.encode("utf-8", "replace") if text else None
            if text:
                res.setdefault("{tag}".format(tag=i.tag), "{text}".format(text=text))
        return res

    @classmethod
    def getTail(cls, strResult):
        responseGroup = search("\<RetornoXML>(.*)\</Retorno", strResult).group(1)
        responseGroup = search("\</Cabecalho>(.*)\</Retorno", responseGroup).group(1)
        root = "<root>" + responseGroup + "</root>"
        tree = etree.fromstring(root)
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
