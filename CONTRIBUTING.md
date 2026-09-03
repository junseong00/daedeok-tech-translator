# 팀 작업 규칙

팀 **일했음청년** 3인(박준성 · 김주희 · 노도원)이 이 저장소에서 함께 작업하기 위한 규칙입니다.
목적은 형식을 갖추는 게 아니라 **셋이 동시에 작업해도 서로의 코드가 사라지지 않게** 하는 것입니다.

## 한 번만 하는 준비

```bash
git clone https://github.com/junseong00/daedeok-tech-translator.git
cd daedeok-tech-translator
git config user.name "본인 GitHub 아이디"
git config user.email "GitHub에 등록한 메일"
```

이름과 메일을 설정하지 않으면 커밋이 누구 것인지 GitHub에 표시되지 않습니다.

사이트를 띄워 확인할 때는 파일을 더블클릭하지 말고 서버로 여세요. `file://`로 열면 브라우저 보안 정책 때문에 `data/data.json`을 못 읽습니다.

```bash
python3 -m http.server 8000   # http://localhost:8000 에서 확인
```

## 작업 흐름

`main`은 **항상 열어서 동작하는 상태**로 둡니다. 모든 작업은 브랜치에서 하고 PR로 합칩니다.

```bash
git switch main && git pull          # 1. 항상 최신 main에서 시작
git switch -c feat/trl-badge         # 2. 브랜치 파기
                                     # 3. 작업
git add -A && git commit -m "TRL 배지를 3단계로 표시"
git push -u origin feat/trl-badge    # 4. 올리기 (첫 push만 -u)
gh pr create --fill                  # 5. PR 열기 (또는 GitHub 웹에서)
```

머지된 뒤에는 브랜치를 정리합니다.

```bash
git switch main && git pull
git branch -d feat/trl-badge
```

작업이 길어지면 중간에 `git switch main && git pull` 후 `git switch -` 로 돌아와
`git merge main` 을 해두세요. 나중에 한꺼번에 충돌을 푸는 것보다 훨씬 쉽습니다.

### 브랜치 이름

| 접두사 | 쓰는 경우 | 예시 |
|---|---|---|
| `feat/` | 새 기능·화면 | `feat/detail-dialog` |
| `fix/` | 버그 수정 | `fix/empty-search-crash` |
| `data/` | 데이터 파이프라인 | `data/trl-mapping` |
| `docs/` | 문서만 | `docs/readme-datasets` |

### 커밋 메시지

한국어로, **무엇을 했는지** 한 줄이면 충분합니다. `수정`, `ㅇㅇ`, `asdf` 같은 메시지는
나중에 "어디서 깨졌지"를 찾을 때 아무 도움이 안 됩니다.

```
좋음:  검색 결과 0건일 때 안내 문구 추가
좋음:  TRL 값 없는 64건을 '성숙도 미공개'로 분리
나쁨:  수정
나쁨:  index.html 변경
```

## 충돌을 막는 두 가지 규칙

### 1. `index.html`은 영역을 나눠서 만집니다

이 프로젝트는 단일 파일 웹앱이라 **충돌이 날 지점은 사실상 `index.html` 하나뿐**입니다.
파일은 세 영역으로 나뉘어 있습니다.

| 영역 | 위치 | 내용 |
|---|---|---|
| 스타일 | `<style>` 블록 | CSS |
| 마크업 | `<body>` ~ `</dialog>` | 검색창 · 카드 목록 · 상세 다이얼로그 |
| 로직 | 아래쪽 `<script>` 블록 | 검색 · 필터 · 렌더링 |

**작업을 시작하기 전에 어느 영역을 만질지 팀에 먼저 말하세요.** 두 사람이 같은 영역을
동시에 고치는 상황이 되면, 한 명이 먼저 머지하고 다른 한 명이 `git merge main`으로
받아온 뒤 이어서 작업합니다.

### 2. `data/data.json`은 손으로 고치지 않습니다

1.9MB 생성물입니다. 두 사람이 각자 재생성해서 커밋하면 충돌이 나는데,
이 파일은 **손으로 충돌을 풀 수 없습니다.**

- 데이터를 바꾸려면 `build_data.py`만 고칩니다.
- 재생성과 커밋은 **한 번에 한 사람만** 합니다.

```bash
bash download.sh          # 원본 CSV 4종 내려받기 (raw/ 에 저장, git 추적 안 함)
python3 build_data.py     # raw/ -> data/data.json
```

혹시 `data/data.json`에서 충돌이 나면 손으로 풀지 말고 재생성하세요.

```bash
git checkout --theirs data/data.json   # 상대 것으로 일단 맞추고
python3 build_data.py                  # 다시 생성
git add data/data.json
```

## 하지 말아야 할 것

- **`git push --force`** — 원격 히스토리를 덮어써서 남의 커밋이 사라집니다.
  정말 필요하면 `--force-with-lease`를 쓰고, 쓰기 전에 팀에 말하세요.
- **`main`에 직접 push** — 리뷰 없이 깨진 코드가 들어가면 셋 다 막힙니다.
- **`raw/` 커밋** — 원본 CSV는 `.gitignore`에 있습니다. `download.sh`로 언제든 다시 받습니다.
- **API 키·비밀번호 커밋** — 지금은 키를 쓰지 않지만, 나중에 추가된다면
  파일에 직접 적지 말고 팀에 먼저 물어보세요. 한 번 커밋되면 히스토리에 영구히 남습니다.

## 코드에 손대기 전에 알아둘 것

이 서비스에는 README에 적어둔 원칙이 있고, 코드 리뷰에서 이 기준으로 봅니다.

- **기술 설명 원문을 요약하거나 다시 쓰지 않습니다.** 가공은 공백 정리와 TRL 배지 매핑 두 가지뿐입니다.
- **데이터의 한계를 화면에서 감추지 않습니다.** TRL 3~5가 88.6%라는 사실, 기관이
  개별 기술과 매칭된 결과가 아니라는 사실은 그대로 보여줍니다.
- 입력 오류로 확인된 행(`build_data.py`의 `FLAGGED_ROWS`)도 숨기지 않고 표시합니다.

## 리뷰

PR은 **본인 외 한 명**이 보고 승인하면 머지합니다. 리뷰어는 이것만 봐도 충분합니다.

1. 로컬에서 띄워 봤을 때 동작하는가
2. 검색이 여전히 되는가 (`반려동물`, `친환경 포장` 정도로 확인)
3. 위의 "코드에 손대기 전에 알아둘 것"을 어기지 않았는가

막히면 PR에 그냥 코멘트로 물어보세요. 혼자 30분 넘게 붙잡고 있지 않는 게 팀 전체에 이득입니다.
