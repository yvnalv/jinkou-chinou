#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Zero-Python smart synchronization tool for jinkou-chinou domain skills (PowerShell 5.1+ / 7+).

.DESCRIPTION
    Dynamically scans domain skills and syncs them to local AI agent skill folders:
      - Gemini / Antigravity             : %USERPROFILE%\.gemini\config\skills
      - Claude Code                      : %USERPROFILE%\.claude\skills
      - Cursor IDE                       : %USERPROFILE%\.cursor\skills
      - GitHub Copilot                   : %USERPROFILE%\.copilot\skills
      - OpenAI / Agent Skills (ChatGPT)  : %USERPROFILE%\.agents\skills
      - OpenAI Codex                     : %USERPROFILE%\.codex\skills

    Features:
      - Zero external dependencies (works out of the box on Windows 10/11 without Python).
      - SHA-256 content hashing via .NET to scan first and only copy/overwrite changed files.
      - Safe pruning of deleted files and empty directories.
      - Per-skill version tracking (vX.Y.Z, vOld -> vNew, vX.Y.Z (modified), NEW (vX.Y.Z)).
      - Installed Skills & Version Catalog + Remote GitHub (origin/main) update check.
#>

$ErrorActionPreference = "Stop"

# Parse both PowerShell-style (-DryRun) and GNU-style (--dry-run) arguments
$DryRun = $false
$Force = $false
$TargetsArg = ""
$NoPause = $false
$JsonOutput = $false

for ($i = 0; $i -lt $args.Count; $i++) {
    $arg = [string]$args[$i]
    switch -Regex ($arg) {
        '^(-{1,2}dry-?run)$' { $DryRun = $true }
        '^(-{1,2}force)$' { $Force = $true }
        '^(-{1,2}no-?pause|/no-?pause)$' { $NoPause = $true }
        '^(-{1,2}json)$' { $JsonOutput = $true }
        '^(-{1,2}use-?ps1|-{1,2}powershell)$' { }
        '^(-{1,2}targets?)(=(.*))?$' {
            if ($Matches[3]) {
                $TargetsArg = $Matches[3]
            } elseif (($i + 1) -lt $args.Count) {
                $i++
                $TargetsArg = [string]$args[$i]
            }
        }
        '^(-{1,2}help|-\?|/\?)$' {
            Write-Host "Usage: powershell -ExecutionPolicy Bypass -File tools/sync_skills.ps1 [--dry-run] [--force] [--targets gemini,claude] [--json]"
            exit 0
        }
    }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$DomainsDir = Join-Path $RootDir "domains"
$InstallMarker = ".installed-by-jinkou-chinou.json"

$IgnoredNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
@("__pycache__", ".git", ".DS_Store", "Thumbs.db", "desktop.ini", $InstallMarker) | ForEach-Object {
    [void]$IgnoredNames.Add($_)
}
$IgnoredSuffixes = @(".pyc", ".pyo", ".tmp")

function Get-Sha256Hex {
    param([string]$FilePath)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $stream = [System.IO.File]::OpenRead($FilePath)
    try {
        $hashBytes = $sha256.ComputeHash($stream)
        return ([System.BitConverter]::ToString($hashBytes)).Replace("-", "").ToLowerInvariant()
    } finally {
        $stream.Dispose()
        $sha256.Dispose()
    }
}

function Get-SkillVersion {
    param([string]$SkillDir)
    $yamlPath = Join-Path (Join-Path $SkillDir "config") "skill.yaml"
    if (Test-Path -LiteralPath $yamlPath -PathType Leaf) {
        try {
            $content = [System.IO.File]::ReadAllText($yamlPath)
            if ($content -match '(?m)^\s*version\s*:\s*["'']?([^"''\s#]+)["'']?') {
                return $Matches[1].Trim()
            }
        } catch {}
    }

    $mdPath = Join-Path $SkillDir "SKILL.md"
    if (Test-Path -LiteralPath $mdPath -PathType Leaf) {
        try {
            $content = [System.IO.File]::ReadAllText($mdPath)
            if ($content -match '(?m)^\s*version\s*:\s*["'']?([^"''\s#]+)["'']?') {
                return $Matches[1].Trim()
            }
        } catch {}
    }
    return "0.1.0"
}

function Read-InstallMarker {
    param([string]$SkillDest)
    $markerPath = Join-Path $SkillDest $InstallMarker
    $result = @{}
    if (Test-Path -LiteralPath $markerPath -PathType Leaf) {
        try {
            $raw = [System.IO.File]::ReadAllText($markerPath)
            $obj = $raw | ConvertFrom-Json
            foreach ($prop in $obj.PSObject.Properties) {
                if ($null -ne $prop.Value) {
                    $result[$prop.Name] = [string]$prop.Value
                }
            }
        } catch {}
    }
    return $result
}

function Write-InstallMarker {
    param(
        [string]$SkillDest,
        [string]$SkillName,
        [string]$DomainName,
        [string]$VersionStr,
        [string]$SourcePath,
        [string]$InstalledAt,
        [string]$UpdatedAt
    )
    $markerPath = Join-Path $SkillDest $InstallMarker
    $escSkill = $SkillName.Replace('\', '\\').Replace('"', '\"')
    $escDomain = $DomainName.Replace('\', '\\').Replace('"', '\"')
    $escVer = $VersionStr.Replace('\', '\\').Replace('"', '\"')
    $escSource = $SourcePath.Replace('\', '\\').Replace('"', '\"')
    $jsonText = "{`n  `"skill`": `"$escSkill`",`n  `"domain`": `"$escDomain`",`n  `"version`": `"$escVer`",`n  `"source`": `"$escSource`",`n  `"installed_at`": `"$InstalledAt`",`n  `"updated_at`": `"$UpdatedAt`",`n  `"synced_at`": `"$UpdatedAt`"`n}"
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText($markerPath, $jsonText, $utf8NoBom)
}

function Get-FallbackIso {
    param([string]$SkillDest)
    $targetFile = Join-Path $SkillDest "SKILL.md"
    if (-not (Test-Path -LiteralPath $targetFile)) {
        $targetFile = $SkillDest
    }
    try {
        $item = Get-Item -LiteralPath $targetFile -Force
        return $item.LastWriteTimeUtc.ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
    } catch {
        return (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
    }
}

function Get-FolderCreatedIso {
    param([string]$SkillDest)
    try {
        $item = Get-Item -LiteralPath $SkillDest -Force
        return $item.CreationTimeUtc.ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
    } catch {
        return Get-FallbackIso -SkillDest $SkillDest
    }
}

function ConvertFrom-IsoToLocal {
    param([string]$IsoStr)
    if ($IsoStr) {
        try {
            return ([DateTimeOffset]::Parse($IsoStr)).LocalDateTime
        } catch {}
    }
    return (Get-Date)
}

function Format-DateShort {
    param([string]$IsoStr)
    return (ConvertFrom-IsoToLocal -IsoStr $IsoStr).ToString("yyyy-MM-dd")
}

function Format-DateTimeMin {
    param([string]$IsoStr)
    return (ConvertFrom-IsoToLocal -IsoStr $IsoStr).ToString("yyyy-MM-dd HH:mm")
}

function Scan-SkillFolder {
    param([string]$FolderPath)
    $fileMap = @{}
    if (-not (Test-Path -LiteralPath $FolderPath -PathType Container)) {
        return $fileMap
    }

    $rootFull = [System.IO.Path]::GetFullPath($FolderPath)
    if (-not $rootFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $rootFull += [System.IO.Path]::DirectorySeparatorChar
    }

    $stack = [System.Collections.Generic.Stack[string]]::new()
    $stack.Push($FolderPath)

    while ($stack.Count -gt 0) {
        $currentDir = $stack.Pop()
        foreach ($subDir in [System.IO.Directory]::GetDirectories($currentDir)) {
            $dirName = [System.IO.Path]::GetFileName($subDir)
            if (-not $IgnoredNames.Contains($dirName)) {
                $stack.Push($subDir)
            }
        }

        foreach ($filePath in [System.IO.Directory]::GetFiles($currentDir)) {
            $fileName = [System.IO.Path]::GetFileName($filePath)
            if ($IgnoredNames.Contains($fileName)) { continue }

            $skipSuffix = $false
            foreach ($suffix in $IgnoredSuffixes) {
                if ($fileName.EndsWith($suffix, [System.StringComparison]::OrdinalIgnoreCase)) {
                    $skipSuffix = $true
                    break
                }
            }
            if ($skipSuffix) { continue }

            try {
                $fullFile = [System.IO.Path]::GetFullPath($filePath)
                $relPath = $fullFile.Substring($rootFull.Length).Replace('\', '/')
                $fileMap[$relPath] = Get-Sha256Hex -FilePath $fullFile
            } catch {
                continue
            }
        }
    }

    return $fileMap
}

function Discover-DomainSkills {
    $skills = @()
    if (-not (Test-Path -LiteralPath $DomainsDir -PathType Container)) {
        return $skills
    }

    $domainDirs = Get-ChildItem -LiteralPath $DomainsDir -Directory | Sort-Object Name
    foreach ($domainDir in $domainDirs) {
        if ($IgnoredNames.Contains($domainDir.Name)) { continue }
        $skillDirs = Get-ChildItem -LiteralPath $domainDir.FullName -Directory | Sort-Object Name
        foreach ($skillDir in $skillDirs) {
            if ($IgnoredNames.Contains($skillDir.Name)) { continue }
            $skillMd = Join-Path $skillDir.FullName "SKILL.md"
            if (Test-Path -LiteralPath $skillMd -PathType Leaf) {
                $files = Scan-SkillFolder -FolderPath $skillDir.FullName
                $ver = Get-SkillVersion -SkillDir $skillDir.FullName
                $skills += [PSCustomObject]@{
                    Name    = $skillDir.Name
                    Domain  = $domainDir.Name
                    Version = $ver
                    Path    = $skillDir.FullName
                    Files   = $files
                }
            }
        }
    }
    return $skills
}

function Resolve-DefaultTargets {
    $userHome = [Environment]::GetFolderPath("UserProfile")
    if (-not $userHome) { $userHome = $HOME }

    $codexHome = $env:CODEX_HOME
    if ($codexHome) {
        $legacyCodex = Join-Path $codexHome "skills"
    } else {
        $legacyCodex = Join-Path (Join-Path $userHome ".codex") "skills"
    }

    $targets = [ordered]@{
        "Gemini / Antigravity"            = Join-Path (Join-Path (Join-Path $userHome ".gemini") "config") "skills"
        "Claude Code"                     = Join-Path (Join-Path $userHome ".claude") "skills"
        "Cursor IDE"                      = Join-Path (Join-Path $userHome ".cursor") "skills"
        "GitHub Copilot"                  = Join-Path (Join-Path $userHome ".copilot") "skills"
        "OpenAI / Agent Skills (ChatGPT)" = Join-Path (Join-Path $userHome ".agents") "skills"
        "OpenAI Codex"                    = $legacyCodex
    }

    $clineDir = Join-Path $userHome ".cline"
    if (Test-Path -LiteralPath $clineDir -PathType Container) {
        $targets["Cline"] = Join-Path $clineDir "skills"
    }
    $cagentDir = Join-Path $userHome ".cagent"
    if (Test-Path -LiteralPath $cagentDir -PathType Container) {
        $targets["CAgent"] = Join-Path $cagentDir "skills"
    }

    return $targets
}

function Format-VersionDisplay {
    param([PSCustomObject]$Meta)
    if ($Meta.Status -eq "installed") {
        return "NEW (v$($Meta.CurrVersion))"
    }
    if ($Meta.Status -eq "updated") {
        if ($Meta.PrevVersion -and ($Meta.PrevVersion -ne $Meta.CurrVersion)) {
            return "v$($Meta.PrevVersion) -> v$($Meta.CurrVersion)"
        }
        return "v$($Meta.CurrVersion) (modified)"
    }
    return "v$($Meta.CurrVersion)"
}

function Format-StatusDisplay {
    param([PSCustomObject]$Meta)
    if ($Meta.Status -eq "installed") { return "[+] INSTALLED" }
    if ($Meta.Status -eq "updated") { return "[~] UPDATED" }
    return "[=] CURRENT"
}

function Sync-SkillToDestination {
    param(
        [PSCustomObject]$Skill,
        [string]$DestDir,
        [bool]$IsDryRun,
        [bool]$IsForce
    )
    $skillDest = Join-Path $DestDir $Skill.Name
    $diff = @{
        added    = @()
        modified = @()
        removed  = @()
    }
    $nowIso = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")

    if (-not (Test-Path -LiteralPath $skillDest)) {
        $diff.added = @($Skill.Files.Keys | Sort-Object)
        if (-not $IsDryRun) {
            [void][System.IO.Directory]::CreateDirectory($skillDest)
            foreach ($relPath in $diff.added) {
                $srcFile = Join-Path $Skill.Path ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
                $dstFile = Join-Path $skillDest ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
                $dstParent = Split-Path -Parent $dstFile
                if (-not (Test-Path -LiteralPath $dstParent)) {
                    [void][System.IO.Directory]::CreateDirectory($dstParent)
                }
                Copy-Item -LiteralPath $srcFile -Destination $dstFile -Force
            }
            Write-InstallMarker -SkillDest $skillDest -SkillName $Skill.Name -DomainName $Skill.Domain -VersionStr $Skill.Version -SourcePath $Skill.Path -InstalledAt $nowIso -UpdatedAt $nowIso
        }
        $meta = [PSCustomObject]@{
            Name           = $Skill.Name
            Domain         = $Skill.Domain
            Status         = "installed"
            PrevVersion    = $null
            CurrVersion    = $Skill.Version
            InstalledAt    = $nowIso
            UpdatedAt      = $nowIso
            ChangedThisRun = $true
        }
        return @{ Status = "installed"; Diff = $diff; Meta = $meta }
    }

    $oldMarker = Read-InstallMarker -SkillDest $skillDest
    $prevVersion = if ($oldMarker.ContainsKey("version") -and $oldMarker["version"]) { $oldMarker["version"] } else { Get-SkillVersion -SkillDir $skillDest }
    $fallbackIso = if ($oldMarker.ContainsKey("synced_at") -and $oldMarker["synced_at"]) { $oldMarker["synced_at"] } else { Get-FallbackIso -SkillDest $skillDest }
    $createdIso = Get-FolderCreatedIso -SkillDest $skillDest
    $rawInstalled = if ($oldMarker.ContainsKey("installed_at") -and $oldMarker["installed_at"]) { $oldMarker["installed_at"] } else { $createdIso }
    $installedAt = if ((ConvertFrom-IsoToLocal -IsoStr $createdIso) -lt (ConvertFrom-IsoToLocal -IsoStr $rawInstalled)) { $createdIso } else { $rawInstalled }
    $prevUpdatedAt = if ($oldMarker.ContainsKey("updated_at") -and $oldMarker["updated_at"]) { $oldMarker["updated_at"] } else { $fallbackIso }

    $destFiles = Scan-SkillFolder -FolderPath $skillDest

    if ($IsForce) {
        $diff.modified = @($Skill.Files.Keys | Sort-Object)
        if (-not $IsDryRun) {
            Remove-Item -LiteralPath $skillDest -Recurse -Force
            [void][System.IO.Directory]::CreateDirectory($skillDest)
            foreach ($relPath in $diff.modified) {
                $srcFile = Join-Path $Skill.Path ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
                $dstFile = Join-Path $skillDest ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
                $dstParent = Split-Path -Parent $dstFile
                if (-not (Test-Path -LiteralPath $dstParent)) {
                    [void][System.IO.Directory]::CreateDirectory($dstParent)
                }
                Copy-Item -LiteralPath $srcFile -Destination $dstFile -Force
            }
            Write-InstallMarker -SkillDest $skillDest -SkillName $Skill.Name -DomainName $Skill.Domain -VersionStr $Skill.Version -SourcePath $Skill.Path -InstalledAt $installedAt -UpdatedAt $nowIso
        }
        $meta = [PSCustomObject]@{
            Name           = $Skill.Name
            Domain         = $Skill.Domain
            Status         = "updated"
            PrevVersion    = $prevVersion
            CurrVersion    = $Skill.Version
            InstalledAt    = $installedAt
            UpdatedAt      = $nowIso
            ChangedThisRun = $true
        }
        return @{ Status = "updated"; Diff = $diff; Meta = $meta }
    }

    $addedList = @()
    $modifiedList = @()
    $removedList = @()

    foreach ($relPath in ($Skill.Files.Keys | Sort-Object)) {
        $srcHash = $Skill.Files[$relPath]
        if (-not $destFiles.ContainsKey($relPath)) {
            $addedList += $relPath
        } elseif ($destFiles[$relPath] -ne $srcHash) {
            $modifiedList += $relPath
        }
    }

    foreach ($relPath in ($destFiles.Keys | Sort-Object)) {
        if (-not $Skill.Files.ContainsKey($relPath)) {
            $removedList += $relPath
        }
    }

    $diff.added = $addedList
    $diff.modified = $modifiedList
    $diff.removed = $removedList

    $hasChanges = ($addedList.Count -gt 0) -or ($modifiedList.Count -gt 0) -or ($removedList.Count -gt 0)
    if (-not $hasChanges) {
        if (-not $IsDryRun -and (-not $oldMarker.ContainsKey("version") -or -not $oldMarker.ContainsKey("installed_at") -or -not $oldMarker.ContainsKey("updated_at") -or ($oldMarker["installed_at"] -ne $installedAt))) {
            Write-InstallMarker -SkillDest $skillDest -SkillName $Skill.Name -DomainName $Skill.Domain -VersionStr $Skill.Version -SourcePath $Skill.Path -InstalledAt $installedAt -UpdatedAt $prevUpdatedAt
        }
        $meta = [PSCustomObject]@{
            Name           = $Skill.Name
            Domain         = $Skill.Domain
            Status         = "up-to-date"
            PrevVersion    = $prevVersion
            CurrVersion    = $Skill.Version
            InstalledAt    = $installedAt
            UpdatedAt      = $prevUpdatedAt
            ChangedThisRun = $false
        }
        return @{ Status = "up-to-date"; Diff = $diff; Meta = $meta }
    }

    if (-not $IsDryRun) {
        foreach ($relPath in ($addedList + $modifiedList)) {
            $srcFile = Join-Path $Skill.Path ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
            $dstFile = Join-Path $skillDest ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
            $dstParent = Split-Path -Parent $dstFile
            if (-not (Test-Path -LiteralPath $dstParent)) {
                [void][System.IO.Directory]::CreateDirectory($dstParent)
            }
            Copy-Item -LiteralPath $srcFile -Destination $dstFile -Force
        }

        $skillDestFull = [System.IO.Path]::GetFullPath($skillDest)
        foreach ($relPath in $removedList) {
            $dstFile = Join-Path $skillDest ($relPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
            if (Test-Path -LiteralPath $dstFile -PathType Leaf) {
                Remove-Item -LiteralPath $dstFile -Force
            }
            $parentDir = Split-Path -Parent $dstFile
            while ($parentDir -and ([System.IO.Path]::GetFullPath($parentDir) -ne $skillDestFull)) {
                if ((Test-Path -LiteralPath $parentDir -PathType Container) -and
                    ([System.IO.Directory]::GetFileSystemEntries($parentDir).Length -eq 0)) {
                    Remove-Item -LiteralPath $parentDir -Force
                    $parentDir = Split-Path -Parent $parentDir
                } else {
                    break
                }
            }
        }

        Write-InstallMarker -SkillDest $skillDest -SkillName $Skill.Name -DomainName $Skill.Domain -VersionStr $Skill.Version -SourcePath $Skill.Path -InstalledAt $installedAt -UpdatedAt $nowIso
    }

    $meta = [PSCustomObject]@{
        Name           = $Skill.Name
        Domain         = $Skill.Domain
        Status         = "updated"
        PrevVersion    = $prevVersion
        CurrVersion    = $Skill.Version
        InstalledAt    = $installedAt
        UpdatedAt      = $nowIso
        ChangedThisRun = $true
    }
    return @{ Status = "updated"; Diff = $diff; Meta = $meta }
}

function Test-RemoteRepoUpdates {
    $gitDir = Join-Path $RootDir ".git"
    if (-not (Test-Path -LiteralPath $gitDir)) {
        return @{ State = "skipped"; Ahead = 0; Subject = "" }
    }
    try {
        $oldEap = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        Push-Location -LiteralPath $RootDir
        try {
            $null = & git fetch origin main --quiet 2>$null
            $logOut = @(& git log "HEAD..origin/main" --oneline 2>$null)
            if ($LASTEXITCODE -ne 0) {
                return @{ State = "skipped"; Ahead = 0; Subject = "" }
            }
            $lines = @($logOut | Where-Object { $_ -and ([string]$_).Trim() -ne "" })
            if ($lines.Count -eq 0) {
                return @{ State = "up-to-date"; Ahead = 0; Subject = "" }
            }
            $firstLine = ([string]$lines[0]).Trim()
            $spaceIdx = $firstLine.IndexOf(" ")
            $subj = if ($spaceIdx -gt 0) { $firstLine.Substring($spaceIdx + 1) } else { $firstLine }
            return @{ State = "behind"; Ahead = $lines.Count; Subject = $subj }
        } finally {
            Pop-Location
            $ErrorActionPreference = $oldEap
        }
    } catch {
        return @{ State = "skipped"; Ahead = 0; Subject = "" }
    }
}

# Main execution
$defaultTargets = Resolve-DefaultTargets
$activeTargets = [ordered]@{}

if ($TargetsArg) {
    $keys = $TargetsArg.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    foreach ($k in $keys) {
        $kLower = $k.ToLowerInvariant()
        if ($kLower -match "gemini|antigravity") {
            $activeTargets["Gemini / Antigravity"] = $defaultTargets["Gemini / Antigravity"]
        } elseif ($kLower -match "claude") {
            $activeTargets["Claude Code"] = $defaultTargets["Claude Code"]
        } elseif ($kLower -match "cursor") {
            $activeTargets["Cursor IDE"] = $defaultTargets["Cursor IDE"]
        } elseif ($kLower -match "copilot|github") {
            $activeTargets["GitHub Copilot"] = $defaultTargets["GitHub Copilot"]
        } elseif ($kLower -match "chatgpt|agents|openai") {
            $activeTargets["OpenAI / Agent Skills (ChatGPT)"] = $defaultTargets["OpenAI / Agent Skills (ChatGPT)"]
        } elseif ($kLower -match "codex") {
            $activeTargets["OpenAI Codex"] = $defaultTargets["OpenAI Codex"]
        } elseif (($kLower -match "cline") -and $defaultTargets.Contains("Cline")) {
            $activeTargets["Cline"] = $defaultTargets["Cline"]
        } elseif (($kLower -match "cagent") -and $defaultTargets.Contains("CAgent")) {
            $activeTargets["CAgent"] = $defaultTargets["CAgent"]
        } else {
            $fullCustom = [System.IO.Path]::GetFullPath($k)
            $leafName = Split-Path -Leaf $fullCustom
            $activeTargets["Custom ($leafName)"] = $fullCustom
        }
    }
} else {
    $activeTargets = $defaultTargets
}

$skills = Discover-DomainSkills
$userHome = [Environment]::GetFolderPath("UserProfile")
if (-not $userHome) { $userHome = $HOME }

if (-not $JsonOutput) {
    Write-Host ("=" * 76)
    Write-Host "         jinkou-chinou AI Skills Smart Synchronizer (PowerShell)"
    Write-Host ("=" * 76)
    Write-Host ("Current User Home : {0}" -f $userHome)
    Write-Host ("Discovered Skills : {0} domain skills" -f $skills.Count)
    if ($DryRun) {
        Write-Host "[DRY RUN MODE] No files will be modified on disk."
    }
    Write-Host ("-" * 76)
    Write-Host "Sync Destinations:"
    foreach ($name in $activeTargets.Keys) {
        Write-Host ("  * {0,-32} -> {1}" -f $name, $activeTargets[$name])
    }
    Write-Host ("=" * 76)
    Write-Host ""
}

$targetResults = @()

foreach ($targetName in $activeTargets.Keys) {
    $targetPath = $activeTargets[$targetName]
    if (-not $JsonOutput) {
        Write-Host (">>> Syncing to: {0} ({1})" -f $targetName, $targetPath)
    }

    $res = [PSCustomObject]@{
        TargetName      = $targetName
        TargetPath      = $targetPath
        InstalledSkills = @()
        UpdatedSkills   = @()
        UpToDateSkills  = @()
        FailedSkills    = @{}
        FileChanges     = @{}
        SkillMeta       = @{}
        SkippedReason   = $null
    }

    try {
        if (-not $DryRun -and -not (Test-Path -LiteralPath $targetPath -PathType Container)) {
            [void][System.IO.Directory]::CreateDirectory($targetPath)
        }
    } catch {
        $res.SkippedReason = "Could not access or create folder: $($_.Exception.Message)"
        $targetResults += $res
        if (-not $JsonOutput) {
            Write-Host ("  [!] SKIPPED     : {0}" -f $res.SkippedReason)
            Write-Host "                    (Continuing to remaining AI targets...)`n"
        }
        continue
    }

    foreach ($skill in $skills) {
        try {
            $syncOut = Sync-SkillToDestination -Skill $skill -DestDir $targetPath -IsDryRun $DryRun -IsForce $Force
            $status = $syncOut.Status
            $diff = $syncOut.Diff
            $meta = $syncOut.Meta
            $res.SkillMeta[$skill.Name] = $meta
            $verLabel = Format-VersionDisplay -Meta $meta

            if ($status -eq "installed") {
                $res.InstalledSkills += $skill.Name
                $res.FileChanges[$skill.Name] = $diff
                if (-not $JsonOutput) {
                    Write-Host ("  [+] INSTALLED   : {0,-26} {1,-18} ({2} files)" -f $skill.Name, $verLabel, $diff.added.Count)
                }
            } elseif ($status -eq "updated") {
                $res.UpdatedSkills += $skill.Name
                $res.FileChanges[$skill.Name] = $diff
                $totalChanges = $diff.added.Count + $diff.modified.Count + $diff.removed.Count
                if (-not $JsonOutput) {
                    Write-Host ("  [~] UPDATED     : {0,-26} {1,-18} ({2} files changed)" -f $skill.Name, $verLabel, $totalChanges)
                }
            } else {
                $res.UpToDateSkills += $skill.Name
                if (-not $JsonOutput) {
                    Write-Host ("  [=] CURRENT     : {0,-26} {1}" -f $skill.Name, $verLabel)
                }
            }
        } catch {
            $res.FailedSkills[$skill.Name] = $_.Exception.Message
            if (-not $JsonOutput) {
                Write-Host ("  [!] FAILED      : {0} ({1}) - Continuing..." -f $skill.Name, $_.Exception.Message)
            }
        }
    }

    $targetResults += $res
    if (-not $JsonOutput) {
        Write-Host ""
    }
}

# Aggregate per-skill catalog metadata
$catalogMeta = @()
$validResults = @($targetResults | Where-Object { -not $_.SkippedReason })
foreach ($skill in $skills) {
    $chosen = $null
    foreach ($r in $validResults) {
        $m = $r.SkillMeta[$skill.Name]
        if (-not $m) { continue }
        if ($null -eq $chosen) {
            $chosen = $m
        } elseif (($m.Status -eq "installed") -and ($chosen.Status -ne "installed")) {
            $chosen = $m
        } elseif (($m.Status -eq "updated") -and ($chosen.Status -eq "up-to-date")) {
            $chosen = $m
        }
    }
    if ($null -eq $chosen) {
        $nowIso = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
        $chosen = [PSCustomObject]@{
            Name           = $skill.Name
            Domain         = $skill.Domain
            Status         = "up-to-date"
            PrevVersion    = $skill.Version
            CurrVersion    = $skill.Version
            InstalledAt    = $nowIso
            UpdatedAt      = $nowIso
            ChangedThisRun = $false
        }
    }
    $catalogMeta += $chosen
}

$remoteInfo = Test-RemoteRepoUpdates

if ($JsonOutput) {
    $payload = [ordered]@{
        timestamp    = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
        engine       = "powershell"
        dry_run      = $DryRun
        remote_check = [ordered]@{
            state          = $remoteInfo.State
            commits_ahead  = $remoteInfo.Ahead
            latest_subject = $remoteInfo.Subject
        }
        skills       = @(
            foreach ($m in $catalogMeta) {
                [ordered]@{
                    name         = $m.Name
                    domain       = $m.Domain
                    status       = $m.Status
                    prev_version = $m.PrevVersion
                    version      = $m.CurrVersion
                    installed_at = $m.InstalledAt
                    updated_at   = $m.UpdatedAt
                }
            }
        )
        targets      = @(
            foreach ($r in $targetResults) {
                [ordered]@{
                    name           = $r.TargetName
                    path           = $r.TargetPath
                    installed      = $r.InstalledSkills
                    updated        = $r.UpdatedSkills
                    up_to_date     = $r.UpToDateSkills
                    failed         = $r.FailedSkills
                    skipped_reason = $r.SkippedReason
                    changes        = $r.FileChanges
                }
            }
        )
    }
    Write-Output ($payload | ConvertTo-Json -Depth 8)
    exit 0
}

$anyChanges = $false
foreach ($r in $targetResults) {
    if (($r.InstalledSkills.Count + $r.UpdatedSkills.Count) -gt 0) {
        $anyChanges = $true
        break
    }
}

if ($anyChanges) {
    Write-Host ("=" * 76)
    Write-Host "                         DETAILED CHANGE LOG"
    Write-Host ("=" * 76)
    foreach ($r in $targetResults) {
        if ($r.SkippedReason -or (($r.InstalledSkills.Count + $r.UpdatedSkills.Count + $r.FailedSkills.Count) -eq 0)) {
            continue
        }
        Write-Host ("Destination: {0} [{1}]" -f $r.TargetName, $r.TargetPath)
        foreach ($name in $r.InstalledSkills) {
            $m = $r.SkillMeta[$name]
            $vStr = if ($m) { Format-VersionDisplay -Meta $m } else { "" }
            Write-Host ("  * [NEW SKILL] {0} ({1})" -f $name, $vStr)
            $addedFiles = $r.FileChanges[$name].added
            $limit = [Math]::Min(6, $addedFiles.Count)
            for ($idx = 0; $idx -lt $limit; $idx++) {
                Write-Host ("      + {0}" -f $addedFiles[$idx])
            }
            if ($addedFiles.Count -gt 6) {
                Write-Host ("      + ... and {0} more files" -f ($addedFiles.Count - 6))
            }
        }
        foreach ($name in $r.UpdatedSkills) {
            $m = $r.SkillMeta[$name]
            $vStr = if ($m) { Format-VersionDisplay -Meta $m } else { "" }
            $diff = $r.FileChanges[$name]
            Write-Host ("  * [MODIFIED]  {0} ({1})" -f $name, $vStr)
            foreach ($f in $diff.added) { Write-Host ("      + added:    {0}" -f $f) }
            foreach ($f in $diff.modified) { Write-Host ("      ~ updated:  {0}" -f $f) }
            foreach ($f in $diff.removed) { Write-Host ("      - removed:  {0}" -f $f) }
        }
        foreach ($name in $r.FailedSkills.Keys) {
            Write-Host ("  * [FAILED]    {0}: {1}" -f $name, $r.FailedSkills[$name])
        }
        Write-Host ""
    }
}

Write-Host ("=" * 76)
Write-Host "                     INSTALLED SKILLS & VERSION CATALOG"
Write-Host ("=" * 76)
Write-Host ("{0,-28} {1,-20} {2,-15} {3}" -f "Skill Name", "Version", "Status", "Last Synced")
Write-Host ("-" * 76)
foreach ($m in $catalogMeta) {
    $verCol = Format-VersionDisplay -Meta $m
    $stCol = Format-StatusDisplay -Meta $m
    $dateCol = (Format-DateShort -IsoStr $m.UpdatedAt) + $(if ($m.ChangedThisRun) { " *" } else { "" })
    Write-Host ("{0,-28} {1,-20} {2,-15} {3}" -f $m.Name, $verCol, $stCol, $dateCol)
}
Write-Host ("-" * 76)

if ($catalogMeta.Count -gt 0) {
    $latestUpdated = ($catalogMeta | Sort-Object { ConvertFrom-IsoToLocal -IsoStr $_.UpdatedAt } -Descending)[0]
    $latestAdded = ($catalogMeta | Sort-Object { ConvertFrom-IsoToLocal -IsoStr $_.InstalledAt } -Descending)[0]
    $luVer = if (($latestUpdated.Status -eq "updated") -and $latestUpdated.PrevVersion -and ($latestUpdated.PrevVersion -ne $latestUpdated.CurrVersion)) {
        "v$($latestUpdated.PrevVersion) -> v$($latestUpdated.CurrVersion)"
    } else {
        "v$($latestUpdated.CurrVersion)"
    }
    Write-Host ("Latest Updated : {0} ({1}) on {2}" -f $latestUpdated.Name, $luVer, (Format-DateTimeMin -IsoStr $latestUpdated.UpdatedAt))
    Write-Host ("Latest Added   : {0} (v{1}) on {2}" -f $latestAdded.Name, $latestAdded.CurrVersion, (Format-DateTimeMin -IsoStr $latestAdded.InstalledAt))
}

Write-Host ("=" * 76)
Write-Host "                           AGENT SYNC SUMMARY"
Write-Host ("=" * 76)
foreach ($r in $targetResults) {
    if ($r.SkippedReason) {
        Write-Host ("{0,-31} : SKIPPED ({1})" -f $r.TargetName, $r.SkippedReason)
    } else {
        $failNote = if ($r.FailedSkills.Count -gt 0) { ", $($r.FailedSkills.Count) error(s)" } else { "" }
        Write-Host ("{0,-31} : {1} new, {2} updated, {3} current{4}" -f $r.TargetName, $r.InstalledSkills.Count, $r.UpdatedSkills.Count, $r.UpToDateSkills.Count, $failNote)
    }
}
Write-Host ("-" * 76)

if ($remoteInfo.State -eq "behind") {
    $subj = if ($remoteInfo.Subject.Length -gt 58) { $remoteInfo.Subject.Substring(0, 58) } else { $remoteInfo.Subject }
    Write-Host ("Remote Check   : [!] UPDATE AVAILABLE ON GITHUB (origin/main is {0} commit(s) ahead:" -f $remoteInfo.Ahead)
    Write-Host ("                 `"{0}`")" -f $subj)
    Write-Host "                 -> Run 'git pull' then re-run sync-skills.bat to update!"
} elseif ($remoteInfo.State -eq "up-to-date") {
    Write-Host "Remote Check   : [OK] Up to date with GitHub (origin/main)"
} else {
    Write-Host "Remote Check   : [-] Offline / skipped (using local repository state)"
}

if ($anyChanges) {
    $maxNew = ($targetResults | ForEach-Object { $_.InstalledSkills.Count } | Measure-Object -Maximum).Maximum
    $maxUpd = ($targetResults | ForEach-Object { $_.UpdatedSkills.Count } | Measure-Object -Maximum).Maximum
    if ($DryRun) {
        Write-Host ("Overall Status : DRY RUN -- {0} new, {1} updated would be applied." -f $maxNew, $maxUpd)
    } else {
        Write-Host ("Overall Status : SUCCESS -- {0} installed, {1} updated across {2} AI agents!" -f $maxNew, $maxUpd, $targetResults.Count)
    }
} else {
    Write-Host ("Overall Status : ALL {0} SKILLS ARE CURRENT (No local updates needed)" -f $skills.Count)
}

Write-Host ("=" * 76)
if (-not $NoPause -and -not $JsonOutput) {
    Write-Host ""
    [void](Read-Host "Press Enter to close this window")
}
exit 0
