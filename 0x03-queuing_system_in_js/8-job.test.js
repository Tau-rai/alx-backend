// Wrting the test for job creation
const kue = require('kue');
const { expect } = require('chai');

const queue = kue.createQueue();

const createPushNotificationJobs = require('./8-job');

describe('createPushNotificationJobs', () => {
  beforeEach(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationJobs('jobs', queue)).to.throw('Jobs should be an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is a test job' },
      { phoneNumber: '45678901', message: 'Second test job' }
    ];
    createPushNotificationJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });
});
