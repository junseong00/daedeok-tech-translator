#!/usr/bin/env python3
"""특구재단 공공데이터 4종(cp949 CSV) -> 정적 사이트용 JSON.

원문 왜곡 방지 원칙: 기술 개요 요약/상세, 국내외 전망은 원본 문자열을 그대로 옮긴다.
가공은 (1) 공백 정리 (2) TRL 코드 -> 3단계 배지 매핑 뿐이다.
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "raw")
OUT = Path(__file__).parent / "data"

# 원본 데이터 입력 오류로 확인된 행(0-based). 기술명과 요약 내용의 주제가 서로 다르다.
# 전후 행은 정상이라 구조적 밀림이 아닌 단발성 오류이며, 숨기지 않고 화면에 표시한다.
FLAGGED_ROWS = {22}

TRL_BADGE = {
    7: "ready", 8: "ready", 9: "ready",
    6: "collab",
    2: "early", 3: "early", 4: "early", 5: "early",
}


def clean(v):
    if pd.isna(v):
        return ""
    return re.sub(r"\s+", " ", str(v)).strip()


def build_tech():
    df = pd.read_csv(RAW / "tech.raw", encoding="cp949")
    out = []
    for i, row in df.iterrows():
        trl = row["기술 성숙도 코드"]
        trl = None if pd.isna(trl) else int(trl)
        out.append({
            "i": int(i),
            "name": clean(row["공개 기술 명"]),
            "appNo": clean(row["출원 번호"]),
            "year": clean(row["제작 연도"]),
            "trl": trl,
            "stage": TRL_BADGE.get(trl, "unknown"),
            "summary": clean(row["기술 개요 요약 내용"]),
            "detail": clean(row["기술 개요 상세 내용"]),
            "domestic": clean(row["국내 전망 내용"]),
            "overseas": clean(row["국외 전망 내용"]),
            "focus": clean(row["사업화 중점 내용"]),
            "flagged": int(i) in FLAGGED_ROWS,
        })
    return out


def build_partners():
    df = pd.read_csv(RAW / "inno.raw", encoding="cp949")
    dd = df[(df["특구지역명"] == "대덕") & (df["조직형태"] != "기업")]
    out = [
        {"name": clean(r["기관(기업)명"]), "type": clean(r["조직형태"]), "zone": clean(r["지구명"])}
        for _, r in dd.iterrows()
    ]
    out.sort(key=lambda x: (x["type"], x["name"]))
    return out


def build_context():
    labco = pd.read_csv(RAW / "labco.raw", encoding="cp949")
    dd = labco[labco["현행특구"] == "대덕"]
    by_year = dd["등록연도"].value_counts().sort_index()

    perf = pd.read_csv(RAW / "perf.raw", encoding="cp949")
    perf.columns = [clean(c) for c in perf.columns]
    daedeok = perf[perf["구분"] == "대덕"].iloc[0]

    return {
        "labcoTotal": int(len(dd)),
        "labcoByYear": {str(k): int(v) for k, v in by_year.items()},
        "transferCount": int(daedeok["기술이전건수"]),
        "transferFeeMillion": int(daedeok["기술이전료(백만원)"]),
        "perfTable": [
            {"zone": clean(r["구분"]),
             "transferCount": int(r["기술이전건수"]),
             "transferFee": int(r["기술이전료(백만원)"])}
            for _, r in perf.iterrows()
        ],
    }


def main():
    OUT.mkdir(exist_ok=True)
    tech, partners, context = build_tech(), build_partners(), build_context()

    stage_counts = {}
    for t in tech:
        stage_counts[t["stage"]] = stage_counts.get(t["stage"], 0) + 1

    payload = {
        "tech": tech,
        "partners": partners,
        "context": context,
        "stats": {
            "techTotal": len(tech),
            "stageCounts": stage_counts,
            "partnerTotal": len(partners),
            "years": sorted({t["year"] for t in tech if t["year"]}),
        },
    }

    path = OUT / "data.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    print(f"기술 {len(tech)}건 · 실행 파트너 {len(partners)}건 · "
          f"연구소기업 {context['labcoTotal']}건")
    print(f"단계 분포: {stage_counts}")
    print(f"{path} ({path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
