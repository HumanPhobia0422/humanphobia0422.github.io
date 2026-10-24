# humanphobia0422.github.io

HumanPhobia0422의 보안 공부 기록 블로그입니다. Jekyll과 GitHub Pages를 사용합니다.

- 블로그: https://humanphobia0422.github.io
- 저장소: https://github.com/HumanPhobia0422/humanphobia0422.github.io

## 새 글 쓰기

`_posts/` 폴더에 `YYYY-MM-DD-영문제목.md` 파일을 만들고 아래처럼 작성합니다.
날짜와 제목, 본문은 실제 작성 내용으로 바꿉니다.

```markdown
---
title: "글 제목"
date: YYYY-MM-DD
categories: []
tags: []
---

여기에 글 내용을 작성합니다.
```

`main` 브랜치에 커밋하고 push하면 GitHub Pages가 배포합니다.
저장소의 Actions 탭에서 배포 결과를 확인할 수 있습니다.

## 카테고리 관리

`_config.yml`의 `category_list`에 적힌 카테고리는 글이 없어도 표시됩니다.
현재 고정 카테고리는 없습니다. 글에 카테고리를 지정하면 자동으로 함께 표시됩니다.

## 주요 파일

- `_config.yml`: 블로그 제목, 작성자, 주소, 고정 카테고리
- `_posts/`: 게시글
- `_layouts/`: 공통 화면과 게시글 레이아웃
- `assets/css/style.css`: 스타일
- `index.html`: 메인 화면
- `categories.html`: 카테고리별 글 목록
- `about.md`: 소개
