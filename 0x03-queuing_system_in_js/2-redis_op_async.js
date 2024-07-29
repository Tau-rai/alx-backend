// basic redis client using node_redis module
import { createClient } from 'redis';
import redis from 'redis';
import { promisify } from 'util';


const client = createClient();
const getAsync = promisify(client.get).bind(client);

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
});

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, (err, reply) => {
        redis.print(`Reply: ${reply}`);
    });
}

const displaySchoolValue = async (schoolName) => {
    try {
        const reply = await getAsync(schoolName);
        console.log(reply);
    } catch (error) {
        console.error('Error fetching school value:', error);
    }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
