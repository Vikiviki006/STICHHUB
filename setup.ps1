# Base directory
$BASE = "D:\STICHHUB"

# Root folders
New-Item -ItemType Directory -Force -Path "$BASE\backend","$BASE\frontend","$BASE\docs"

# Backend structure
New-Item -ItemType Directory -Force -Path `
"$BASE\backend\app\api\v1\endpoints",
"$BASE\backend\app\core",
"$BASE\backend\app\db",
"$BASE\backend\app\models",
"$BASE\backend\app\schemas",
"$BASE\backend\app\services",
"$BASE\backend\app\utils",
"$BASE\backend\alembic\versions",
"$BASE\backend\tests"

# Frontend structure
New-Item -ItemType Directory -Force -Path `
"$BASE\frontend\src\api",
"$BASE\frontend\src\components\catalog",
"$BASE\frontend\src\components\calculator",
"$BASE\frontend\src\components\auth",
"$BASE\frontend\src\components\ar",
"$BASE\frontend\src\components\shipping",
"$BASE\frontend\src\components\shared",
"$BASE\frontend\src\pages",
"$BASE\frontend\src\hooks",
"$BASE\frontend\src\store",
"$BASE\frontend\src\utils",
"$BASE\frontend\src\types",
"$BASE\frontend\public"

# Create Python __init__.py files
Get-ChildItem "$BASE\backend\app" -Recurse -Directory | ForEach-Object {
    New-Item -ItemType File -Path "$($_.FullName)\__init__.py" -Force
}

# Placeholder files
New-Item -ItemType File -Force -Path `
"$BASE\backend\app\main.py",
"$BASE\backend\requirements.txt",
"$BASE\frontend\package.json",
"$BASE\docs\README.md"

Write-Host "✅ StitchHub structure created!"


$files = @(
"backend/app/api/__init__.py",
"backend/app/api/v1/__init__.py",
"backend/app/api/v1/endpoints/__init__.py",
"backend/app/models/__init__.py",
"backend/app/schemas/__init__.py",
"backend/app/services/__init__.py",
"backend/app/core/__init__.py",
"backend/app/db/__init__.py",
"backend/app/utils/__init__.py"
)

foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force
}

Write-Output "done"

mkdir backend/app/utils; New-Item backend/app/utils/__init__.py -ItemType File -Force; echo "done"



#Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#.\setup.ps1