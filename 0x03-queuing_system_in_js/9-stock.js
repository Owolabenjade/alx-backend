import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const client = createClient();
const getAsync = promisify(client.get).bind(client);

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find(product => product.id === id);
}

function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock) : 0;
}

app.get('/list_products', (req, res) => {
  const products = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  }));
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  
  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - reservedStock;
  
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  
  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - reservedStock;
  
  if (currentQuantity <= 0) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }
  
  reserveStockById(itemId, reservedStock + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

app.listen(1245, () => {
  console.log('Server running on port 1245');
});
