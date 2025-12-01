param(
    [string]$Email = $env:TEST_USER_EMAIL,
    [string]$Password = $env:TEST_USER_PASSWORD,
    [string]$Url = 'http://127.0.0.1:5000/api/auth/login'
)

if (-not $Email -or -not $Password) {
    Write-Host "Usage: .\test_login.ps1 -Email <email> -Password <password>"
    Write-Host "Or set environment variables TEST_USER_EMAIL and TEST_USER_PASSWORD"
    exit 1
}

$body = @{ email = $Email; password = $Password } | ConvertTo-Json
try {
    $resp = Invoke-RestMethod -Uri $Url -Method Post -Body $body -ContentType 'application/json'
    Write-Host "Status: Success"
    $resp | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Request failed:`n$($_.Exception.Message)"
    if ($_.Exception.Response) {
        $_.Exception.Response | Format-List * -Force
    }
    exit 1
}
