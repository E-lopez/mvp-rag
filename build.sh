#!/usr/bin/env bash
# Exit immediately if any single component script steps throw an unhandled error
set -o errexit

echo "======= PHASE 1: Installing Python Requirements ======="
pip install --upgrade pip
pip install -r api/requirements.txt

echo "======= PHASE 2: Compiling Frontend Distribution Production Artifacts ======="
# Navigate explicitly into the UI subdirectory to run Node tasks
cd ui
npx pnpm install --frozen-lockfile
echo "Building frontend assets..."
npx pnpm build
cd ..

echo "======= PHASE 3: Migrating Compiled Assets to FastAPI Static Directory ======="
# Ensure the backend static asset target directory exists inside 'api/app/'
mkdir -p api/app/static

# Safely copy the compiled assets from 'ui/dist/' into 'api/app/static/'
cp -r ui/dist/* api/app/static/

echo "======= BUILD PIPELINE COMPLETION SUCCESSFUL ======="