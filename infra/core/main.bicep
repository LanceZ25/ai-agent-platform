param storageAccountName string
param keyVaultName string
param appConfigName string
param appInsightsName string
param aifName string
param location string = resourceGroup().location

module storageModule './storage.bicep' = {
  name: 'storageModule'
  params: { storageAccountName: storageAccountName, location: location }
}

module kvModule './keyvault.bicep' = {
  name: 'kvModule'
  params: { keyVaultName: keyVaultName, location: location }
}

module appConfigModule './appconfig.bicep' = {
  name: 'appConfigModule'
  params: { appConfigName: appConfigName, location: location }
}

module appInsightsModule './appinsights.bicep' = {
  name: 'appInsightsModule'
  params: { appInsightsName: appInsightsName, location: location }
}

module aifModule './ai-foundry.bicep' = {
  name: 'aifModule'
  params: { aifName: aifName, location: location }
}





