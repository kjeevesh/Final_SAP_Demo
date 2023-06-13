from flask import Flask, request
from crontab import CronTab
import random

app = Flask(__name__)

class CronJobManager:
    def __init__(self):
        self.cron = CronTab(user='SAPITSM')

    def add_cron_job(self, program_names, unique_id, schedule):
        # Iterate over the program names and create a cron job for each
        for program_name in program_names:
            # Construct the command for running the program
            command = f'python3 /home/SAPITSM/finalsapdemo/Flask_api/controls/{program_name}.py {unique_id} > /home/SAPITSM/{program_name}/backup.log 2>&1'

            # Add a new cron job with the unique ID
            job = self.cron.new(command=command)
            job.set_comment(unique_id)

            # Set the cron schedule
            job.setall(schedule)

        # Write the updated crontab
        self.cron.write()

    def delete_cron_job(self, unique_id):
        # Iterate over each cron job
        for job in self.cron:
            # Check if the job's comment matches the unique ID
            if job.comment == unique_id:
                # Remove the job
                self.cron.remove(job)

        # Write the updated crontab
        self.cron.write()

manager = CronJobManager()

@app.route('/create_cron_jobs', methods=['POST'])
def create_cron_jobs():
    program_names = request.json.get('program_names')
    unique_id = str(random.randint(1000, 9999))
    schedule = request.json.get('schedule')

    manager.add_cron_job(program_names, unique_id, schedule)
    return 'Cron jobs created successfully'

if __name__ == '__main__':
    app.run()

