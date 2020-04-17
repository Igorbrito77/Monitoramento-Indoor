const  express = require('express');
const routes = express.Router();

const maq = require('./controllers/maq');

routes.get('/', async (req, res) =>{
    const data = await maq.list(req, res);

    return res.json(data);
});


module.exports = routes;