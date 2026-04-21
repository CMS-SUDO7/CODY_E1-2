from quiz import Quiz
import json 
import os

STATE_FILE = "state.json"

class Quiz_game:
    def __init__(self):
        self.문제들 = []
        self.점수 = 0
        self.최고점수 = 0
        self.불러오기()

    def 시작(self):
        if not self.문제들:
            self.load_기본문제()

        self.점수 = 0

        for quiz in self.문제들:
            quiz.화면()

            선택 = self.예외처리("정답을 고르세요(1~4): ", 1, 4)

            if quiz.정답확인(선택):
                print("정답")
                self.점수 +=1
            else:
                print("오답")
        print(f"최종 점수: {self.점수}/{len(self.문제들)}")

        if self.점수 > self.최고점수:
            self.최고점수 = self.점수
            print('최고점수 갱신')
        
        self.저장하기()

    def load_기본문제(self):
        self.문제들 = [
            Quiz("한국의 수도는?", ["서울", "부산", "대구", "인천"], 1),
            Quiz("일본의 수도는?", ["오사카", "도쿄", "교토", "나고야"], 2),
            Quiz("미국의 수도는?", ["뉴욕", "LA", "워싱턴 D.C.", "시카고"], 3),
            Quiz("프랑스 수도는?", ["파리", "리옹", "니스", "마르세유"], 1),
            Quiz("영국 수도는?", ["맨체스터", "런던", "리버풀", "브리스톨"], 2),
        ]

    def 목록보기(self):
        if not self.문제들:
            self.load_기본문제()

        print("2.퀴즈 목록")
        for i, quiz in enumerate(self.문제들, 1):
            print(f"{i}. {quiz.질문}")
            for j, choice in enumerate(quiz.보기, 1):
                print(f"   {j}. {choice}")

    def 메뉴(self):
        while True:
            print("1.퀴즈 풀기")
            print("2.퀴즈 목록")
            print("3.퀴즈 종료")
            print("4.퀴즈 추가")
            print("5 점수 확인")

            선택 = self.예외처리("번호를 입력하세요: ", 1, 5)
            
            if 선택 == 1:
                self.시작()
            elif 선택 == 2:
                self.목록보기()
            elif 선택 == 3:
                self.저장하기()
                print('게임 종료')
                break
            elif 선택 == 4:
                self.퀴즈추가()
            elif 선택 == 5:
                self.점수확인()
            else:
                print('잘못된 입력입니다')



    def 저장하기(self, 파일명="state.json"):
        데이터 = {
            "최고점수": self.최고점수,
            "문제들": [quiz.딕셔너리() for quiz in self.문제들]
        }
        
        try:
            with open(파일명, "w", encoding="utf-8") as f:
                json.dump(데이터, f, ensure_ascii=False, indent=4)
            print(f"{파일명}에 저장 완료")
        except Exception as e:
            print("저장 오류:", e)

    def 불러오기(self, 파일명="state.json"):
        if not os.path.exists(파일명):
            print("저장된 파일이 없어 기본 문제를 불러옵니다.")
            self.load_기본문제()
            return

        try:
            with open(파일명, "r", encoding="utf-8") as f:
                데이터 = json.load(f)
            self.최고점수 = 데이터.get("최고점수", 0)
            self.문제들 = [Quiz.from_딕셔너리(d) for d in 데이터["문제들"]]
            print(f"{파일명}에서 불러오기 완료")

        except (json.JSONDecodeError, FileNotFoundError):
            print("파일이 손상되었거나 없어 기본 문제를 불러옵니다.")
            self.load_기본문제()
        except Exception as e:
            print(f"불러오기 중 오류 발생: {e}")
            self.load_기본문제()
            
    def 퀴즈추가(self):
        질문 = input('문제:').strip()
        보기 = []

        for i in range(4):
            선택지 = input(f"선택지{i+1}:")
            보기.append(선택지)
        정답 = self.예외처리("정답 번호 (1~4): ", 1, 4)

        새퀴즈 = Quiz(질문, 보기, 정답)
        self.문제들.append(새퀴즈)

        self.저장하기()
        print('문제추가완료')

    def 예외처리(self, 메세지, 최소값, 최대값):
        while True:
            try:
                값 = input(메세지).strip()
                if 값 == '':
                    print('숫자를 입력해주세요')
                    continue

                숫자 = int(값)

                if 숫자 < 최소값 or 숫자 > 최대값:
                    print(f'{최소값}~{최대값}사이 숫자를 입력하세요')
                    continue

                return 숫자

            except ValueError:
                print("숫자로 입력하세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n안전하게 종료합니다.")
                self.저장하기()
                raise SystemExit

    def 점수확인(self):
        if self.최고점수 == 0 and self.점수 == 0:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"현재 점수: {self.점수}")
            print(f"최고 점수: {self.최고점수}")