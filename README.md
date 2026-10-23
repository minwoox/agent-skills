# Personal agent skills

Claude Code와 Codex에서 사용하는 개인 스킬, 명령, 공통 작업 지침을 보관합니다.
설치된 파일의 사본을 관리하며, 홈 디렉터리와 자동으로 동기화하지 않습니다.

## 구성

| 저장소 경로 | 설치 위치 | 내용 |
| --- | --- | --- |
| `claude/skills/` | `~/.claude/skills/` | Claude용 개인 스킬과 참조 문서 |
| `claude/commands/` | `~/.claude/commands/` | Git, PR, 테스트 명령 |
| `claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | Claude 전역 작업 지침 |
| `codex/skills/` | `~/.codex/skills/` | Codex용 개인 스킬과 참조 문서 |
| `codex/AGENTS.md` | `~/.codex/AGENTS.md` | Codex 전역 작업 지침 |
| `agents/skills/` | `~/.agents/skills/` | Codex로 이관된 Git 및 PR 스킬 |

개인 스킬은 `engineering-change-workflow`와 `deep-review`입니다.
개발 워크플로는 두 도구에서 같은 내용을 사용합니다.
`deep-review`는 각 도구의 지침 파일 탐색 방식에 맞춰져 있습니다.

플러그인 캐시, Codex 기본 제공 스킬, 인증 정보, 세션 기록, 백업은 포함하지 않습니다.
참조 문서에 있는 원본 출처 링크는 유지합니다.

## 설치

저장소 루트에서 실행합니다. 같은 경로에 파일이 있으면 저장소의 내용으로 덮어씁니다.

```sh
mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.agents"
cp -R claude/. "$HOME/.claude/"
cp -R codex/. "$HOME/.codex/"
cp -R agents/. "$HOME/.agents/"
```

새 세션에서 스킬을 확인합니다. Claude의 상세 리뷰는 `/deep-review`로 실행합니다.

## 변경 사항 저장

설치 위치에서 스킬을 수정했다면 변경한 파일을 위 표의 저장소 경로에 복사합니다.
저장소에서 수정했다면 설치할 파일을 홈 디렉터리의 대응 경로에 복사합니다.
파일 삭제와 이름 변경도 양쪽에서 직접 반영합니다.

변경을 확인한 뒤 해당 파일만 커밋하고 푸시합니다.

```sh
git diff
git status --short
git add -- <변경한-파일>
git commit
git push
```

## 기존 명령의 외부 의존성

Git 및 PR 명령은 현재 설치된 내용을 그대로 보관합니다.
다음 참조 대상은 원본 환경에도 없으므로 이 저장소에 포함되어 있지 않습니다.
해당 명령을 실행하기 전에 참조를 수정하거나 필요한 항목을 제공해야 합니다.

- PR 생성 및 설명 갱신 명령의 `github-context.sh`와 `_pr-description-generator` 에이전트
- Codex 이관 스킬의 `~/.Codex/scripts/` 및 `~/.Codex/commands/` 경로
- 커밋 명령의 `how-to-commit` 규칙. 현재 커밋 지침은 각 도구의 전역 지침과
  `engineering-change-workflow/references/commits.md`에 있습니다.
