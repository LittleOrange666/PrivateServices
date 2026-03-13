Set-Location vue-app
pnpm build
Set-Location ..
if (Test-Path dist) {
    Remove-Item -Path dist -Recurse -Force
}
Copy-Item -Recurse -Force vue-app/dist dist