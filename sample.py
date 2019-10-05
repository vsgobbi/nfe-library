from gateways.saopaulo import SaopauloGateway

nota = {
    "inscricaoPrestador": "57038597",
    "serieRps": "TESTE",
    "tipoRps": "RPS",
    "tributacaoRps": "T",
    "valorPis": "0",
    "valorCofins": "0",
    "valorInss": "0",
    "valorIr": "0",
    "valorCsll": "0",
    "valorServicos": "1",
    "valorDeducoes": "0",
    "aliquotaServicos": "2",
    "numeroRps": "9117092019",
    "dataEmissao": "2019-07-09",
    "statusRps": "N",
    "codigoServico": "05895",
    "issRetido": "false",
    "senderTaxId": "20018183000180",
    "receiverTaxId": "30134945000167",
    "receiverName": "HUMMINGBIRD HEALTH PRODUCTS",
    "receiverStreetLine1": "Null",
    "receiverStreetNumber": "123",
    "receiverStreetLine2": "Null",
    "receiverDistrict": "Null",
    "receiverCity": "3550308",
    "receiverState": "SP",
    "receiverZipCode": "00000000",
    "receiverEmail": "none@none",
    "description": "Teste de emissao de NFS-e de boletos prestados",
}

certificateFile = "./converted.crt"
privateKeyRSA = "./RSAPrivateKey.pem"

privateKeyContent = open(privateKeyRSA).read()
certificateContent = open(certificateFile).read()

SaopauloGateway.sendRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
)
