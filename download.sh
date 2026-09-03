#!/usr/bin/env bash
# 연구개발특구진흥재단 공공데이터 4종 내려받기 (공공데이터포털, 로그인 불필요, 전부 cp949)
# 사용법: bash download.sh [출력디렉터리]   기본값 raw
set -e
OUT="${1:-raw}"
mkdir -p "$OUT"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

dl() {
  curl -sSL -A "$UA" -H "Referer: https://www.data.go.kr/data/$1/fileData.do" \
    "https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=$2&fileDetailSn=1&insertDataPrcus=N" \
    -o "$OUT/$3"
  echo "  -> $OUT/$3 ($(wc -c <"$OUT/$3") bytes)"
}

echo "사업화 공개 기술 세부 현황 (1,451행)";     dl 15149802 FILE_000000003518655 tech.raw
echo "특구 입주기관 통계조사 대상기관 (14,989행)"; dl 15142582 FILE_000000003234628 inno.raw
echo "연구소기업 운영현황 (1,348행)";            dl 15089826 FILE_000000003217534 labco.raw
echo "연구개발특구 연구성과 (6행)";              dl 15118213 FILE_000000003649328 perf.raw
