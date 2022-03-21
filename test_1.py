"""diccionario = {}
contenido = ["a", "b", "c"]
aux = contenido[0]
diccionario[contenido[0]] = [contenido[1], contenido[2]]

print(diccionario["a"][0])
"""

algo = {
    "DueDate": "Fecha actual: Date.now()",
    "DocNumber": "1053811422",
    "Status": "Payable",
    "Line": [
        {
            "Amount": 500,
            "DetailType": "ExpenseDetail",
            "ExpenseDetail": {
                "Customer": {
                    "value": "ABC123",
                    "name": "Sample Customer",
                    "Ref": {
                        "value": "DEF234",
                        "name": "Sample Construction"
                    }
                },
                "Account": {
                    "value": "EFG345",
                    "name": "Fuel"
                },
                "LineStatus": "Billable"
            }
        }
    ],
    "Vendor": {
        "value": "GHI456",
        "name": "Sample Bank"
    },
    "TotalAmt": 1990.19
}

print(algo["Line"][0]["ExpenseDetail"]["Customer"]["Ref"]["value"])
