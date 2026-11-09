#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Zero-Python smart synchronization tool for jinkou-chinou domain skills (PowerShell 5.1+ / 7+).

.DESCRIPTION
    Dynamically scans domain skills and syncs them to local AI agent skill folders:
      - Gemini / Antigravity             : %USERPROFILE%\.gemini\config\skills
      - Claude Code                      : %USERPROFILE%\.claude\skills
      - GitHub Copilot                   : %USERPROFILE%\.copilot\skills
      - OpenAI / Agent Skills (ChatGPT)  : %USERPROFILE%\.agents\skills
      - OpenAI Codex                     : %USERPROFILE%\.codex\skills

    Features:
      - Zero external dependencies (works out of the box on Windows 10/11 without Python).
      - SHA-256 content hashing via .NET to scan first and only copy/overwrite changed files.
      - Safe pruning of deleted files and empty directories.
      - BOM-free UTF-8 installation marker (.installed-by-jinkou-chinou.json) compatible with sync_skills.py.
      - Supports both GNU-style flags (--dry-run, --force, --targets, --json) and PowerShell parameters.
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
        '^(-{1,2}use-?ps1|-{1,2}powershell)$' { } # consumed silently if forwarded from .bat
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
                $skills += [PSCustomObject]@{
                    Name   = $skillDir.Name
                    Domain = $domainDir.Name
                    Path   = $skillDir.FullName
                    Files  = $files
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

function Write-InstallMarker {
    param(
        [string]$SkillDest,
        [string]$SourcePath,
        [string]$DomainName
    )
    $markerPath = Join-Path $SkillDest $InstallMarker
    $utcNow = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
    $escapedSource = $SourcePath.Replace('\', '\\').Replace('"', '\"')
    $escapedDomain = $DomainName.Replace('\', '\\').Replace('"', '\"')
    $jsonText = "{`n  `"source`": `"$escapedSource`",`n  `"domain`": `"$escapedDomain`",`n  `"synced_at`": `"$utcNow`"`n}"
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText($markerPath, $jsonText, $utf8NoBom)
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
            Write-InstallMarker -SkillDest $skillDest -SourcePath $Skill.Path -DomainName $Skill.Domain
        }
        return @{ Status = "installed"; Diff = $diff }
    }

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
            Write-InstallMarker -SkillDest $skillDest -SourcePath $Skill.Path -DomainName $Skill.Domain
        }
        return @{ Status = "updated"; Diff = $diff }
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
        return @{ Status = "up-to-date"; Diff = $diff }
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

        Write-InstallMarker -SkillDest $skillDest -SourcePath $Skill.Path -DomainName $Skill.Domain
    }

    return @{ Status = "updated"; Diff = $diff }
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
        } elseif ($kLower -match "copilot|github") {
            $activeTargets["GitHub Copilot"] = $defaultTargets["GitHub Copilot"]
        } elseif ($kLower -match "chatgpt|agents|openai") {
            $activeTargets["OpenAI / Agent Skills (ChatGPT)"] = $defaultTargets["OpenAI / Agent Skills (ChatGPT)"]
        } elseif ($kLower -match "codex") {
            $activeTargets["OpenAI Codex"] = $defaultTargets["OpenAI Codex"]
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
    Write-Host ("=" * 64)
    Write-Host "   jinkou-chinou AI Skills Smart Synchronizer (PowerShell)"
    Write-Host ("=" * 64)
    Write-Host ("Current User Home : {0}" -f $userHome)
    Write-Host ("Discovered Skills : {0} domain skills" -f $skills.Count)
    if ($DryRun) {
        Write-Host "[DRY RUN MODE] No files will be modified on disk."
    }
    Write-Host ("-" * 64)
    Write-Host "Sync Destinations:"
    foreach ($name in $activeTargets.Keys) {
        Write-Host ("  * {0,-22} -> {1}" -f $name, $activeTargets[$name])
    }
    Write-Host ("=" * 64)
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

            if ($status -eq "installed") {
                $res.InstalledSkills += $skill.Name
                $res.FileChanges[$skill.Name] = $diff
                if (-not $JsonOutput) {
                    Write-Host ("  [+] INSTALLED   : {0} ({1} files)" -f $skill.Name, $diff.added.Count)
                }
            } elseif ($status -eq "updated") {
                $res.UpdatedSkills += $skill.Name
                $res.FileChanges[$skill.Name] = $diff
                $totalChanges = $diff.added.Count + $diff.modified.Count + $diff.removed.Count
                if (-not $JsonOutput) {
                    Write-Host ("  [~] UPDATED     : {0} ({1} files changed)" -f $skill.Name, $totalChanges)
                }
            } else {
                $res.UpToDateSkills += $skill.Name
                if (-not $JsonOutput) {
                    Write-Host ("  [=] UP TO DATE  : {0}" -f $skill.Name)
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

if ($JsonOutput) {
    $payload = [ordered]@{
        timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.ffffff+00:00")
        engine    = "powershell"
        dry_run   = $DryRun
        targets   = @(
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

Write-Host ("=" * 64)
Write-Host "                 DETAILED CHANGE LOG"
Write-Host ("=" * 64)

$anyChanges = $false
foreach ($r in $targetResults) {
    Write-Host ("Destination: {0} [{1}]" -f $r.TargetName, $r.TargetPath)
    if ($r.SkippedReason) {
        Write-Host ("  [SKIPPED] {0}" -f $r.SkippedReason)
        Write-Host ""
        continue
    }

    $installedOrUpdated = $r.InstalledSkills.Count + $r.UpdatedSkills.Count
    if (($installedOrUpdated -eq 0) -and ($r.FailedSkills.Count -eq 0)) {
        Write-Host "  (No changes detected -- all skills are already up to date.)"
    } else {
        if ($installedOrUpdated -gt 0) {
            $anyChanges = $true
        }
        foreach ($name in $r.InstalledSkills) {
            Write-Host ("  * [NEW SKILL] {0}" -f $name)
            $addedFiles = $r.FileChanges[$name].added
            $limit = [Math]::Min(8, $addedFiles.Count)
            for ($idx = 0; $idx -lt $limit; $idx++) {
                Write-Host ("      + {0}" -f $addedFiles[$idx])
            }
            if ($addedFiles.Count -gt 8) {
                Write-Host ("      + ... and {0} more files" -f ($addedFiles.Count - 8))
            }
        }

        foreach ($name in $r.UpdatedSkills) {
            $diff = $r.FileChanges[$name]
            Write-Host ("  * [MODIFIED]  {0}" -f $name)
            foreach ($f in $diff.added) {
                Write-Host ("      + added:    {0}" -f $f)
            }
            foreach ($f in $diff.modified) {
                Write-Host ("      ~ updated:  {0}" -f $f)
            }
            foreach ($f in $diff.removed) {
                Write-Host ("      - removed:  {0}" -f $f)
            }
        }

        foreach ($name in $r.FailedSkills.Keys) {
            Write-Host ("  * [FAILED]    {0}: {1}" -f $name, $r.FailedSkills[$name])
        }
    }
    Write-Host ""
}

Write-Host ("=" * 64)
Write-Host "                    SYNC SUMMARY"
Write-Host ("=" * 64)
foreach ($r in $targetResults) {
    if ($r.SkippedReason) {
        Write-Host ("{0,-30} : SKIPPED ({1})" -f $r.TargetName, $r.SkippedReason)
    } else {
        $failNote = if ($r.FailedSkills.Count -gt 0) { ", $($r.FailedSkills.Count) error(s)" } else { "" }
        Write-Host ("{0,-30} : {1} installed, {2} updated, {3} up-to-date{4}" -f $r.TargetName, $r.InstalledSkills.Count, $r.UpdatedSkills.Count, $r.UpToDateSkills.Count, $failNote)
    }
}
Write-Host ("-" * 64)

if ($anyChanges) {
    if ($DryRun) {
        Write-Host "DRY RUN COMPLETE: The changes above would be applied."
    } else {
        Write-Host "SUCCESS: All skills synchronized with your local AI agents!"
    }
} else {
    Write-Host "ALL SKILLS ARE CURRENT: No updates were needed."
}

Write-Host ("=" * 64)
if (-not $NoPause -and -not $JsonOutput) {
    Write-Host ""
    [void](Read-Host "Press Enter to close this window")
}
exit 0
