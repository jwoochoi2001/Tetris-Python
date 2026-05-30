# 🎮 Terminal Tetris

Python과 curses 라이브러리를 활용하여 개발한 콘솔 기반 테트리스 게임입니다.

기본적인 테트리스 플레이 기능뿐만 아니라 Hold 시스템, Ghost Piece, Pause 메뉴, 난이도 선택, 7-Bag 랜덤 시스템 등을 구현하여 실제 테트리스에 가까운 플레이 경험을 제공합니다.

---

## 🎯 게임 소개

Terminal Tetris는 Python과 curses 라이브러리를 활용하여 개발한 콘솔 기반 테트리스 게임입니다.

블록 이동, 회전, Hold 시스템, Ghost Piece, 레벨 시스템, 7-Bag 랜덤 알고리즘 등 실제 테트리스의 핵심 기능들을 구현하였으며, GUI 없이 터미널 환경에서 플레이할 수 있습니다.

---

## ✨ 주요 기능

### 🧩 7-Bag 랜덤 시스템

실제 현대 테트리스에서 사용하는 7-Bag 시스템을 적용했습니다.

* 7개의 블록이 한 번씩 등장
* 한 세트가 끝나면 다시 섞어서 생성
* 특정 블록이 지나치게 안 나오거나 몰아서 나오는 현상 감소

### 🔄 Hold 기능

현재 블록을 저장해두고 나중에 사용할 수 있습니다.

* C 키로 Hold
* 블록 고정 전까지 1회 사용 가능
* Hold 슬롯과 현재 블록을 교환

### 👻 Ghost Piece

현재 블록이 떨어질 위치를 미리 표시합니다.

### ⏸ Pause 메뉴

게임 진행 중 P 키를 눌러 일시정지가 가능합니다.

### 📈 레벨 시스템

* 라인 제거 시 점수 획득
* 10줄 제거마다 레벨 상승
* 레벨이 높아질수록 낙하 속도 증가

### 🎚 난이도 선택

게임 시작 시 난이도 선택 가능

* Beginner 
* Expert
* (난이도별 속도 차이가 존재)

---

## 🕹 조작 방법

| 키     | 기능     |
| ----- | ------ |
| ← →   | 좌우 이동  |
| ↑     | 회전     |
| ↓     | 소프트 드롭 |
| Space | 하드 드롭  |
| C     | Hold   |
| P     | 일시정지   |
| Q     | 종료     |

---

## 🎮 게임 화면

### 시작 화면

* 난이도 선택
* 조작법 확인

### 플레이 화면

* 게임 보드
* Hold 창
* Next 창
* 점수
* 레벨
* 제거 라인 수

### 일시정지 화면

* Continue
* Quit Menu

### 게임 오버 화면

* 최종 점수 표시
* 플레이 난이도 표시

---

## 🧠 객체지향 구조

### Game

게임의 핵심 로직 담당

* 블록 생성
* 충돌 판정
* 점수 계산
* 라인 제거
* 홀드 기능
* 게임 루프

### Block

테트로미노 모양 데이터 관리

### Color

curses 색상 설정 관리

### Main

게임 시작 화면 및 전체 실행 담당

---

## 📁 프로젝트 구조

```text
Tetris-Python/
│
├── main.py
├── game.py
├── block.py
├── color.py
│
└── README.md
```

---

## ▶ 실행 방법

### 1. 프로젝트 다운로드

```bash
git clone https://github.com/jwoochoi2001/Tetris-Python.git
```

### 2. 프로젝트 폴더 이동

```bash
cd Tetris-Python
```

### 3. 실행

```bash
python3 main.py
```

---

## 💻 개발 환경

* Language : Python 3
* Library : curses
* IDE : PyCharm
* OS : macOS

---

## 📌 구현 기능

* 7-Bag Random System
* Hold System
* Ghost Piece
* Hard Drop
* Soft Drop
* Pause Menu
* Difficulty Selection
* Level System
* Score System
* Line Clear System
* Game Over Screen

---

## 👨‍💻 개발자

최정우

GitHub:
https://github.com/jwoochoi2001

---

## 🚀 소식

본 프로젝트는 Python의 객체지향 프로그래밍(OOP) 구조를 학습하고, 콘솔 환경에서 게임 로직을 구현하기 위해 제작되었습니다.

게임 루프, 충돌 판정, 랜덤 알고리즘, 상태 관리, 사용자 입력 처리 등을 직접 구현하며 Python 프로그래밍 역량 향상을 목표로 개발하였습니다.
