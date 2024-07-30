// Implementing a simple stock management system using Redis.
const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const listProducts = [
    {
        itemId: 1,
        itemName: 'Suitecase 250',
        price: 50,
        initialAvailableQuantity: 4
    },
    {
        itemId: 2,
        itemName: 'Suitecase 450',
        price: 100,
        initialAvailableQuantity: 10
    },
    {
        itemId: 3,
        itemName: 'Suitecase 650',
        price: 350,
        initialAvailableQuantity: 2
    },
    {
        itemId: 4,
        itemName: 'Suitecase 1050',
        price: 550,
        initialAvailableQuantity: 5
    },
];

function getItemById(id) {
    return listProducts.find(product => product.itemId === id);
}

const app = express();
const port = 1245;

app.get('/list_products', (req, res) => {
    res.json(listProducts);
});

const client = redis.createClient();

client.on('connect', () => {
    console.log('Connected to Redis');
});

client.on('error', (err) => {
    console.error('Redis error:', err);
});

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function reserveStockById(itemId, stock) {
    try {
        await setAsync(`item.${itemId}`, stock);
        console.log(`Stock reserved for item ${itemId}`);
    } catch (err) {
        console.error('Error reserving stock:', err);
    }
}

async function getCurrentReservedStockById(itemId) {
    try {
        const stock = await getAsync(`item.${itemId}`);
        return stock ? parseInt(stock, 10) : 0;
    } catch (err) {
        console.error('Error getting reserved stock:', err);
        return 0;
    }
}

app.get('/list_products/:id', async (req, res) => {
    const itemId = parseInt(req.params.id, 10);
    const item = getItemById(itemId);
    if (!item) {
        res.status(404).json({ error: 'Product not found' });
        return;
    }

    try {
        const reservedStock = await getCurrentReservedStockById(itemId);
        const availableStock = item.initialAvailableQuantity - reservedStock;
        res.json({
            ...item,
            availableStock,
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.get('/reserve_product/:id', async (req, res) => {
    const itemId = parseInt(req.params.id, 10);
    const item = getItemById(itemId);
    if (!item) {
        res.status(404).json({ error: 'Product not found' });
        return;
    }

    try {
        const reservedStock = await getCurrentReservedStockById(itemId);
        if (reservedStock >= item.initialAvailableQuantity) {
            res.status(403).json({ error: 'Not enough stock available' });
            return;
        }

        await reserveStockById(itemId, reservedStock + 1);
        res.json({ status: `Reservation confirmed`, itemId: itemId });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
