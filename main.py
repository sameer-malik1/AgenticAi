from crewai.flow.flow import Flow, start, listen
import time


class BasicFlow(Flow):
    @start()
    def func1(self):
        print("step 1", flush=True)
        time.sleep(3)

    @listen(func1)
    def func2(self):
        print("step 2")
        time.sleep(3)
    
    @listen(func2)
    def func3(self):
        print("step 3")
        time.sleep(3)

def kickoff():
    obj = BasicFlow()
    obj.kickoff()


if __name__ == "__main__":
    kickoff()
