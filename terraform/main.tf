provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "caresafe" {
  name     = "caresafeResourceGroup"
  location = "East US"
}




### Postgresql Database setup ###

variable "admin_username" {}
variable "admin_password" {}


resource "azurerm_postgresql_server" "caresafe" {
  name                = "caresafepostgresqlserver"
  location            = azurerm_resource_group.caresafe.location
  resource_group_name = azurerm_resource_group.caresafe.name

  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password

  sku_name   = "GP_Gen5_2"
  version    = "11"
  storage_mb = 5120

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true
  public_network_access_enabled = true
  ssl_enforcement_enabled       = true

  threat_detection_policy {
    email_account_admins = true
    email_addresses      = ["hi@merhmood.me"]
    retention_days       = 7
  }
}

resource "azurerm_postgresql_database" "caresafe" {
  name                = "caresafedb"
  resource_group_name = azurerm_resource_group.caresafe.name
  server_name         = azurerm_postgresql_server.caresafe.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

resource "azurerm_postgresql_firewall_rule" "caresafe" {
  name                = "AllowCaresSafeServerIP"
  resource_group_name = azurerm_resource_group.caresafe.name
  server_name         = azurerm_postgresql_server.caresafe.name
  start_ip_address    = azurerm_container_group.caresafe.ip_address
  end_ip_address      = azurerm_container_group.caresafe.ip_address
}




### Setup Storage Account for Container Volume ###

resource "azurerm_storage_account" "caresafe" {
  name                     = "caresafestorageaccount"
  resource_group_name      = azurerm_resource_group.caresafe.name
  location                 = azurerm_resource_group.caresafe.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "pre-prod"
  }
}





### Setup Storage Share for Container Volume ###

resource "azurerm_storage_share" "caresafe" {
  name                 = "caresafeshare"
  storage_account_name = azurerm_storage_account.caresafe.name
  quota                = 50  # Specify quota in GiB for the file share

  depends_on = [
    azurerm_storage_account.caresafe
  ]
}



### Setup ACR ###

resource "azurerm_container_registry" "caresafeacr" {
  name                = "caresafeacr"
  resource_group_name = azurerm_resource_group.caresafe.name
  location            = azurerm_resource_group.caresafe.location
  sku                 = "Standard"  # Adjust SKU based on your requirements
  admin_enabled = true
}





### Deploy Nginx and Flask Container ###

variable "secret_key" {
  description = "Flask Secret Key"
}
variable "jwt_secret_key" {
  description = "Flask Jwt Secret Key"
}

resource "azurerm_container_group" "caresafe" {
  name                = "caresafe-containergroup"
  location            = azurerm_resource_group.caresafe.location
  resource_group_name = azurerm_resource_group.caresafe.name
  os_type             = "Linux"

  container {
    name   = "flask"
    image  = "${azurerm_container_registry.caresafeacr.login_server}/myflaskapp"
    cpu    = "0.5"
    memory = "1.5"

    environment_variables = {
      OPENAPI_API_KEY = "https://caresafekeyvault.vault.azure.net/secrets/openAiApi/c6ea54dc74824ff3b704a956a3937715"
      SECRET_KEY = var.secret_key
      JWT_SECRET_KEY = var.jwt_secret_key
      DATABASE_URL = "postgresql://${azurerm_postgresql_server.caresafe.administrator_login}:${azurerm_postgresql_server.caresafe.administrator_login_password}@${azurerm_postgresql_server.caresafe.fqdn}:5432/${azurerm_postgresql_database.caresafe.name}"
    }

    volume {
      name       = "nginx-volume"
      mount_path = "/home/app"
      read_only = false

      storage_account_name = azurerm_storage_account.caresafe.name
      share_name           = azurerm_storage_share.caresafe.name
      storage_account_key  = azurerm_storage_account.caresafe.primary_access_key
    }

    ports {
      port     = 5000
      protocol = "TCP"
    }
  }

  container {
    name   = "nginx"
    image  = "${azurerm_container_registry.caresafeacr.login_server}/mynginxapp"
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }

    ports {
      port     = 443
      protocol = "TCP"
    }

    volume {
      name = "certbot-etc"
      mount_path = "/etc/letsencrypt"
      read_only = false

      storage_account_name = azurerm_storage_account.caresafe.name
      share_name           = azurerm_storage_share.caresafe.name
      storage_account_key  = azurerm_storage_account.caresafe.primary_access_key
    }

    volume {
      name = "certbot-var"
      mount_path = "/var/lib/letsencrypt"
      read_only = false

      storage_account_name = azurerm_storage_account.caresafe.name
      share_name           = azurerm_storage_share.caresafe.name
      storage_account_key  = azurerm_storage_account.caresafe.primary_access_key
    }

    volume {
      name = "certbot-www"
      mount_path = "/var/www/certbot"
      read_only = false

      storage_account_name = azurerm_storage_account.caresafe.name
      share_name           = azurerm_storage_share.caresafe.name
      storage_account_key  = azurerm_storage_account.caresafe.primary_access_key
    }
  }

  image_registry_credential {
    server   = azurerm_container_registry.caresafeacr.login_server
    username = azurerm_container_registry.caresafeacr.admin_username
    password = azurerm_container_registry.caresafeacr.admin_password
  }

  tags = {
    environment = "pre-prod"
  }
}

output "public_ip_address" {
  value = azurerm_container_group.caresafe.ip_address
}
