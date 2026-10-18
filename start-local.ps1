# Lightweight localhost server for KOTA BERSIH 3D.
# Binds only to 127.0.0.1; it is not exposed to the local network.
$ErrorActionPreference = 'Stop'
$Port = 8765
$Root = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$Listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse('127.0.0.1'), $Port)

function Get-ContentType([string]$Path) {
    switch ([System.IO.Path]::GetExtension($Path).ToLowerInvariant()) {
        '.html' { 'text/html; charset=utf-8'; break }
        '.js' { 'application/javascript; charset=utf-8'; break }
        '.css' { 'text/css; charset=utf-8'; break }
        '.json' { 'application/json; charset=utf-8'; break }
        '.webmanifest' { 'application/manifest+json; charset=utf-8'; break }
        '.svg' { 'image/svg+xml'; break }
        '.png' { 'image/png'; break }
        '.jpg' { 'image/jpeg'; break }
        '.jpeg' { 'image/jpeg'; break }
        '.ogg' { 'audio/ogg'; break }
        '.ico' { 'image/x-icon'; break }
        default { 'application/octet-stream'; break }
    }
}

try {
    $Listener.Start()
    Write-Host ''
    Write-Host 'KOTA BERSIH 3D berjalan di komputer ini.' -ForegroundColor Green
    Write-Host "Alamat: http://127.0.0.1:$Port" -ForegroundColor Cyan
    Write-Host 'Jangan tutup jendela ini selama bermain.'
    Write-Host 'Untuk berhenti, tekan Ctrl+C.'
    Start-Sleep -Milliseconds 400
    Start-Process "http://127.0.0.1:$Port"

    while ($true) {
        $Client = $Listener.AcceptTcpClient()
        try {
            $Stream = $Client.GetStream()
            $Reader = [System.IO.StreamReader]::new($Stream, [System.Text.Encoding]::ASCII, $false, 1024, $true)
            $RequestLine = $Reader.ReadLine()
            if ([string]::IsNullOrWhiteSpace($RequestLine)) { continue }
            while ($true) {
                $HeaderLine = $Reader.ReadLine()
                if ($null -eq $HeaderLine -or $HeaderLine -eq '') { break }
            }
            $Parts = $RequestLine.Split(' ')
            $Method = if ($Parts.Length -gt 0) { $Parts[0] } else { 'GET' }
            $UrlPath = if ($Parts.Length -gt 1) { $Parts[1].Split('?')[0] } else { '/' }
            if ($Method -ne 'GET' -and $Method -ne 'HEAD') {
                $Body = [System.Text.Encoding]::UTF8.GetBytes('Method Not Allowed')
                $Header = "HTTP/1.1 405 Method Not Allowed`r`nContent-Type: text/plain; charset=utf-8`r`nContent-Length: $($Body.Length)`r`nConnection: close`r`n`r`n"
                $HeaderBytes = [System.Text.Encoding]::ASCII.GetBytes($Header)
                $Stream.Write($HeaderBytes, 0, $HeaderBytes.Length)
                if ($Method -ne 'HEAD') { $Stream.Write($Body, 0, $Body.Length) }
                continue
            }
            try { $Decoded = [System.Uri]::UnescapeDataString($UrlPath) } catch { $Decoded = '/' }
            $Relative = $Decoded.TrimStart('/').Replace('/', [System.IO.Path]::DirectorySeparatorChar)
            if ([string]::IsNullOrWhiteSpace($Relative)) { $Relative = 'index.html' }
            $FullPath = [System.IO.Path]::GetFullPath((Join-Path $Root $Relative))
            if (-not $FullPath.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
                $FullPath = ''
            }
            if (-not $FullPath -or -not (Test-Path -LiteralPath $FullPath -PathType Leaf)) {
                $Body = [System.Text.Encoding]::UTF8.GetBytes('404 Not Found')
                $Header = "HTTP/1.1 404 Not Found`r`nContent-Type: text/plain; charset=utf-8`r`nContent-Length: $($Body.Length)`r`nConnection: close`r`n`r`n"
                $HeaderBytes = [System.Text.Encoding]::ASCII.GetBytes($Header)
                $Stream.Write($HeaderBytes, 0, $HeaderBytes.Length)
                if ($Method -ne 'HEAD') { $Stream.Write($Body, 0, $Body.Length) }
                continue
            }
            $Body = [System.IO.File]::ReadAllBytes($FullPath)
            $Type = Get-ContentType $FullPath
            $Header = "HTTP/1.1 200 OK`r`nContent-Type: $Type`r`nContent-Length: $($Body.Length)`r`nCache-Control: no-cache`r`nConnection: close`r`nX-Content-Type-Options: nosniff`r`n`r`n"
            $HeaderBytes = [System.Text.Encoding]::ASCII.GetBytes($Header)
            $Stream.Write($HeaderBytes, 0, $HeaderBytes.Length)
            if ($Method -ne 'HEAD') { $Stream.Write($Body, 0, $Body.Length) }
            $Stream.Flush()
        } catch {
            # Ignore a client disconnect; keep the local server alive.
        } finally {
            if ($Reader) { $Reader.Dispose() }
            if ($Stream) { $Stream.Dispose() }
            if ($Client) { $Client.Close() }
            $Reader = $null; $Stream = $null; $Client = $null
        }
    }
} finally {
    if ($Listener) { $Listener.Stop() }
}
