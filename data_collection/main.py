import subprocess
import sys 


from apscheduler.schedulers.blocking import BlockingScheduler

def run_spider_job():
    subprocess.run([sys.executable, "spider_runner.py"])

if __name__ == '__main__': 
    scheduler = BlockingScheduler()
    scheduler.add_job(run_spider_job, "interval", minutes=10)
    scheduler.start()