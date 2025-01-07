function Create-AKSAutomatic {
    param (
        [parameter(Mandatory=$true)]
        [alias('rg')]
        [string]$resourceGroupName,

        [parameter(Mandatory=$true)]
        [alias('name')]
        [string]$clusterName
    )

    begin {
        $subscription = az account show
        if ($subscription -eq $null) {
            Write-Error "No subscription is chosen. Please run: az login"
        }
    }

    process {
        az aks create -g $resourceGroupName -n $clusterName --sku automatic
    }

    end {
        Write-Output "Cluster Created"
    }
}
Create-AKSAutomatic -resourceGroupName "devrelasaservice" -clusterName "myAKSClust"