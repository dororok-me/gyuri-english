# 규리와 영어 대화 (시험판) 올리기 안내

## 들어 있는 것
- index.html : 영어 대화 앱 (규리가 질문 → 아이 대답 → 칭찬 → 녹화)
- expr/index.html : 표정 샘플 (기본·웃음·놀람·궁금·울음·칭찬)
- manifest.webmanifest, icon-*.png : 휴대폰 홈 화면에 앱처럼 추가하기 위한 파일
- 검색 사이트에 노출되지 않도록 설정(noindex)되어 있어요. 주소를 아는 사람만 찾아올 수 있어요.

## GitHub Pages로 올리기 (무료, https 자동)
1. github.com 로그인 → 오른쪽 위 + → New repository
2. 이름 예: gyuri-english  /  Public 선택 → Create repository
3. 화면의 "uploading an existing file" 클릭 → 이 폴더 안의 파일 전체(expr 폴더 포함)를 끌어다 놓기 → Commit changes
   (폴더째 끌어다 놓으면 되고, .nojekyll 같은 점(.)으로 시작하는 파일은 안 올라가도 괜찮아요)
4. Settings → Pages → Source: Deploy from a branch → Branch: main / (root) → Save
5. 1~2분 뒤 아래 주소로 열려요
   https://내아이디.github.io/gyuri-english/
   표정 샘플: https://내아이디.github.io/gyuri-english/expr/

## 학부모에게 안내할 때
- 아이폰: Safari로 열기 → 공유 버튼 → "홈 화면에 추가"
- 안드로이드: Chrome으로 열기 → ⋮ 메뉴 → "홈 화면에 추가"
- 처음 시작할 때 카메라·마이크 허용을 눌러야 해요.
- 음성 인식이 안 되면 "잘 대답했어요" 버튼을 누르면 돼요. 아이폰에서는 이 방법이 더 안정적이에요.

## 수정본을 다시 올릴 때
같은 이름의 파일을 같은 저장소에 다시 업로드(덮어쓰기)하면 1~2분 뒤 반영돼요.
