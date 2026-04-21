class Quiz:
    def __init__(self, 질문, 보기, 정답):
        self.질문 = 질문
        self.보기 = 보기
        self.정답 = 정답

    def 화면(self):
        print(f"{self.질문}")
        for i, choice in enumerate(self.보기, 1):
            print(f"{i}. {choice}")

    def 정답확인(self, 선택번호):
        return 선택번호 == self.정답
    
    def 딕셔너리(self):
        return {
            "질문": self.질문,
            "보기": self.보기,
            "정답": self.정답
        }

    @staticmethod
    def from_딕셔너리(data):
        return Quiz(data["질문"], data["보기"], data["정답"])