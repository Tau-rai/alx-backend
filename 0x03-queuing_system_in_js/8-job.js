// Writing the job creation function

function createPushNotificationJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw new Error('Jobs should be an array');

  jobs.forEach((job) => {
      const jobQueue = queue.create('push_notification_code_3', job);
      jobQueue.save((err) => {
          if (!err) {
              console.log(`Notification job created: ${jobQueue.id}`);
          } else {
              console.error('Error creating job:', err);
          }
      });

      jobQueue.on('complete', () => {
          console.log(`Notification job ${jobQueue.id} completed`);
      }).on('failed', (err) => {
          console.log(`Notification job ${jobQueue.id} failed: ${err}`);
      }).on('progress', (progress) => {
          console.log(`Notification job ${jobQueue.id} ${progress}% complete`);
      });
  });
}

module.exports = createPushNotificationJobs;
