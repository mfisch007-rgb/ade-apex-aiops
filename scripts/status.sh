#!/data/data/com.termux/files/usr/bin/bash

# ==========================================================
# ADE-APEX Project Resume Script
# Version: 2.0
# ==========================================================

cd ~/ade-apex-aiops || exit 1

echo "========== ADE-APEX RESUME REPORT =========="

echo
echo "PROJECT:"
pwd

echo
echo "CURRENT BRANCH:"
git branch --show-current

echo
echo "LATEST 15 COMMITS:"
git --no-pager log --oneline -15

echo
echo "WORKING TREE:"
git status --short

echo
echo "DIRECTORY TREE:"
find app -type f \
    ! -path "*/__pycache__/*" \
    ! -name "*.pyc" \
    | sort

echo
echo "COMPILE CHECK:"
python -m compileall app

echo
echo "========== END OF REPORT =========="
