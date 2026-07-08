# 작심삼일 수사대 - Backend

AI가 목표 실패 원인을 분석해 탐정처럼 브리핑해주는 목표 관리 서비스의 백엔드 서버입니다.

## 🔗 링크

- 🌐 서비스 바로가기: [[프론트엔드 배포 URL](https://jakshim-frontend-one.vercel.app/)]
- 📄 API 문서 (Swagger): [[백엔드 URL](https://app-gowest-dev.azurewebsites.net/docs)]
- 💻 Frontend 레포: [\[링크\]](https://github.com/jaksim-susa/jaksim-frontend)

## 🛠️ 기술 스택

- **Language/Framework**: Python, FastAPI
- **Database**: MongoDB
- **AI**: Google Gemini API
- **Infra**: Azure App Service, Azure Key Vault
- **Auth**: 카카오 OAuth2, JWT

## ✨ 주요 기능

- 카카오 소셜 로그인 및 JWT 기반 인증
- 목표 생성 및 관리 API
- 성공/실패 기록 및 실패 사유 저장 API
- Gemini 기반 AI 실패 원인 분류 API
- Gemini 기반 AI 수사 브리핑 생성 API
- 성공률/실패 패턴 통계 API

## 📁 폴더 구조

```
app/
├── api/
│ └── routes/ # 라우터 (엔드포인트)
├── core/ # 설정, 보안
├── models/ # MongoDB 도큐먼트 모델
├── schemas/ # 요청/응답 스키마 (Pydantic)
└── service/ # 비즈니스 로직
```

| 폴더          | 설명                                                                     |
| ------------- | ------------------------------------------------------------------------ |
| `api/routes/` | 로그인/인증, 목표 관리, 성공·실패 기록, AI 분류/브리핑 등 API 엔드포인트 |
| `core/`       | 환경 설정, JWT/Key Vault 등 보안 관련 로직                               |
| `models/`     | MongoDB에 저장되는 데이터 모델 정의                                      |
| `schemas/`    | API 요청/응답 데이터 검증용 Pydantic 스키마                              |
| `service/`    | Gemini 연동, 카카오 OAuth 처리 등 실제 비즈니스 로직                     |

## 🔐 환경 변수

주요 환경 변수 항목 (값은 보안상 비공개, Azure Key Vault로 관리)

| 변수명                          | 설명                       |
| ------------------------------- | -------------------------- |
| `DOCUMENT-DB-CONNECTION-STRING` | MongoDB 연결 문자열        |
| `GEMINI_API_KEY`                | Google Gemini API 키       |
| `JWT_SECRET_KEY`                | JWT 토큰 서명 키           |
| `KAKAO_CLIENT_ID`               | 카카오 OAuth 클라이언트 ID |
| `KAKAO_CLIENT_SECRET`           | 카카오 OAuth 시크릿        |

실제 값은 Azure Key Vault를 통해 안전하게 관리되며, 코드에 하드코딩되지 않습니다.

## 🚧 진행 상황

**✅ 구현 완료**

- 카카오 로그인 (OAuth2, JWT 기반 인증)
- 목표 생성
- 성공/실패 기록 (실패 사유 입력)
- AI 실패 원인 분류
- AI 수사 브리핑
- 분석 대시보드 (통계/패턴 그래프)
- 라이트/다크 테마

**📋 추가 개발 예정**

- 로그아웃
- 목표 수정/삭제/종료
- 메모 작성
- 캐릭터 성장

## 📄 관련 문서

프로젝트 소개, 기획 문서(API/DB/기능정의서 등)는 [[노션 페이지](https://jaksim3il.notion.site/37c01887c58f80978dd8c7bcf39ce0ba?pvs=74)]에서 확인하실 수 있습니다.
