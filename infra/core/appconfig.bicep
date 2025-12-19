param appConfigName string
param location string = resourceGroup().location  

resource appcfg 'Microsoft.AppConfiguration/configurationStores@2022-05-01' = {
  name: appConfigName
  location: location
  sku: {
    name: 'Standard'
  }
}
