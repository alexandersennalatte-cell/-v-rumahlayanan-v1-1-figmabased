param(
  [string]$Url = "file:///K:/Newfolder/index.html",
  [string]$Out = "K:\Newfolder\tools\shots\desktop.png",
  [int]$Width = 1440,
  [int]$Height = 1000,
  [int]$FullPage = 1
)

$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$dir = Split-Path $Out -Parent
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$tag = [System.IO.Path]::GetFileNameWithoutExtension($Out)
$profile = "K:\Newfolder\tools\tmp\prof_$tag"
if (-not (Test-Path $profile)) { New-Item -ItemType Directory -Path $profile -Force | Out-Null }
if (Test-Path $Out) { Remove-Item $Out -Force }

$chromeArgs = @(
  "--headless=new",
  "--disable-gpu",
  "--hide-scrollbars",
  "--no-sandbox",
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-extensions",
  "--disable-features=Translate,BackForwardCache",
  "--allow-file-access-from-files",
  "--force-device-scale-factor=1",
  "--virtual-time-budget=10000",
  "--user-data-dir=$profile",
  "--window-size=$Width,$Height",
  "--screenshot=$Out"
)
if ($FullPage -eq 1) { $chromeArgs += "--screenshot-full-page" }
$chromeArgs += $Url

& $chrome @chromeArgs 2>&1 | Out-Null
Start-Sleep -Milliseconds 400
if (Test-Path $Out) {
  $size = python -c "from PIL import Image; im=Image.open(r'$Out'); print(f'{im.width}x{im.height}')"
  "rendered: $Out  $size"
} else {
  "FAILED to render $Out"
}


