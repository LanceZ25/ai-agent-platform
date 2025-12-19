param aifName string
param location string = resourceGroup().location

resource aif 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: aifName
  location: location
  sku: {
    name: 'Standard'
  }
}
